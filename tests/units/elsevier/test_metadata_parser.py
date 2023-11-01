from common.utils import parse_without_names_spaces
from elsevier.metadata_parser import ElsevierMetadataParser
from pytest import fixture, mark, param


@fixture(scope="module")
def parser():
    return ElsevierMetadataParser(
        doi="10.1016/j.physletb.2023.137730",
        file_path="extracted/CERNQ000000010669A/CERNQ000000010669",
    )


@fixture
def article(shared_datadir):
    with open(shared_datadir / "CERNQ000000010011" / "dataset.xml") as file:
        return parse_without_names_spaces(file.read())


@fixture()
def parsed_article(parser, article):
    return parser.parse(article)


@mark.parametrize(
    "expected, key",
    [
        param(
            [{"journal_title": "PLB", "year": 2023}],
            "publication_info",
            id="test_publication_info",
        ),
        param(
            "2023-02-04",
            "date_published",
            id="test_published_date",
        ),
        param(
            [{"primary": "PLB"}],
            "collections",
            id="test_collections",
        ),
        param(
            [
                {
                    "license": "CC-BY-3.0",
                    "url": "http://creativecommons.org/licenses/by/3.0/",
                }
            ],
            "license",
            id="test_license",
        ),
        param(
              [{'value': {'filetype': 'pdf', 'path': 'extracted/CERNQ000000010669A/CERNQ000000010669/S0370269323000643/main.pdf'}}, {'value': {'filetype': 'xml', 'path': 'extracted/CERNQ000000010669A/CERNQ000000010669/S0370269323000643/main.pdf'}}, {'value': {'filetype': 'pdfa', 'path': 'extracted/CERNQ000000010669A/CERNQ000000010669/S0370269323000643/main_a-2b.pdf'}}],
            "local_files",
            id="test_local_files",
        ),
    ],
)
def test_elsevier_dataset_parsing(parsed_article, expected, key):
    assert parsed_article[key] == expected
