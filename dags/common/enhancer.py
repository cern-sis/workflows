import datetime


class Enhancer:
    def __constuct_abstracts(self, item, publisher):
        item["abstracts"] = [{"value": item.pop("abstracts", ""), "source": publisher}]

    def __construct_acquisition_source(self, item, creation_date, publisher):
        item["acquisition_source"] = {
            "source": publisher,
            "method": publisher,
            "date": creation_date,
            "submission_number": "path/to/the/file",
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
                "title": item.pop("title", ""),
                "subtitle": item.pop("subtitle", ""),
                "source": publisher,
            }
        ]

    def __call__(self, publisher, item):
        creation_date = datetime.datetime.now().isoformat()
        item_copy = item.copy()
        self.__constuct_abstracts(item_copy, publisher)
        self.__construct_acquisition_source(item_copy, creation_date, publisher)
        self.__construct_copyright(item_copy)
        self.__construct_imprints(item_copy, publisher)
        self.__construct_record_creation_date(item_copy, creation_date)
        self.__construct_titles(item_copy, publisher)
        return item_copy
