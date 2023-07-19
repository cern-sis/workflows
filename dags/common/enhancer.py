import datetime
import re

from common.constants import FN_REGEX


class Enhancer:
    def __construct_abstracts(self, item, publisher):
        item["abstracts"] = [{"value": item.pop("abstract", ""), "source": publisher}]

    def __construct_acquisition_source(self, item, creation_date, publisher):
        item["acquisition_source"] = {
            "source": publisher,
            "method": publisher,
            "date": creation_date,
        }

    def __construct_copyright(self, item):
        item["copyright"] = [
            {
                "holder": item.pop("copyright_holder", ""),
                "year": item.pop("copyright_year", ""),
                "statement": item.pop("copyright_statement", ""),
                "material": item.pop("copyright_material", ""),
            }
        ]

    def __construct_imprints(self, item, publisher):
        item["imprints"] = [
            {"date": item.pop("date_published", ""), "publisher": publisher}
        ]

    def __construct_record_creation_date(self, item, creation_date):
        item["record_creation_date"] = creation_date

    def __construct_titles(self, item, publisher):
        item["titles"] = [
            {
                # removing footer notes (fn tag with its content)
                "title": FN_REGEX.sub("", item.pop("title", "")).strip(),
                "subtitle": item.pop("subtitle", ""),
                "source": publisher,
            }
        ]

    def __remove_country(self, item):
        pattern_for_cern_cooperation_agreement = re.compile(
            r"cooperation agreement with cern", re.IGNORECASE
        )
        for author in item.get("authors", []):
            for affiliation in author.get("affiliations", []):
                match_pattern = pattern_for_cern_cooperation_agreement.search(
                    affiliation.get("value", "")
                )
                if match_pattern:
                    affiliation.pop("country", None)

    def __call__(self, publisher, item):
        creation_date = datetime.datetime.now().isoformat()
        item_copy = item.copy()
        self.__construct_abstracts(item_copy, publisher)
        self.__construct_acquisition_source(item_copy, creation_date, publisher)
        self.__construct_copyright(item_copy)
        self.__construct_imprints(item_copy, publisher)
        self.__construct_record_creation_date(item_copy, creation_date)
        self.__construct_titles(item_copy, publisher)
        self.__remove_country(item)
        return item_copy
