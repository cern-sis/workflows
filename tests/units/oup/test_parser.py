import os

from common.utils import parse_without_names_spaces
from oup.parser import OUPParser
from pytest import fixture, mark, param


@fixture(scope="module")
def iop_parser():
    yield OUPParser()


@fixture
def articles(shared_datadir):
    articles = []
    file_names = os.listdir(shared_datadir)
    for file_name in file_names:
        with open(shared_datadir / file_name) as file:
            articles.append(parse_without_names_spaces(file.read()))
    yield articles


@fixture()
def parsed_articles(iop_parser, articles):
    yield [iop_parser._publisher_specific_parsing(article) for article in articles]


@mark.parametrize(
    "expected, key",
    [
        param(
            [
                ["10.1093/ptep/ptac108"],
                ["10.1093/ptep/ptac120"],
                ["10.1093/ptep/ptac113"],
            ],
            "dois",
            id="test_dois",
        ),
        param(
            ["article", "article", "article"],
            "journal_doctype",
            id="test_journal_doctype",
        ),
        param(
            [
                {"value": "2204.01249"},
                {"value": "2205.14599"},
                {"value": "2207.02498"},
            ],
            "arxiv_eprints",
            id="test_arxiv_eprints",
        ),
        param(
            [27, 16, 13],
            "page_nr",
            id="test_page_nr",
        ),
        param(
            [
                "We construct open-closed superstring interactions based on the open-closed homotopy algebra structure. This provides a classical open superstring field theory on general closed-superstring-field backgrounds described by classical solutions of the nonlinear equation of motion of the closed superstring field theory. We also give the corresponding WZW-like action through the map connecting the homotopy-based and WZW-like formulations.",
                "The<italic>KBc</italic>algebra is a subalgebra that has been used to construct classical solutions in Witten&#8217;s open string field theory, such as the tachyon vacuum solution. The main purpose of this paper is to give various operator sets that satisfy the<italic>KBc</italic>algebra. In addition, since those sets can contain matter operators arbitrarily, we can reproduce the solution of Kiermaier, Okawa, and Soler, and that of Erler and Maccaferri. Starting with a single D-brane solution on the tachyon vacuum, we replace the original<italic>KBc</italic>in it with an appropriate set to generate each of the above solutions. Thus, it is expected that the<italic>KBc</italic>algebra, combined with the single D-brane solution, leads to a more unified description of classical solutions.",
                "We study<italic>F</italic>-wave bottom mesons in heavy quark effective theory. The available experimental and theoretical data is used to calculate the masses of<italic>F</italic>-wave bottom mesons. The decay widths of bottom mesons are analyzed to find upper bounds for the associated couplings. We also construct Regge trajectories for our predicted data in the (<italic>J, M</italic><sup>2</sup>) plane, and our results nicely fit on Regge lines. Our results may provide crucial information for future experimental studies.",
            ],
            "abstract",
            id="test_abstract",
        ),
        param(
            [
                "Open-closed homotopy algebra in superstring field theory",
                "Generating string field theory solutions with matter operators from<italic>KBc</italic>algebra",
                "Study of<italic>F</italic>-wave bottom mesons in heavy quark effective theory",
            ],
            "title",
            id="test_title",
        ),
        param(
            [
                [
                    {
                        "surname": "Kunitomo",
                        "given_names": "Hiroshi",
                        "email": "kunitomo@yukawa.kyoto-u.ac.jp",
                        "affiliations": [
                            {
                                "institution": "Center for Gravitational Physics and Quantum Information, Yukawa Institute for Theoretical Physics",
                                "country": "Japan",
                            }
                        ],
                    }
                ],
                [
                    {
                        "surname": "Hata",
                        "given_names": "Hiroyuki",
                        "email": None,
                        "affiliations": [
                            {
                                "institution": "Department of Physics, Kyoto University",
                                "country": "Japan",
                            }
                        ],
                    },
                    {
                        "surname": "Takeda",
                        "given_names": "Daichi",
                        "email": None,
                        "affiliations": [
                            {
                                "institution": "Department of Physics, Kyoto University",
                                "country": "Japan",
                            }
                        ],
                    },
                    {
                        "surname": "Yoshinaka",
                        "given_names": "Jojiro",
                        "email": "george.yoshinaka@gauge.scphys.kyoto-u.ac.jp",
                        "affiliations": [
                            {
                                "institution": "Department of Physics, Kyoto University",
                                "country": "Japan",
                            }
                        ],
                    },
                ],
                [
                    {
                        "surname": "Garg",
                        "given_names": "Ritu",
                        "email": "rgarg_phd19@thapar.edu",
                        "affiliations": [
                            {
                                "institution": "School of Physics and Materials Science, Thapar Institute of Engineering and Technology",
                                "country": "INDIA",
                            }
                        ],
                    },
                    {
                        "surname": "Upadhyay",
                        "given_names": "A",
                        "email": None,
                        "affiliations": [
                            {
                                "institution": "School of Physics and Materials Science, Thapar Institute of Engineering and Technology",
                                "country": "INDIA",
                            }
                        ],
                    },
                ],
            ],
            "authors",
            id="test_authors",
        ),
        param(
            ["2022-08-18", "2022-09-02", "2022-08-27"],
            "date_published",
            id="test_date_published",
        ),
        param(
            [
                "Progress of Theoretical and Experimental Physics",
                "Progress of Theoretical and Experimental Physics",
                "Progress of Theoretical and Experimental Physics",
            ],
            "journal_title",
            id="test_journal_title",
        ),
        param(
            ["9", "9", "9"],
            "journal_issue",
            id="test_journal_issue",
        ),
        param(
            ["2022", "2022", "2022"],
            "journal_volume",
            id="test_volume",
        ),
        param(
            ["093B07", "093B09", "093B08"],
            "journal_artid",
            id="test_journal_artid",
        ),
        param(
            ["2022", "2022", "2022"],
            "journal_year",
            id="test_journal_year",
        ),
        param(
            [
                "© The Author(s) 2022. Published by Oxford University Press on behalf of the Physical Society of Japan.",
                "© The Author(s) 2022. Published by Oxford University Press on behalf of the Physical Society of Japan.",
                "© The Author(s) 2022. Published by Oxford University Press on behalf of the Physical Society of Japan.",
            ],
            "copyright_statement",
            id="test_copyright_statement",
        ),
        param(
            [2022, 2022, 2022],
            "copyright_year",
            id="test_copyright_year",
        ),
        param(
            [
                [
                    {
                        "license": "CC-BY-4.0",
                        "url": "https://creativecommons.org/licenses/by/4.0/",
                    }
                ],
                [
                    {
                        "license": "CC-BY-4.0",
                        "url": "https://creativecommons.org/licenses/by/4.0/",
                    }
                ],
                [
                    {
                        "license": "CC-BY-4.0",
                        "url": "https://creativecommons.org/licenses/by/4.0/",
                    }
                ],
            ],
            "license",
            id="test_license",
        ),
        param(
            [
                ["Progress of Theoretical and Experimental Physics"],
                ["Progress of Theoretical and Experimental Physics"],
                ["Progress of Theoretical and Experimental Physics"],
            ],
            "collections",
            id="test_collections",
        ),
    ],
)
def test_iop_articles_parsing(parsed_articles, expected, key):
    for (
        expected_value,
        article,
    ) in zip(expected, parsed_articles):
        assert key in article
        assert article[key] == expected_value
