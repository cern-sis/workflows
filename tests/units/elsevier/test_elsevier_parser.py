from os import listdir

from common.utils import parse_without_names_spaces
from elsevier.parser import ElsevierParser
from pytest import fixture, mark, param


@fixture(scope="module")
def parser():
    return ElsevierParser()


@fixture
def articles(shared_datadir):
    articles = []
    file_names = ["main2.xml", "main.xml"]
    for filename in file_names:
        with open(shared_datadir / filename) as file:
            articles.append(parse_without_names_spaces(file.read()))
    return articles


@fixture()
def parsed_articles(parser, articles):
    return [parser._publisher_specific_parsing(article) for article in articles]


@mark.parametrize(
    "expected, key",
    [
        param(
            [
                ["10.1016/j.physletb.2023.137730"],
                ["10.1016/j.physletb.2023.138173"],
            ],
            "dois",
            id="test_dois",
        ),
        param(
            [
                "We present the first systematic comparison of the charged-particle pseudorapidity densities for three widely different collision systems, pp, p <glyph name='sbnd' />Pb, and Pb <glyph name='sbnd' />Pb, at the top energy of the Large Hadron Collider ( <math altimg='si1.svg'><msqrt><mrow><msub><mrow><mi>s</mi></mrow><mrow><mi mathvariant='normal'>NN</mi></mrow></msub></mrow></msqrt><mo linebreak='goodbreak' linebreakstyle='after'>=</mo><mn>5.02</mn><mspace width='0.2em' /><mtext>TeV</mtext></math>) measured over a wide pseudorapidity range ( <math altimg='si3.svg'><mo linebreak='badbreak' linebreakstyle='after'>&#8722;</mo><mn>3.5</mn><mo linebreak='goodbreak' linebreakstyle='after'>&lt;</mo><mi>&#951;</mi><mo linebreak='goodbreak' linebreakstyle='after'>&lt;</mo><mn>5</mn></math>), the widest possible among the four experiments at that facility. The systematic uncertainties are minimised since the measurements are recorded by the same experimental apparatus (ALICE). The distributions for p <glyph name='sbnd' />Pb and Pb <glyph name='sbnd' />Pb collisions are determined as a function of the centrality of the collisions, while results from pp collisions are reported for inelastic events with at least one charged particle at midrapidity. The charged-particle pseudorapidity densities are, under simple and robust assumptions, transformed to charged-particle rapidity densities. This allows for the calculation and the presentation of the evolution of the width of the rapidity distributions and of a lower bound on the Bjorken energy density, as a function of the number of participants in all three collision systems. We find a decreasing width of the particle production, and roughly a smooth ten fold increase in the energy density, as the system size grows, which is consistent with a gradually higher dense phase of matter.",
                "One of the leading issues in quantum field theory and cosmology is the mismatch between the observed and calculated values for the cosmological constant in Einstein's field equations of up to 120 orders of magnitude. In this paper, we discuss new methods to potentially bridge this chasm using the generalized uncertainty principle (GUP). We find that if quantum gravity GUP models are the solution to this puzzle, then it may require the gravitationally modified position operator undergoes a parity transformation at high energies.",
            ],
            "abstract",
            id="test_abstract",
        ),
        param(
            [
                "System-size dependence of the charged-particle pseudorapidity density at  <math altimg='si1.svg'><msqrt><mrow><msub><mrow><mi>s</mi></mrow><mrow><mi mathvariant='normal'>NN</mi></mrow></msub></mrow></msqrt><mo linebreak='goodbreak' linebreakstyle='after'>=</mo><mn>5.02</mn><mspace width='0.2em' /><mtext>TeV</mtext></math> for pp, p <glyph name='sbnd' />Pb, and Pb <glyph name='sbnd' />Pb collisions",
                "Quantum gravity, the cosmological constant, and parity transformation",
            ],
            "title",
            id="test_tilte",
        ),
        param(
            [
                [
                    {
                        "surname": "Acharya",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Variable Energy Cyclotron Centre, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Variable Energy Cyclotron Centre",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Adamová",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Nuclear Physics Institute of the Czech Academy of Sciences, Řež u Prahy, Czech Republic",
                                "organization": "Nuclear Physics Institute of the Czech Academy of Sciences",
                                "country": "Czech Republic",
                            }
                        ],
                    },
                ],
                [
                    {
                        "surname": "Bishop",
                        "given_names": "Michael",
                        "affiliations": [
                            {
                                "value": "Mathematics Department, California State University Fresno, Fresno, CA 93740, USA",
                                "organization": "Mathematics Department",
                                "country": "USA",
                            }
                        ],
                        "email": "mibishop@mail.fresnostate.edu",
                    },
                    {
                        "surname": "Martin",
                        "given_names": "Peter",
                        "affiliations": [
                            {
                                "value": "Physics Department, California State University Fresno, Fresno, CA 93740, USA",
                                "organization": "Physics Department",
                                "country": "USA",
                            }
                        ],
                        "email": "kotor2@mail.fresnostate.edu",
                    },
                    {
                        "surname": "Singleton",
                        "given_names": "Douglas",
                        "affiliations": [
                            {
                                "value": "Physics Department, California State University Fresno, Fresno, CA 93740, USA",
                                "organization": "Physics Department",
                                "country": "USA",
                            },
                            {
                                "value": "Kavli Institute for Theoretical Physics, University of California Santa Barbara, Santa Barbara, CA 93106, USA",
                                "organization": "Kavli Institute for Theoretical Physics",
                                "country": "USA",
                            },
                        ],
                        "email": "dougs@mail.fresnostate.edu",
                    },
                ],
            ],
            "authors",
            id="test_authors",
        ),
        param(
            ["European Center of Nuclear Research, ALICE experiment", "The Author(s)"],
            "copyright_holder",
            id="test_copyright_holder",
        ),
        param(
            ["2023"],
            "copyright_year",
            id="test_copyright_year",
        ),
        param(
            ["European Center of Nuclear Research, ALICE experiment", "The Author(s)"],
            "copyright_statement",
            id="test_copyright_statement",
        ),
        param(
            ["137730", "138173"],
            "journal_artid",
            id="test_journal_artid",
        ),
    ],
)
def test_elsevier_parsing(parsed_articles, expected, key):
    for (expected_value, article) in zip(expected, parsed_articles):
        assert article[key] == expected_value
