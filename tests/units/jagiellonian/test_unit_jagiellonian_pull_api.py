from datetime import datetime, timezone
from unittest import mock

import pytest
from airflow.models import DagBag


@pytest.fixture(scope="class")
def dagbag():
    return DagBag(dag_folder="dags/", include_examples=False)


@pytest.mark.usefixtures("dagbag")
class TestUnitJagiellonianPullApi:
    def setup_method(self):
        self.dag_id = "jagiellonian_pull_api"
        self.execution_date = datetime.now(timezone.utc)

        self.dag = DagBag(dag_folder="dags/", include_examples=False).get_dag(
            self.dag_id
        )
        assert self.dag is not None, f"DAG {self.dag_id} failed to load"

    def test_filter_arxiv_category(self):
        crossref_data = [
            {
                "indexed": {
                    "date-parts": [[2022, 4, 5]],
                    "date-time": "2022-04-05T04:39:36Z",
                    "timestamp": 1649133576925,
                },
                "reference-count": 0,
                "publisher": "Jagiellonian University",
                "issue": "11",
                "content-domain": {"domain": [], "crossmark-restriction": False},
                "short-container-title": ["Acta Phys. Pol. B"],
                "published-print": {"date-parts": [[2011]]},
                "DOI": "10.5506/aphyspolb.42.2407",
                "type": "journal-article",
                "created": {
                    "date-parts": [[2011, 11, 18]],
                    "date-time": "2011-11-18T12:12:51Z",
                    "timestamp": 1321618371000,
                },
                "page": "2407",
                "source": "Crossref",
                "is-referenced-by-count": 0,
                "title": [""],
                "prefix": "10.5506",
                "volume": "42",
                "author": [
                    {
                        "given": "T.",
                        "family": "Gajdosik",
                        "sequence": "first",
                        "affiliation": [],
                    },
                    {
                        "given": "A.",
                        "family": "Juodagalvis",
                        "sequence": "additional",
                        "affiliation": [],
                    },
                    {
                        "given": "D.",
                        "family": "Jurčiukonis",
                        "sequence": "additional",
                        "affiliation": [],
                    },
                    {
                        "given": "T.",
                        "family": "Sabonis",
                        "sequence": "additional",
                        "affiliation": [],
                    },
                ],
                "member": "3462",
                "container-title": ["Acta Physica Polonica B"],
                "language": "en",
                "link": [
                    {
                        "URL": "https://www.actaphys.uj.edu.pl/fulltext?series=Reg&vol=42&page=2407",
                        "content-type": "unspecified",
                        "content-version": "vor",
                        "intended-application": "similarity-checking",
                    }
                ],
                "deposited": {
                    "date-parts": [[2019, 4, 30]],
                    "date-time": "2019-04-30T18:22:47Z",
                    "timestamp": 1556648567000,
                },
                "score": 0.0,
                "resource": {
                    "primary": {
                        "URL": "http://www.actaphys.uj.edu.pl/vol42/abs/v42p2407"
                    }
                },
                "issued": {"date-parts": [[2011]]},
                "references-count": 0,
                "journal-issue": {
                    "issue": "11",
                    "published-print": {"date-parts": [[2011]]},
                },
                "URL": "https://doi.org/10.5506/aphyspolb.42.2407",
                "ISSN": ["0587-4254", "1509-5770"],
                "issn-type": [
                    {"value": "0587-4254", "type": "print"},
                    {"value": "1509-5770", "type": "electronic"},
                ],
                "published": {"date-parts": [[2011]]},
            },
            {
                "indexed": {
                    "date-parts": [[2025, 4, 24]],
                    "date-time": "2025-04-24T08:40:05Z",
                    "timestamp": 1745484005007,
                    "version": "3.40.4",
                },
                "reference-count": 0,
                "publisher": "Jagiellonian University",
                "issue": "3",
                "license": [
                    {
                        "start": {
                            "date-parts": [[2025, 4, 16]],
                            "date-time": "2025-04-16T00:00:00Z",
                            "timestamp": 1744761600000,
                        },
                        "content-version": "vor",
                        "delay-in-days": 0,
                        "URL": "https://creativecommons.org/licenses/by/4.0/",
                    }
                ],
                "content-domain": {"domain": [], "crossmark-restriction": False},
                "short-container-title": ["Acta Phys. Pol. B"],
                "accepted": {"date-parts": [[2025, 1, 27]]},
                "abstract": "<jats:p>The interpretation of the energy-momentum tensor form factor \\(D(t)\\) of hadrons in terms of pressure and shear force distributions is discussed, concerns raised in the literature are reviewed, and ways to reconcile the concerns with the interpretation are indicated.</jats:p>\n          <jats:sec>\n            <jats:title>Abstract</jats:title>\n            <jats:supplementary-material>\n              <jats:permissions>\n                <jats:copyright-statement>Published by the Jagiellonian University</jats:copyright-statement>\n                <jats:copyright-year>2025</jats:copyright-year>\n                <jats:copyright-holder>authors</jats:copyright-holder>\n              </jats:permissions>\n            </jats:supplementary-material>\n          </jats:sec>",
                "DOI": "10.5506/aphyspolb.56.3-a17",
                "type": "journal-article",
                "created": {
                    "date-parts": [[2025, 4, 16]],
                    "date-time": "2025-04-16T13:02:16Z",
                    "timestamp": 1744808536000,
                },
                "page": "1",
                "update-policy": "https://doi.org/10.5506/crossmark-policy",
                "source": "Crossref",
                "is-referenced-by-count": 0,
                "title": [
                    "Pressure Inside Hadrons: Criticism, Conjectures, and All That"
                ],
                "prefix": "10.5506",
                "volume": "56",
                "author": [
                    {
                        "ORCID": "https://orcid.org/0000-0002-7091-2377",
                        "authenticated-orcid": False,
                        "given": "C.",
                        "family": "Lorcé",
                        "sequence": "first",
                        "affiliation": [
                            {
                                "id": [
                                    {
                                        "id": "https://ror.org/042tfbd02",
                                        "id-type": "ROR",
                                        "asserted-by": "publisher",
                                    }
                                ],
                                "name": "CPHT, CNRS, École polytechnique, Institut Polytechnique de Paris",
                            }
                        ],
                    },
                    {
                        "ORCID": "https://orcid.org/0000-0002-9985-0448",
                        "authenticated-orcid": False,
                        "given": "P.",
                        "family": "Schweitzer",
                        "sequence": "additional",
                        "affiliation": [
                            {
                                "id": [
                                    {
                                        "id": "https://ror.org/02der9h97",
                                        "id-type": "ROR",
                                        "asserted-by": "publisher",
                                    }
                                ],
                                "name": "Department of Physics, University of Connecticut",
                            }
                        ],
                    },
                ],
                "member": "3462",
                "published-online": {"date-parts": [[2025, 4, 16]]},
                "container-title": ["Acta Physica Polonica B"],
                "language": "en",
                "link": [
                    {
                        "URL": "https://www.actaphys.uj.edu.pl/findarticle?series=Reg&vol=56&aid=3-A17",
                        "content-type": "unspecified",
                        "content-version": "vor",
                        "intended-application": "similarity-checking",
                    }
                ],
                "deposited": {
                    "date-parts": [[2025, 4, 24]],
                    "date-time": "2025-04-24T08:25:37Z",
                    "timestamp": 1745483137000,
                },
                "score": 0.0,
                "resource": {
                    "primary": {
                        "URL": "https://www.actaphys.uj.edu.pl/findarticle?series=Reg&vol=56&aid=3-A17"
                    }
                },
                "issued": {"date-parts": [[2025, 4, 16]]},
                "references-count": 0,
                "journal-issue": {
                    "issue": "3",
                    "published-online": {"date-parts": [[2025, 3]]},
                },
                "URL": "https://doi.org/10.5506/aphyspolb.56.3-a17",
                "relation": {
                    "has-preprint": [
                        {
                            "id-type": "arxiv",
                            "id": "2501.04622",
                            "asserted-by": "subject",
                        }
                    ]
                },
                "ISSN": ["0587-4254", "1509-5770"],
                "issn-type": [
                    {"type": "print", "value": "0587-4254"},
                    {"type": "electronic", "value": "1509-5770"},
                ],
                "published": {"date-parts": [[2025, 4, 16]]},
                "assertion": [
                    {
                        "value": "2024-12-31",
                        "name": "date_received",
                        "label": "Date Received",
                        "group": {
                            "name": "publication_dates",
                            "label": "Publication dates",
                        },
                    },
                    {
                        "value": "2025 The authors",
                        "name": "copyright_statement",
                        "label": "Copyright statement",
                        "group": {"name": "copyright", "label": "copyright"},
                    },
                    {
                        "value": "The authors",
                        "name": "copyright_holder",
                        "label": "Copyright holder",
                        "group": {"name": "copyright", "label": "copyright"},
                    },
                    {
                        "value": "2025",
                        "name": "copyright_year",
                        "label": "Copyright year",
                        "group": {"name": "copyright", "label": "copyright"},
                    },
                    {
                        "value": "hep-ph",
                        "name": "arxiv_main_category",
                        "label": "arXiv main category",
                        "group": {"name": "arXiv", "label": "arXiv"},
                    },
                    {
                        "value": "https://www.actaphys.uj.edu.pl/fulltext?series=Reg&vol=56&aid=3-A17",
                        "name": "full_text_link_pdf",
                        "label": "full text link pdf",
                        "group": {"name": "full_text", "label": "full text"},
                    },
                    {
                        "value": "https://www.actaphys.uj.edu.pl/fulltext?series=Reg&vol=56&aid=3-A17&fmt=pdfa",
                        "name": "full_text_link_pdfa",
                        "label": "full text link pdfa",
                        "group": {"name": "full_text", "label": "full text"},
                    },
                ],
                "article-number": "3-A17",
            },
        ]

        task = self.dag.get_task("jagiellonian_filter_arxiv_category")
        function_to_unit_test = task.python_callable

        result = function_to_unit_test(crossref_data)

        expected = [
            {
                "indexed": {
                    "date-parts": [[2025, 4, 24]],
                    "date-time": "2025-04-24T08:40:05Z",
                    "timestamp": 1745484005007,
                    "version": "3.40.4",
                },
                "reference-count": 0,
                "publisher": "Jagiellonian University",
                "issue": "3",
                "license": [
                    {
                        "start": {
                            "date-parts": [[2025, 4, 16]],
                            "date-time": "2025-04-16T00:00:00Z",
                            "timestamp": 1744761600000,
                        },
                        "content-version": "vor",
                        "delay-in-days": 0,
                        "URL": "https://creativecommons.org/licenses/by/4.0/",
                    }
                ],
                "content-domain": {"domain": [], "crossmark-restriction": False},
                "short-container-title": ["Acta Phys. Pol. B"],
                "accepted": {"date-parts": [[2025, 1, 27]]},
                "abstract": "<jats:p>The interpretation of the energy-momentum tensor form factor \\(D(t)\\) of hadrons in terms of pressure and shear force distributions is discussed, concerns raised in the literature are reviewed, and ways to reconcile the concerns with the interpretation are indicated.</jats:p>\n          <jats:sec>\n            <jats:title>Abstract</jats:title>\n            <jats:supplementary-material>\n              <jats:permissions>\n                <jats:copyright-statement>Published by the Jagiellonian University</jats:copyright-statement>\n                <jats:copyright-year>2025</jats:copyright-year>\n                <jats:copyright-holder>authors</jats:copyright-holder>\n              </jats:permissions>\n            </jats:supplementary-material>\n          </jats:sec>",
                "DOI": "10.5506/aphyspolb.56.3-a17",
                "type": "journal-article",
                "created": {
                    "date-parts": [[2025, 4, 16]],
                    "date-time": "2025-04-16T13:02:16Z",
                    "timestamp": 1744808536000,
                },
                "page": "1",
                "update-policy": "https://doi.org/10.5506/crossmark-policy",
                "source": "Crossref",
                "is-referenced-by-count": 0,
                "title": [
                    "Pressure Inside Hadrons: Criticism, Conjectures, and All That"
                ],
                "prefix": "10.5506",
                "volume": "56",
                "author": [
                    {
                        "ORCID": "https://orcid.org/0000-0002-7091-2377",
                        "authenticated-orcid": False,
                        "given": "C.",
                        "family": "Lorcé",
                        "sequence": "first",
                        "affiliation": [
                            {
                                "id": [
                                    {
                                        "id": "https://ror.org/042tfbd02",
                                        "id-type": "ROR",
                                        "asserted-by": "publisher",
                                    }
                                ],
                                "name": "CPHT, CNRS, École polytechnique, Institut Polytechnique de Paris",
                            }
                        ],
                    },
                    {
                        "ORCID": "https://orcid.org/0000-0002-9985-0448",
                        "authenticated-orcid": False,
                        "given": "P.",
                        "family": "Schweitzer",
                        "sequence": "additional",
                        "affiliation": [
                            {
                                "id": [
                                    {
                                        "id": "https://ror.org/02der9h97",
                                        "id-type": "ROR",
                                        "asserted-by": "publisher",
                                    }
                                ],
                                "name": "Department of Physics, University of Connecticut",
                            }
                        ],
                    },
                ],
                "member": "3462",
                "published-online": {"date-parts": [[2025, 4, 16]]},
                "container-title": ["Acta Physica Polonica B"],
                "language": "en",
                "link": [
                    {
                        "URL": "https://www.actaphys.uj.edu.pl/findarticle?series=Reg&vol=56&aid=3-A17",
                        "content-type": "unspecified",
                        "content-version": "vor",
                        "intended-application": "similarity-checking",
                    }
                ],
                "deposited": {
                    "date-parts": [[2025, 4, 24]],
                    "date-time": "2025-04-24T08:25:37Z",
                    "timestamp": 1745483137000,
                },
                "score": 0.0,
                "resource": {
                    "primary": {
                        "URL": "https://www.actaphys.uj.edu.pl/findarticle?series=Reg&vol=56&aid=3-A17"
                    }
                },
                "issued": {"date-parts": [[2025, 4, 16]]},
                "references-count": 0,
                "journal-issue": {
                    "issue": "3",
                    "published-online": {"date-parts": [[2025, 3]]},
                },
                "URL": "https://doi.org/10.5506/aphyspolb.56.3-a17",
                "relation": {
                    "has-preprint": [
                        {
                            "id-type": "arxiv",
                            "id": "2501.04622",
                            "asserted-by": "subject",
                        }
                    ]
                },
                "ISSN": ["0587-4254", "1509-5770"],
                "issn-type": [
                    {"type": "print", "value": "0587-4254"},
                    {"type": "electronic", "value": "1509-5770"},
                ],
                "published": {"date-parts": [[2025, 4, 16]]},
                "assertion": [
                    {
                        "value": "2024-12-31",
                        "name": "date_received",
                        "label": "Date Received",
                        "group": {
                            "name": "publication_dates",
                            "label": "Publication dates",
                        },
                    },
                    {
                        "value": "2025 The authors",
                        "name": "copyright_statement",
                        "label": "Copyright statement",
                        "group": {"name": "copyright", "label": "copyright"},
                    },
                    {
                        "value": "The authors",
                        "name": "copyright_holder",
                        "label": "Copyright holder",
                        "group": {"name": "copyright", "label": "copyright"},
                    },
                    {
                        "value": "2025",
                        "name": "copyright_year",
                        "label": "Copyright year",
                        "group": {"name": "copyright", "label": "copyright"},
                    },
                    {
                        "value": "hep-ph",
                        "name": "arxiv_main_category",
                        "label": "arXiv main category",
                        "group": {"name": "arXiv", "label": "arXiv"},
                    },
                    {
                        "value": "https://www.actaphys.uj.edu.pl/fulltext?series=Reg&vol=56&aid=3-A17",
                        "name": "full_text_link_pdf",
                        "label": "full text link pdf",
                        "group": {"name": "full_text", "label": "full text"},
                    },
                    {
                        "value": "https://www.actaphys.uj.edu.pl/fulltext?series=Reg&vol=56&aid=3-A17&fmt=pdfa",
                        "name": "full_text_link_pdfa",
                        "label": "full text link pdfa",
                        "group": {"name": "full_text", "label": "full text"},
                    },
                ],
                "article-number": "3-A17",
            }
        ]

        assert result == expected

    @mock.patch("airflow.api.common.trigger_dag.trigger_dag")
    def test_trigger_file_processing(self, mock_trigger_dag):

        sample_data = [
            {"DOI": "10.5506/aphyspolb.56.3-a17", "title": ["Article 1"]},
            {"DOI": "10.5506/aphyspolb.56.3-a18", "title": ["Article 2"]},
        ]

        task = self.dag.get_task("jagiellonian_trigger_file_processing")
        function_to_unit_test = task.python_callable

        function_to_unit_test(sample_data)

        assert mock_trigger_dag.call_count == 2
