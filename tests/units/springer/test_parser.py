import xml.etree.ElementTree as ET
from os import listdir

from common.enhancer import Enhancer
from pytest import fixture
from springer.parser import SpringerParser
from springer.springer_process_file import process_xml


@fixture(scope="module")
def parser():
    return SpringerParser()


@fixture
def articles(datadir):

    articles = []
    for filename in sorted(listdir(datadir)):
        with open(datadir / filename) as file:
            xml = process_xml(file.read())
            articles.append(ET.fromstring(xml))
    return articles


@fixture()
def parsed_articles(parser, articles):
    return [parser._publisher_specific_parsing(article) for article in articles]


def test_weird_titles(parsed_articles):
    parsed_titles = sorted([a.get("title") for a in parsed_articles])
    expected_results = sorted(
        [
            " $$(g-2)_{e,\\mu }$$ anomalies and decays $$h\\rightarrow e_a e_b$$ , "
            "$$Z\\rightarrow e_ae_b$$ , and $$e_b\\rightarrow e_a \\gamma $$ in a two "
            "Higgs doublet model with inverse seesaw neutrinos",
            " $$\\Lambda $$ polarization in very high energy heavy ion collisions as a probe of the quark–gluon plasma formation and properties",
            "A strategy for a general search for new phenomena using data-derived signal regions and its application within the ATLAS experiment",
            "Quasi-normal modes of slowly-rotating Johannsen black holes",
            "Revisiting the mechanical properties of the nucleon",
            "Symmetry breaking in quantum curves and super Chern-Simons matrix models",
        ]
    )

    assert expected_results == parsed_titles


def test_authors(parsed_articles):
    expected_results = (
        [
            {
                "affiliations": [
                    {
                        "organization": "Kyoto University",
                        "value": "Center for Gravitational Physics, Yukawa Institute for Theoretical Physics, "
                        "Kyoto University, Sakyo-ku, Kyoto, 606-8502, Japan",
                        "country": "Japan",
                    }
                ],
                "surname": "Kubo",
                "given_names": "Naotaka",
                "email": "naotaka.kubo@yukawa.kyoto-u.ac.jp",
            },
            {
                "affiliations": [
                    {
                        "organization": "Osaka City University",
                        "value": "Department of Physics, Graduate School of Science, Osaka City University, Sumiyoshi-ku, "
                        "Osaka, 558-8585, Japan",
                        "country": "Japan",
                    },
                    {
                        "organization": "Nambu Yoichiro Institute of Theoretical and Experimental Physics (NITEP)",
                        "value": "Nambu Yoichiro Institute of Theoretical and Experimental Physics (NITEP), Sumiyoshi-ku, "
                        "Osaka, 558-8585, Japan",
                        "country": "Japan",
                    },
                    {
                        "organization": "Osaka City University Advanced Mathematical Institute (OCAMI)",
                        "value": "Osaka City University Advanced Mathematical Institute (OCAMI), "
                        "Sumiyoshi-ku, Osaka, 558-8585, Japan",
                        "country": "Japan",
                    },
                ],
                "orcid": "my-test-orcid",
                "surname": "Moriyama",
                "given_names": "Sanefumi",
                "email": "moriyama@sci.osaka-cu.ac.jp",
            },
            {
                "affiliations": [
                    {
                        "organization": "School of Physics, Korea Institute for Advanced Study",
                        "value": "School of Physics, Korea Institute for Advanced Study, Dongdaemun-gu, Seoul, 02455, Korea",
                        "country": "Korea",
                    }
                ],
                "surname": "Nosaka",
                "given_names": "Tomoki",
                "email": "nosaka@yukawa.kyoto-u.ac.jp",
            },
        ],
        [
            {
                "affiliations": [
                    {
                        "organization": "Université Paris-Saclay",
                        "value": "Centre de Physique Théorique, École polytechnique, CNRS, "
                        "Université Paris-Saclay, Palaiseau, 91128, France",
                        "country": "France",
                    }
                ],
                "surname": "Lorcé",
                "given_names": "Cédric",
            },
            {
                "affiliations": [
                    {
                        "organization": "Université Paris-Saclay",
                        "value": "IRFU, CEA, Université Paris-Saclay, Gif-sur-Yvette, 91191, France",
                        "country": "France",
                    }
                ],
                "surname": "Moutarde",
                "given_names": "Hervé",
            },
            {
                "affiliations": [
                    {
                        "organization": "Université Paris-Saclay",
                        "value": "Centre de Physique Théorique, École polytechnique, CNRS, "
                        "Université Paris-Saclay, Palaiseau, 91128, France",
                        "country": "France",
                    },
                    {
                        "organization": "Université Paris-Saclay",
                        "value": "IRFU, CEA, Université Paris-Saclay, Gif-sur-Yvette, 91191, France",
                        "country": "France",
                    },
                ],
                "surname": "Trawiński",
                "given_names": "Arkadiusz",
                "email": "Arkadiusz.Trawinski@cea.fr",
            },
        ],
    )

    for authors, parsed_article in zip(expected_results, parsed_articles):
        assert authors == parsed_article["authors"]

        for author in authors:
            for aff in author.get("affiliations", []):
                if aff.get("country") == "Korea":
                    aff["country"] = "South Korea"

        assert Enhancer()("Springer", parsed_article)["authors"] == authors


def test_title(parsed_articles):
    titles = (
        "Symmetry breaking in quantum curves and super Chern-Simons matrix models",
        "Revisiting the mechanical properties of the nucleon",
        "A strategy for a general search for new phenomena using data-derived signal regions and its "
        "application within the ATLAS experiment",
    )
    for title, article in zip(titles, parsed_articles):
        assert "title" in article
        assert article["title"] == title


def test_date_published(parsed_articles):
    dates_published = ("2019-01-28", "2019-01-29", "2019-02-06")
    for date_published, article in zip(dates_published, parsed_articles):
        assert "date_published" in article
        assert article["date_published"] == date_published


def test_license(parsed_articles):
    expected_licenses = (
        [
            {
                "license": "CC-BY-3.0",
                "url": "https://creativecommons.org/licenses/by/3.0",
            }
        ],
        [
            {
                "license": "CC-BY-4.0",
                "url": "https://creativecommons.org/licenses/by/4.0",
            }
        ],
        [
            {
                "license": "CC-BY-4.0",
                "url": "https://creativecommons.org/licenses/by/4.0",
            }
        ],
    )
    for expected_license, article in zip(expected_licenses, parsed_articles):
        assert "license" in article
        assert article["license"] == expected_license


def test_dois(parsed_articles):
    dois = (
        "10.1007/JHEP01(2019)210",
        "10.1140/epjc/s10052-019-6572-3",
        "10.1140/epjc/s10052-019-6540-y",
    )
    for doi, article in zip(dois, parsed_articles):
        assert "dois" in article
        assert article["dois"] == [doi]


def test_collections(parsed_articles):
    collections = (
        ["Journal of High Energy Physics"],
        ["European Physical Journal C"],
        ["European Physical Journal C"],
    )
    for collection, article in zip(collections, parsed_articles):
        assert "collections" in article
        for coll in collection:
            assert coll in article["collections"]


def test_collaborations(parsed_articles):
    collaborations = ([], [], ["ATLAS Collaboration"])
    for collaboration, article in zip(collaborations, parsed_articles):
        if collaboration:
            assert "collaborations" in article
            assert article["collaborations"] == collaboration
        else:
            assert "collaborations" not in article


def test_publication_info(parsed_articles):
    expected_results = (
        dict(
            journal_title="Journal of High Energy Physics",
            journal_year=2019,
            journal_volume="2019",
            journal_issue="1",
            journal_fpage="1",
            journal_lpage="29",
            journal_artid="JHEP012019210",
        ),
        dict(
            journal_title="European Physical Journal C",
            journal_year=2019,
            journal_volume="79",
            journal_issue="1",
            journal_fpage="1",
            journal_lpage="25",
            journal_artid="s10052-019-6572-3",
        ),
        dict(
            journal_title="European Physical Journal C",
            journal_year=2019,
            journal_volume="79",
            journal_issue="2",
            journal_fpage="1",
            journal_lpage="45",
            journal_artid="s10052-019-6540-y",
        ),
    )
    for expected, article in zip(expected_results, parsed_articles):
        for k, v in expected.items():
            assert k in article
            assert article[k] == v


def test_page_nr(parsed_articles):
    expected_results = ([29], [25], [45])
    for expected, article in zip(expected_results, parsed_articles):
        assert "page_nr" in article
        assert article["page_nr"] == expected


def test_copyrights(parsed_articles):
    expected_results = (
        {"copyright_holder": "SISSA, Trieste, Italy", "copyright_year": 2019},
        {"copyright_holder": "The Author(s)", "copyright_year": 2019},
        {
            "copyright_holder": "CERN for the benefit of the ATLAS collaboration",
            "copyright_year": 2019,
        },
    )
    for expected, article in zip(expected_results, parsed_articles):
        for k, v in expected.items():
            assert k in article
            assert article[k] == v


def test_arxiv(parsed_articles):
    expected_results = (
        [dict(value="1811.06048")],
        [dict(value="1810.09837")],
        [dict(value="1807.07447v1")],
    )

    for expected, article in zip(expected_results, parsed_articles):
        assert "arxiv_eprints" in article
        assert article["arxiv_eprints"] == expected


def test_doctype(parsed_articles):
    expected_results = (
        "article",
        "article",
        "article",
    )

    for expected, article in zip(expected_results, parsed_articles):
        assert "journal_doctype" in article
        assert article["journal_doctype"] == expected


def test_abstract(parsed_articles):
    abstracts = (
        "It was known that quantum curves and super Chern-Simons matrix models correspond to each other. "
        "From the viewpoint of symmetry, the algebraic curve of genus one, called the del Pezzo curve, enjoys "
        "symmetry of the exceptional algebra, while the super Chern-Simons matrix model is described by the free "
        "energy of topological strings on the del Pezzo background with the symmetry broken. We study the symmetry "
        "breaking of the quantum cousin of the algebraic curve and reproduce the results in the super Chern-Simons matrix model.",
        "We discuss in detail the distributions of energy, radial pressure and tangential pressure inside the nucleon. "
        "In particular, this discussion is carried on in both the instant form and the front form of dynamics. Moreover "
        "we show for the first time how these mechanical concepts can be defined when the average nucleon momentum does "
        "not vanish. We express the conditions of hydrostatic equilibrium and stability in terms of these two and "
        "three-dimensional energy and pressure distributions. We briefly discuss the phenomenological relevance of our "
        "findings with a simple yet realistic model. In the light of this exhaustive mechanical description of the "
        "nucleon, we also present several possible connections between hadronic physics and compact stars, like e.g. "
        "the study of the equation of state for matter under extreme conditions and stability constraints.",
        "This paper describes a strategy for a general search used by the ATLAS Collaboration to find potential indications "
        "of new physics. Events are classified according to their final state into many event classes. For each event class "
        "an automated search algorithm tests whether the data are compatible with the Monte Carlo simulated expectation in s"
        "everal distributions sensitive to the effects of new physics. The significance of a deviation is quantified using "
        "pseudo-experiments. A data selection with a significant deviation defines a signal region for a dedicated follow-up "
        "analysis with an improved background expectation. The analysis of the data-derived signal regions on a new dataset "
        "allows a statistical interpretation without the large look-elsewhere effect. The sensitivity of the approach is "
        "discussed using Standard Model processes and benchmark signals of new physics. As an example, results are shown "
        "for 3.2 fb $$^{-1}$$ of proton–proton collision data at a centre-of-mass energy of 13 $$\\text {TeV}$$ collected with the ATLAS detector "
        "at the LHC in 2015, in which more than 700 event classes and more than $$10^5$$ regions have been analysed. No significant "
        "deviations are found and consequently no data-derived signal regions for a follow-up analysis have been defined.",
        "The detection of gravitational waves with ground-based laser interferometers has opened a new window to test and constrain"
        " General Relativity (GR) in the strong, dynamical, and non-linear regime. In this paper, we follow an agnostic approach and"
        " we study the quasi-normal modes of gravitational perturbations of Johannsen black holes under the assumptions of the validity"
        " of the Einstein Equations and of low values of the black hole spin parameter and deformation parameters. We find that the"
        " deformation parameter $$\\alpha _{13}$$ has a stronger impact on the quasi-normal modes than the other leading order deformation"
        " parameters ( $$\\alpha _{22}$$ , $$\\alpha _{52}$$ , and $$\\epsilon _{3}$$ ). We derive a fitting formula for the fundamental"
        " modes with $$l=2$$ and $$l=3$$ for the deformation parameter $$\\alpha _{13}$$ valid in the slow rotation approximation"
        " ( $$a_* < 0.4$$ ). Finally, we constrain $$\\alpha _{13}$$ from the event GW170104; within our analysis, we find that"
        " the data of GW170104 are consistent with the predictions of GR.",
        "The lepton flavor violating decays $$h\\rightarrow e_b^\\pm "
        "e_a^\\mp $$ , $$Z\\rightarrow e_b^\\pm e_a^\\mp $$ , and "
        "$$e_b\\rightarrow e_a \\gamma $$ will be discussed in the "
        "framework of the Two Higgs doublet model with presence of new "
        "inverse seesaw neutrinos and a singly charged Higgs boson that "
        "accommodate both $$1\\sigma $$ experimental data of $$(g-2)$$ "
        "anomalies of the muon and electron. Numerical results indicate "
        "that there exist regions of the parameter space supporting all "
        "experimental data of $$(g-2)_{e,\\mu }$$ as well as the "
        "promising LFV signals corresponding to the future experimental "
        "sensitivities.",
        None,
    )
    for abstract, article in zip(abstracts, parsed_articles):
        if abstract is None:
            assert "abstract" not in article
        else:
            assert article["abstract"] == abstract


@fixture
def article_with_orcid(parser, datadir):
    with open(datadir / "s10052-024-12692-y.xml") as file:
        yield parser._generic_parsing(
            parser._publisher_specific_parsing(ET.fromstring(file.read()))
        )


def test_article_with_cleaned_orcid(article_with_orcid):
    expected_output = [
        {
            "surname": "Hong",
            "given_names": "T.",
            "email": "tthong@agu.edu.vn",
            "affiliations": [
                {
                    "value": "An Giang University, Long Xuyen, 880000, Vietnam",
                    "organization": "An Giang University",
                    "country": "Vietnam",
                    "ror": "https://ror.org/023pm6532",
                },
                {
                    "value": "Vietnam National University, Ho Chi Minh City, 700000, Vietnam",
                    "organization": "Vietnam National University",
                    "country": "Vietnam",
                },
            ],
            "full_name": "Hong, T.",
        },
        {
            "surname": "Tran",
            "given_names": "Q.",
            "email": "tqduyet@agu.edu.vn",
            "affiliations": [
                {
                    "value": "An Giang University, Long Xuyen, 880000, Vietnam",
                    "organization": "An Giang University",
                    "country": "Vietnam",
                    "ror": "https://ror.org/023pm6532",
                },
                {
                    "value": "Vietnam National University, Ho Chi Minh City, 700000, Vietnam",
                    "organization": "Vietnam National University",
                    "country": "Vietnam",
                },
            ],
            "full_name": "Tran, Q.",
        },
        {
            "surname": "Nguyen",
            "given_names": "T.",
            "email": "thanhphong@ctu.edu.vn",
            "affiliations": [
                {
                    "value": "Department of Physics, Can Tho University, 3/2 Street, Can Tho, Vietnam",
                    "organization": "Can Tho University",
                    "country": "Vietnam",
                    "ror": "https://ror.org/0071qz696",
                }
            ],
            "full_name": "Nguyen, T.",
        },
        {
            "surname": "Hue",
            "given_names": "L.",
            "email": "lethohue@vlu.edu.vn",
            "affiliations": [
                {
                    "value": "Subatomic Physics Research Group, Science and Technology Advanced Institute, Van Lang University, Ho Chi Minh City, Vietnam",
                    "organization": "Van Lang University",
                    "country": "Vietnam",
                    "ror": "https://ror.org/02ryrf141",
                }
            ],
            "full_name": "Hue, L.",
        },
        {
            "orcid": "0009-0005-5993-6895",
            "surname": "Nha",
            "given_names": "N.",
            "email": "nguyenhuathanhnha@vlu.edu.vn",
            "affiliations": [
                {
                    "value": "Subatomic Physics Research Group, Science and Technology Advanced Institute, Van Lang University, Ho Chi Minh City, Vietnam",
                    "organization": "Van Lang University",
                    "country": "Vietnam",
                    "ror": "https://ror.org/02ryrf141",
                },
                {
                    "value": "Faculty of Applied Technology, School of Technology, Van Lang University, Ho Chi Minh City, Vietnam",
                    "organization": "Van Lang University",
                    "country": "Vietnam",
                    "ror": "https://ror.org/02ryrf141",
                },
            ],
            "full_name": "Nha, N.",
        },
    ]

    assert expected_output == article_with_orcid["authors"]
