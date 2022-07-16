import argparse
import csv

from opensearch_dsl import Q, Search
from opensearchpy import OpenSearch, RequestsHttpConnection


def map_hit(hit):
    # TODO: recid is currently wrong, it should be changed.
    return {
        "doi": hit.dois,
        "recid": hit.meta.id,
        "journal": hit.publication_info[0].journal_title,
        "creation_date": hit.record_creation_date,
        # TODO: Add primary category
        # "primary_category": hit.arxiv_eprints[0].categories[0],
        "authors": hit.authors,
    }


def get_authors(dict):
    return dict["authors"]


def get_country_with_highest_gdp(countries, gdps):
    values = [(country, gdps[country]) for country in countries]
    return max(values, key=lambda t: t[1])[0]


def get_most_important_country(countries, gdps):
    hep_institutes = ["KEK", "SLAC", "DESY", "FERMILAB", "JINR"]
    if len(countries) == 0:
        return countries[0]
    if "CERN" in countries:
        return "CERN"
    if len(present_hep := set(hep_institutes).intersection(set(countries))) > 0:
        if len(present_hep) == 1:
            return present_hep.pop()
        return get_country_with_highest_gdp(
            countries, gdps
        )  # TODO: Change this to use HEP countries
    return get_country_with_highest_gdp(countries, gdps)


def get_gdp_from_file():
    with open("gdp.csv", "r") as file:
        reader = csv.reader(file)
        ret_dict = {}
        for row in reader:
            value = row[3]
            ret_dict[row[0]] = float(value) if value else 0
        ret_dict["Taiwan"] = ret_dict["China"]
        return ret_dict


def build_countries_list_values(countries, all_countries_list):
    ret_dict = {country: 0 for country in all_countries_list}
    for country in countries:
        ret_dict[country] += 1
    ret_list = [value for value in ret_dict.items()]
    ret_list.sort()
    return [amount for _, amount in ret_list]


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

    client = OpenSearch(
        hosts=[{"host": host, "port": port, "url_prefix": "/es"}],
        http_auth=(username, password),
        use_ssl=False,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
        connection_class=RequestsHttpConnection,
    )

    s = (
        Search(using=client, index="scoap3-records")
        .extra(from_=0, size=10000)
        .query(
            "nested",
            path="imprints",
            query=Q(
                "range",
                **{
                    "imprints.date": {
                        "gt": f"{from_year}-01-01T00:00:00",
                        "lt": f"{to_year}-01-01T00:00:00",
                    }
                },
            ),
        )
    )
    full_country_list = [
        "Afghanistan",
        "Albania",
        "Algeria",
        "Angola",
        "Antigua and Barbuda",
        "Argentina",
        "Armenia",
        "Australia",
        "Austria",
        "Azerbaijan",
        "Bahamas",
        "Bahrain",
        "Bangladesh",
        "Barbados",
        "Belarus",
        "Belgium",
        "Belize",
        "Benin",
        "Bhutan",
        "Bolivia",
        "Bosnia and Herzegovina",
        "Botswana",
        "Brazil",
        "Brunei",
        "Bulgaria",
        "Burkina Faso",
        "Burundi",
        "Cabo Verde",
        "Cambodia",
        "Cameroon",
        "Canada",
        "Caribbean small states",
        "Central African Republic",
        "CERN",
        "Chad",
        "Chile",
        "China",
        "Colombia",
        "Comoros",
        "Congo Dem. Rep.",
        "Congo Rep.",
        "Costa Rica",
        "Cote d'Ivoire",
        "Croatia",
        "Cuba",
        "Cyprus",
        "Czech Republic",
        "Denmark",
        "DESY",
        "Dominica",
        "Dominican Republic",
        "Ecuador",
        "Egypt",
        "El Salvador",
        "Equatorial Guinea",
        "Estonia",
        "Ethiopia",
        "FERMILAB",
        "Fiji",
        "Finland",
        "France",
        "Gabon",
        "Gambia",
        "Georgia",
        "Germany",
        "Ghana",
        "Greece",
        "Grenada",
        "Guatemala",
        "Guinea",
        "Guinea-Bissau",
        "Guyana",
        "Haiti",
        "Honduras",
        "Hong Kong",
        "HUMAN CHECK",
        "Hungary",
        "Iceland",
        "India",
        "Indonesia",
        "Iran",
        "Iraq",
        "Ireland",
        "Israel",
        "Italy",
        "Jamaica",
        "Japan",
        "JINR",
        "Jordan",
        "Kazakhstan",
        "KEK",
        "Kenya",
        "Kiribati",
        "Kosovo",
        "Kuwait",
        "Kyrgyz Republic",
        "Latvia",
        "Lebanon",
        "Lesotho",
        "Liberia",
        "Libya",
        "Lithuania",
        "Luxembourg",
        "Macao SAR China",
        "Macedonia",
        "Madagascar",
        "Malawi",
        "Malaysia",
        "Maldives",
        "Mali",
        "Malta",
        "Marshall Islands",
        "Mauritania",
        "Mauritius",
        "Mexico",
        "Micronesia Fed. Sts.",
        "Moldova",
        "Monaco",
        "Mongolia",
        "Montenegro",
        "Morocco",
        "Mozambique",
        "Myanmar",
        "Namibia",
        "Nepal",
        "Netherlands",
        "New Zealand",
        "Nicaragua",
        "Niger",
        "Nigeria",
        "North Korea",
        "Norway",
        "Oman",
        "Other small states",
        "Pakistan",
        "Palestine",
        "Panama",
        "Papua New Guinea",
        "Paraguay",
        "Peru",
        "Philippines",
        "Poland",
        "Portugal",
        "Puerto Rico",
        "Qatar",
        "San Marino",
        "Romania",
        "Russia",
        "Rwanda",
        "Samoa",
        "Sao Tome and Principe",
        "Saudi Arabia",
        "Senegal",
        "Serbia",
        "Seychelles",
        "Sierra Leone",
        "Singapore",
        "SLAC",
        "Slovakia",
        "Slovenia",
        "Solomon Islands",
        "South Africa",
        "South Korea",
        "Spain",
        "Sri Lanka",
        "St. Kitts and Nevis",
        "St. Lucia",
        "St. Vincent and the Grenadines",
        "Sudan",
        "Suriname",
        "Swazilend",
        "Sweden",
        "Switzerland",
        "Syria",
        "Taiwan",
        "Tajikistan",
        "Tanzania",
        "Thailand",
        "Timor-Leste",
        "Togo",
        "Tonga",
        "Trinidad and Tobago",
        "Tunisia",
        "Turkey",
        "Turkmenistan",
        "Uganda",
        "UK",
        "Ukraine",
        "United Arab Emirates",
        "Uruguay",
        "USA",
        "Uzbekistan",
        "Venezuela",
        "Vietnam",
        "Yemen",
        "Zambia",
        "Zimbabwe",
    ]

    with open("results.csv", "w") as file:
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

        for hit in s.scan():
            entry = map_hit(hit)
            authors_list = get_authors(entry)

            data_line = [
                entry["doi"][0]["value"],
                entry["recid"],
                entry["journal"],
                entry["creation_date"],
                "",
                len(entry["authors"]),
            ]
            authors = entry["authors"]

            affiliations_per_author = [
                list(map(lambda x: x["country"], author["affiliations"]))
                for author in authors
            ]
            countries = [
                get_most_important_country(affils, gdps)
                for affils in affiliations_per_author
            ]

            # TODO: build_countries_list_values should return percentages instead of absolute values.
            writer.writerow(
                data_line + build_countries_list_values(countries, full_country_list)
            )

            # TODO: Fix "missing scrollID" issue.
