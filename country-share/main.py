import argparse
import csv

import urllib3
from countries import full_country_list
from elasticsearch import Elasticsearch
from utils import (
    build_countries_list_values,
    get_affiliations,
    get_authors,
    get_gdp_from_file,
    get_most_important_country,
    get_primary_category,
)

urllib3.disable_warnings()


def map_hit(hit):
    return {
        "doi": hit["dois"],
        "recid": hit["control_number"],
        "journal": hit["publication_info"][0]["journal_title"],
        "creation_date": hit["record_creation_date"],
        "primary_category": get_primary_category(hit),
        "authors": hit["authors"],
    }


parser = argparse.ArgumentParser()

parser.add_argument("--from_year", help="Starting year to fetch articles.")
parser.add_argument("--to_year", help="Ending year to fetch articles.")
parser.add_argument("--host", help="ES Cluster Hostname.")
parser.add_argument("--port", help="ES Cluster Port.")
parser.add_argument("--username", help="ES Cluster Username.")
parser.add_argument("--password", help="ES Cluster Password.")

if __name__ == "__main__":
    args = parser.parse_args()
    from_year = args.from_year
    to_year = args.to_year
    host = args.host
    port = args.port
    username = args.username
    password = args.password

    if from_year is None:
        raise Exception("Missing from_year argument.")
    if to_year is None:
        raise Exception("Missing to_year argument.")
    if host is None:
        raise Exception("Missing host argument.")
    if port is None:
        raise Exception("Missing port argument.")
    if username is None:
        raise Exception("Missing username argument.")
    if password is None:
        raise Exception("Missing password argument.")

    client = Elasticsearch(
        hosts=[
            {
                "host": (host),
                "http_auth": (username, password),
                "http_compress": True,
                "port": 443,
                "timeout": 60,
                "url_prefix": "es",
                "use_ssl": True,
                "verify_certs": False,
            }
        ]
    )
    data = client.search(
        index="scoap3-records",
        scroll="2m",
        _source=[
            "dois",
            "control_number",
            "publication_info",
            "record_creation_date",
            "arxiv_eprints",
            "authors",
        ],
        body={
            "query": {"range": {"year": {"gte": f"{from_year}", "lte": f"{to_year}"}}}
        },
    )
    sid = data["_scroll_id"]
    scroll_size = len(data["hits"]["hits"])
    count = 0
    count_exception = 0
    countries_error = []
    file_name = "results.csv"
    with open(file_name , "w") as file:
        writer = csv.writer(file)
        header = [
            "doi",
            "recid",
            "journal",
            "creation_date",
            "primary_category",
            "total_authors",
        ] + full_country_list
        writer.writerow(header)
        gdps = get_gdp_from_file()
        while scroll_size > 0:
            hits = data["hits"]["hits"]
            for hit in hits:
                try:
                    entry = map_hit(hit["_source"])
                    authors_list = get_authors(entry)
                    data_line = [
                        entry["doi"][0]["value"],
                        entry["recid"],
                        entry["journal"],
                        entry["creation_date"],
                        entry["primary_category"],
                        len(entry["authors"]),
                    ]
                    authors = entry["authors"]
                    affiliations_per_author = get_affiliations(authors)
                    countries = [
                        get_most_important_country(affils, gdps)
                        for affils in affiliations_per_author
                    ]
                    writer.writerow(
                        data_line
                        + build_countries_list_values(countries, full_country_list)
                    )
                except Exception as e:
                    print("Exception occured", e ,". Most likely need to change countries mapping!")
                    count_exception+=1

            data = client.scroll(scroll_id=sid, scroll="2m")
            sid = data["_scroll_id"]
            scroll_size = len(data["hits"]["hits"])
        client.clear_scroll(scroll_id=sid)
