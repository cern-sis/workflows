import json
from io import BytesIO

from common.enhancer import Enhancer
from common.utils import parse_without_names_spaces
from elsevier.parser import ElsevierParser
from pytest import fixture, mark, param


@fixture(scope="module")
def parser():
    return ElsevierParser()


@fixture
def articles(shared_datadir):
    articles = []
    file_names = [
        "main2.xml",
        "main.xml",
        "main_rjjlr.xml",
        "j.physletb.2023.138109.xml",
        "main_simple_head.xml",
        "main-3.xml",
    ]
    for filename in file_names:
        with open(shared_datadir / filename, "rb") as file:
            xml_content_bytes = BytesIO(file.read())
            xml = parse_without_names_spaces(xml_content_bytes)
            articles.append(xml)
    return articles


@fixture()
def parsed_articles(parser, articles):
    return [parser._publisher_specific_parsing(article) for article in articles]


@fixture()
def enhanced_articles(parser, parsed_articles):
    return [
        Enhancer()("Elsevier", parser._publisher_specific_parsing(article))
        for article in parsed_articles
    ]


@mark.parametrize(
    "expected, key",
    [
        param(
            [
                ["10.1016/j.physletb.2023.137730"],
                ["10.1016/j.physletb.2023.138173"],
                ["10.1016/j.physletb.2022.137649"],
                ["10.1016/j.physletb.2023.138109"],
                ["10.1016/j.physletb.2025.139258"],
                ["10.1016/j.physletb.2025.139355"],
            ],
            "dois",
            id="test_dois",
        ),
        param(
            [
                "We present the first systematic comparison of the charged-particle pseudorapidity densities for three widely different collision systems, pp, p <glyph name='sbnd' />Pb, and Pb <glyph name='sbnd' />Pb, at the top energy of the Large Hadron Collider ( <math altimg='si1.svg'><msqrt><mrow><msub><mrow><mi>s</mi></mrow><mrow><mi mathvariant='normal'>NN</mi></mrow></msub></mrow></msqrt><mo linebreak='goodbreak' linebreakstyle='after'>=</mo><mn>5.02</mn><mspace width='0.2em' /><mtext>TeV</mtext></math>) measured over a wide pseudorapidity range ( <math altimg='si3.svg'><mo linebreak='badbreak' linebreakstyle='after'>&#8722;</mo><mn>3.5</mn><mo linebreak='goodbreak' linebreakstyle='after'>&lt;</mo><mi>&#951;</mi><mo linebreak='goodbreak' linebreakstyle='after'>&lt;</mo><mn>5</mn></math>), the widest possible among the four experiments at that facility. The systematic uncertainties are minimised since the measurements are recorded by the same experimental apparatus (ALICE). The distributions for p <glyph name='sbnd' />Pb and Pb <glyph name='sbnd' />Pb collisions are determined as a function of the centrality of the collisions, while results from pp collisions are reported for inelastic events with at least one charged particle at midrapidity. The charged-particle pseudorapidity densities are, under simple and robust assumptions, transformed to charged-particle rapidity densities. This allows for the calculation and the presentation of the evolution of the width of the rapidity distributions and of a lower bound on the Bjorken energy density, as a function of the number of participants in all three collision systems. We find a decreasing width of the particle production, and roughly a smooth ten fold increase in the energy density, as the system size grows, which is consistent with a gradually higher dense phase of matter.",
                "One of the leading issues in quantum field theory and cosmology is the mismatch between the observed and calculated values for the cosmological constant in Einstein's field equations of up to 120 orders of magnitude. In this paper, we discuss new methods to potentially bridge this chasm using the generalized uncertainty principle (GUP). We find that if quantum gravity GUP models are the solution to this puzzle, then it may require the gravitationally modified position operator undergoes a parity transformation at high energies.",
                "This letter reports measurements which characterize the underlying event associated with hard scatterings at mid-pseudorapidity ( <math altimg='si2.svg'><mo stretchy='false'>|</mo><mi>&#951;</mi><mo stretchy='false'>|</mo><mo linebreak='goodbreak' linebreakstyle='after'>&lt;</mo><mn>0.8</mn></math>) in pp, p&#8211;Pb and Pb&#8211;Pb collisions at centre-of-mass energy per nucleon pair,  <math altimg='si1.svg'><msqrt><mrow><msub><mrow><mi>s</mi></mrow><mrow><mi mathvariant='normal'>NN</mi></mrow></msub></mrow></msqrt><mo linebreak='goodbreak' linebreakstyle='after'>=</mo><mn>5.02</mn></math> <hsp sp='0.20' />TeV. The measurements are performed with ALICE at the LHC. Different multiplicity classes are defined based on the event activity measured at forward rapidities. The hard scatterings are identified by the leading particle defined as the charged particle with the largest transverse momentum ( <math altimg='si3.svg'><msub><mrow><mi>p</mi></mrow><mrow><mi mathvariant='normal'>T</mi></mrow></msub></math>) in the collision and having 8  <math altimg='si4.svg'><mo linebreak='badbreak' linebreakstyle='after'>&lt;</mo><msub><mrow><mi>p</mi></mrow><mrow><mi mathvariant='normal'>T</mi></mrow></msub><mo linebreak='goodbreak' linebreakstyle='after'>&lt;</mo><mn>15</mn></math> <hsp sp='0.20' />GeV/ <italic>c</italic>. The  <math altimg='si3.svg'><msub><mrow><mi>p</mi></mrow><mrow><mi mathvariant='normal'>T</mi></mrow></msub></math> spectra of associated particles (0.5  <math altimg='si5.svg'><mo>&#8804;</mo><msub><mrow><mi>p</mi></mrow><mrow><mi mathvariant='normal'>T</mi></mrow></msub><mo linebreak='goodbreak' linebreakstyle='after'>&lt;</mo><mn>6</mn></math> <hsp sp='0.20' />GeV/ <italic>c</italic>) are measured in different azimuthal regions defined with respect to the leading particle direction: toward, transverse, and away. The associated charged particle yields in the transverse region are subtracted from those of the away and toward regions. The remaining jet-like yields are reported as a function of the multiplicity measured in the transverse region. The measurements show a suppression of the jet-like yield in the away region and an enhancement of high- <math altimg='si3.svg'><msub><mrow><mi>p</mi></mrow><mrow><mi mathvariant='normal'>T</mi></mrow></msub></math> associated particles in the toward region in central Pb&#8211;Pb collisions, as compared to minimum-bias pp collisions. These observations are consistent with previous measurements that used two-particle correlations, and with an interpretation in terms of parton energy loss in a high-density quark gluon plasma. These yield modifications vanish in peripheral Pb&#8211;Pb collisions and are not observed in either high-multiplicity pp or p&#8211;Pb collisions.",
                "We investigate the stability of the electroweak vacuum in metric-affine gravity in which the Standard Model Higgs boson can be non-minimally coupled to both the Ricci scalar and the Holst invariant. We find that vacuum stability is improved in this framework across a wide range of model parameters.",
            ],
            "abstract",
            id="test_abstract",
        ),
        param(
            [
                "System-size dependence of the charged-particle pseudorapidity density at  <math altimg='si1.svg'><msqrt><mrow><msub><mrow><mi>s</mi></mrow><mrow><mi mathvariant='normal'>NN</mi></mrow></msub></mrow></msqrt><mo linebreak='goodbreak' linebreakstyle='after'>=</mo><mn>5.02</mn><mspace width='0.2em' /><mtext>TeV</mtext></math> for pp, p <glyph name='sbnd' />Pb, and Pb <glyph name='sbnd' />Pb collisions",
                "Quantum gravity, the cosmological constant, and parity transformation",
                "Study of charged particle production at high  <italic>p</italic> <inf>T</inf> using event topology in pp, p&#8211;Pb and Pb&#8211;Pb collisions at  <math altimg='si1.svg'><msqrt><mrow><msub><mrow><mi>s</mi></mrow><mrow><mi mathvariant='normal'>NN</mi></mrow></msub></mrow></msqrt><mo linebreak='goodbreak' linebreakstyle='after'>=</mo><mn>5.02</mn></math> <hsp sp='0.20' />TeV",
                "Electroweak vacuum decay in metric-affine gravity",
                "Corrigendum to “A potential approach to the  <italic>X</italic>(3872) thermal behavior&#8221; [Phys. Lett. B 854 (2024) 138760]",
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
                [
                    {
                        "surname": "Acharya",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Université Clermont Auvergne, CNRS/IN2P3, LPC, Clermont-Ferrand, France",
                                "organization": "Université Clermont Auvergne",
                                "country": "France",
                            },
                            {
                                "value": "Variable Energy Cyclotron Centre, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Variable Energy Cyclotron Centre",
                                "country": "India",
                            },
                        ],
                        "orcid": "0000-0002-9213-5329",
                    },
                    {
                        "surname": "Adamová",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Nuclear Physics Institute of the Czech Academy of Sciences, Husinec-Řež, Czech Republic",
                                "organization": "Nuclear Physics Institute of the Czech Academy of Sciences",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0002-0504-7428",
                    },
                    {
                        "surname": "Adler",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Johann-Wolfgang-Goethe Universität Frankfurt Institut für Informatik, Fachbereich Informatik und Mathematik, Frankfurt, Germany",
                                "organization": "Johann-Wolfgang-Goethe Universität Frankfurt Institut für Informatik",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Aglieri Rinella",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-9611-3696",
                    },
                    {
                        "surname": "Agnello",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Dipartimento DISAT del Politecnico and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento DISAT del Politecnico",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-0760-5075",
                    },
                    {
                        "surname": "Agrawal",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bologna, Bologna, Italy",
                                "organization": "INFN, Sezione di Bologna",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-0348-9836",
                    },
                    {
                        "surname": "Ahammed",
                        "given_names": "Z.",
                        "affiliations": [
                            {
                                "value": "Variable Energy Cyclotron Centre, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Variable Energy Cyclotron Centre",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0001-5241-7412",
                    },
                    {
                        "surname": "Ahmad",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Aligarh Muslim University, Aligarh, India",
                                "organization": "Department of Physics",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0003-0497-5705",
                    },
                    {
                        "surname": "Ahn",
                        "given_names": "S.U.",
                        "affiliations": [
                            {
                                "value": "Korea Institute of Science and Technology Information, Daejeon, Republic of Korea",
                                "organization": "Korea Institute of Science and Technology Information",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0001-8847-489X",
                    },
                    {
                        "surname": "Ahuja",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Faculty of Science, P.J. Šafárik University, Košice, Slovak Republic",
                                "organization": "Faculty of Science",
                                "country": "Slovak Republic",
                            }
                        ],
                        "orcid": "0000-0002-4417-1392",
                    },
                    {
                        "surname": "Akindinov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-7388-3022",
                    },
                    {
                        "surname": "Al-Turany",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-8071-4497",
                    },
                    {
                        "surname": "Aleksandrov",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-9719-7035",
                    },
                    {
                        "surname": "Alessandro",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Torino, Turin, Italy",
                                "organization": "INFN, Sezione di Torino",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-9680-4940",
                    },
                    {
                        "surname": "Alfanda",
                        "given_names": "H.M.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0002-5659-2119",
                    },
                    {
                        "surname": "Alfaro Molina",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Instituto de Física, Universidad Nacional Autónoma de México, Mexico City, Mexico",
                                "organization": "Instituto de Física",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0000-0002-4713-7069",
                    },
                    {
                        "surname": "Ali",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Aligarh Muslim University, Aligarh, India",
                                "organization": "Department of Physics",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-0877-7979",
                    },
                    {
                        "surname": "Ali",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "COMSATS University Islamabad, Islamabad, Pakistan",
                                "organization": "COMSATS University Islamabad",
                                "country": "Pakistan",
                            }
                        ],
                    },
                    {
                        "surname": "Alici",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Bologna, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-3618-4617",
                    },
                    {
                        "surname": "Alizadehvandchali",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "University of Houston, Houston, TX, United States",
                                "organization": "University of Houston",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0009-0000-7365-1064",
                    },
                    {
                        "surname": "Alkin",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-2205-5761",
                    },
                    {
                        "surname": "Alme",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Department of Physics and Technology, University of Bergen, Bergen, Norway",
                                "organization": "Department of Physics and Technology",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0000-0003-0177-0536",
                    },
                    {
                        "surname": "Alocco",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Cagliari, Cagliari, Italy",
                                "organization": "INFN, Sezione di Cagliari",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-8910-9173",
                    },
                    {
                        "surname": "Alt",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0005-4862-5370",
                    },
                    {
                        "surname": "Altsybeev",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-8079-7026",
                    },
                    {
                        "surname": "Anaam",
                        "given_names": "M.N.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0002-6180-4243",
                    },
                    {
                        "surname": "Andrei",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Horia Hulubei National Institute of Physics and Nuclear Engineering, Bucharest, Romania",
                                "organization": "Horia Hulubei National Institute of Physics and Nuclear Engineering",
                                "country": "Romania",
                            }
                        ],
                        "orcid": "0000-0001-8535-0680",
                    },
                    {
                        "surname": "Andronic",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Westfälische Wilhelms-Universität Münster, Institut für Kernphysik, Münster, Germany",
                                "organization": "Westfälische Wilhelms-Universität Münster",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-2372-6117",
                    },
                    {
                        "surname": "Anguelov",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0006-0236-2680",
                    },
                    {
                        "surname": "Antinori",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Padova, Padova, Italy",
                                "organization": "INFN, Sezione di Padova",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-7366-8891",
                    },
                    {
                        "surname": "Antonioli",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bologna, Bologna, Italy",
                                "organization": "INFN, Sezione di Bologna",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-7516-3726",
                    },
                    {
                        "surname": "Anuj",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Aligarh Muslim University, Aligarh, India",
                                "organization": "Department of Physics",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-2205-4419",
                    },
                    {
                        "surname": "Apadula",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Lawrence Berkeley National Laboratory, Berkeley, CA, United States",
                                "organization": "Lawrence Berkeley National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-5478-6120",
                    },
                    {
                        "surname": "Aphecetche",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "SUBATECH, IMT Atlantique, Nantes Université, CNRS-IN2P3, Nantes, France",
                                "organization": "SUBATECH",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0001-7662-3878",
                    },
                    {
                        "surname": "Appelshäuser",
                        "given_names": "H.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-0614-7671",
                    },
                    {
                        "surname": "Arcelli",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Bologna, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-6367-9215",
                    },
                    {
                        "surname": "Arnaldi",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Torino, Turin, Italy",
                                "organization": "INFN, Sezione di Torino",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-6698-9577",
                    },
                    {
                        "surname": "Arsene",
                        "given_names": "I.C.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, University of Oslo, Oslo, Norway",
                                "organization": "Department of Physics",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0000-0003-2316-9565",
                    },
                    {
                        "surname": "Arslandok",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Yale University, New Haven, CT, United States",
                                "organization": "Yale University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-3888-8303",
                    },
                    {
                        "surname": "Augustinus",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0009-0008-5460-6805",
                    },
                    {
                        "surname": "Averbeck",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-4277-4963",
                    },
                    {
                        "surname": "Aziz",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie, Orsay, France",
                                "organization": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-4333-8090",
                    },
                    {
                        "surname": "Azmi",
                        "given_names": "M.D.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Aligarh Muslim University, Aligarh, India",
                                "organization": "Department of Physics",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-2501-6856",
                    },
                    {
                        "surname": "Badalà",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Catania, Catania, Italy",
                                "organization": "INFN, Sezione di Catania",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-0569-4828",
                    },
                    {
                        "surname": "Baek",
                        "given_names": "Y.W.",
                        "affiliations": [
                            {
                                "value": "Gangneung-Wonju National University, Gangneung, Republic of Korea",
                                "organization": "Gangneung-Wonju National University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0002-4343-4883",
                    },
                    {
                        "surname": "Bai",
                        "given_names": "X.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0009-9085-079X",
                    },
                    {
                        "surname": "Bailhache",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-7987-4592",
                    },
                    {
                        "surname": "Bailung",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Indore, Indore, India",
                                "organization": "Indian Institute of Technology Indore",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0003-1172-0225",
                    },
                    {
                        "surname": "Bala",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Jammu, Jammu, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-4116-2861",
                    },
                    {
                        "surname": "Balbino",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Dipartimento DISAT del Politecnico and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento DISAT del Politecnico",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-0359-1403",
                    },
                    {
                        "surname": "Baldisseri",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA), IRFU, Départment de Physique Nucléaire (DPhN), Saclay, France",
                                "organization": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA)",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-6186-289X",
                    },
                    {
                        "surname": "Balis",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "AGH University of Science and Technology, Cracow, Poland",
                                "organization": "AGH University of Science and Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0002-3082-4209",
                    },
                    {
                        "surname": "Banerjee",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Bose Institute, Department of Physics and Centre for Astroparticle Physics and Space Science (CAPSS), Kolkata, India",
                                "organization": "Bose Institute",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0001-5743-7578",
                    },
                    {
                        "surname": "Banoo",
                        "given_names": "Z.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Jammu, Jammu, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-7178-3001",
                    },
                    {
                        "surname": "Barbera",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Catania, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-5971-6415",
                    },
                    {
                        "surname": "Barioglio",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-7328-9154",
                    },
                    {
                        "surname": "Barlou",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "National and Kapodistrian University of Athens, School of Science, Department of Physics , Athens, Greece",
                                "organization": "National and Kapodistrian University of Athens",
                                "country": "Greece",
                            }
                        ],
                    },
                    {
                        "surname": "Barnaföldi",
                        "given_names": "G.G.",
                        "affiliations": [
                            {
                                "value": "Wigner Research Centre for Physics, Budapest, Hungary",
                                "organization": "Wigner Research Centre for Physics",
                                "country": "Hungary",
                            }
                        ],
                        "orcid": "0000-0001-9223-6480",
                    },
                    {
                        "surname": "Barnby",
                        "given_names": "L.S.",
                        "affiliations": [
                            {
                                "value": "Nuclear Physics Group, STFC Daresbury Laboratory, Daresbury, United Kingdom",
                                "organization": "Nuclear Physics Group",
                                "country": "United Kingdom",
                            }
                        ],
                        "orcid": "0000-0001-7357-9904",
                    },
                    {
                        "surname": "Barret",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Université Clermont Auvergne, CNRS/IN2P3, LPC, Clermont-Ferrand, France",
                                "organization": "Université Clermont Auvergne",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0003-0611-9283",
                    },
                    {
                        "surname": "Barreto",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Universidade de São Paulo (USP), São Paulo, Brazil",
                                "organization": "Universidade de São Paulo (USP)",
                                "country": "Brazil",
                            }
                        ],
                        "orcid": "0000-0002-6454-0052",
                    },
                    {
                        "surname": "Bartels",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "University of Liverpool, Liverpool, United Kingdom",
                                "organization": "University of Liverpool",
                                "country": "United Kingdom",
                            }
                        ],
                        "orcid": "0009-0002-3371-4483",
                    },
                    {
                        "surname": "Barth",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0001-7633-1189",
                    },
                    {
                        "surname": "Bartsch",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0006-7928-4203",
                    },
                    {
                        "surname": "Baruffaldi",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Padova, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-7790-1152",
                    },
                    {
                        "surname": "Bastid",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Université Clermont Auvergne, CNRS/IN2P3, LPC, Clermont-Ferrand, France",
                                "organization": "Université Clermont Auvergne",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-6905-8345",
                    },
                    {
                        "surname": "Basu",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Lund University Department of Physics, Division of Particle Physics, Lund, Sweden",
                                "organization": "Lund University Department of Physics",
                                "country": "Sweden",
                            }
                        ],
                        "orcid": "0000-0003-0687-8124",
                    },
                    {
                        "surname": "Batigne",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "SUBATECH, IMT Atlantique, Nantes Université, CNRS-IN2P3, Nantes, France",
                                "organization": "SUBATECH",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0001-8638-6300",
                    },
                    {
                        "surname": "Battistini",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0000-0199-3372",
                    },
                    {
                        "surname": "Batyunya",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0009-0009-2974-6985",
                    },
                    {
                        "surname": "Bauri",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Bombay (IIT), Mumbai, India",
                                "organization": "Indian Institute of Technology Bombay (IIT)",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Bazo Alba",
                        "given_names": "J.L.",
                        "affiliations": [
                            {
                                "value": "Sección Física, Departamento de Ciencias, Pontificia Universidad Católica del Perú, Lima, Peru",
                                "organization": "Sección Física",
                                "country": "Peru",
                            }
                        ],
                        "orcid": "0000-0001-9148-9101",
                    },
                    {
                        "surname": "Bearden",
                        "given_names": "I.G.",
                        "affiliations": [
                            {
                                "value": "Niels Bohr Institute, University of Copenhagen, Copenhagen, Denmark",
                                "organization": "Niels Bohr Institute",
                                "country": "Denmark",
                            }
                        ],
                        "orcid": "0000-0003-2784-3094",
                    },
                    {
                        "surname": "Beattie",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Yale University, New Haven, CT, United States",
                                "organization": "Yale University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0001-7431-4051",
                    },
                    {
                        "surname": "Becht",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-7908-3288",
                    },
                    {
                        "surname": "Behera",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Indore, Indore, India",
                                "organization": "Indian Institute of Technology Indore",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-2599-7957",
                    },
                    {
                        "surname": "Belikov",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Université de Strasbourg, CNRS, IPHC UMR 7178, F-67000 Strasbourg, France",
                                "organization": "Université de Strasbourg",
                                "country": "France",
                            }
                        ],
                        "orcid": "0009-0005-5922-8936",
                    },
                    {
                        "surname": "Bell Hechavarria",
                        "given_names": "A.D.C.",
                        "affiliations": [
                            {
                                "value": "Westfälische Wilhelms-Universität Münster, Institut für Kernphysik, Münster, Germany",
                                "organization": "Westfälische Wilhelms-Universität Münster",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-0442-6549",
                    },
                    {
                        "surname": "Bellini",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Bologna, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-3498-4661",
                    },
                    {
                        "surname": "Bellwied",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "University of Houston, Houston, TX, United States",
                                "organization": "University of Houston",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-3156-0188",
                    },
                    {
                        "surname": "Belokurova",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-4862-3384",
                    },
                    {
                        "surname": "Belyaev",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0003-2843-9667",
                    },
                    {
                        "surname": "Bencedi",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Wigner Research Centre for Physics, Budapest, Hungary",
                                "organization": "Wigner Research Centre for Physics",
                                "country": "Hungary",
                            },
                            {
                                "value": "Instituto de Ciencias Nucleares, Universidad Nacional Autónoma de México, Mexico City, Mexico",
                                "organization": "Instituto de Ciencias Nucleares",
                                "country": "Mexico",
                            },
                        ],
                        "orcid": "0000-0002-9040-5292",
                    },
                    {
                        "surname": "Beole",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-4673-8038",
                    },
                    {
                        "surname": "Bercuci",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Horia Hulubei National Institute of Physics and Nuclear Engineering, Bucharest, Romania",
                                "organization": "Horia Hulubei National Institute of Physics and Nuclear Engineering",
                                "country": "Romania",
                            }
                        ],
                        "orcid": "0000-0002-4911-7766",
                    },
                    {
                        "surname": "Berdnikov",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0003-0309-5917",
                    },
                    {
                        "surname": "Berdnikova",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-3705-7898",
                    },
                    {
                        "surname": "Bergmann",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0004-5511-2496",
                    },
                    {
                        "surname": "Besoiu",
                        "given_names": "M.G.",
                        "affiliations": [
                            {
                                "value": "Institute of Space Science (ISS), Bucharest, Romania",
                                "organization": "Institute of Space Science (ISS)",
                                "country": "Romania",
                            }
                        ],
                        "orcid": "0000-0001-5253-2517",
                    },
                    {
                        "surname": "Betev",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-1373-1844",
                    },
                    {
                        "surname": "Bhaduri",
                        "given_names": "P.P.",
                        "affiliations": [
                            {
                                "value": "Variable Energy Cyclotron Centre, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Variable Energy Cyclotron Centre",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0001-7883-3190",
                    },
                    {
                        "surname": "Bhasin",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Jammu, Jammu, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-3687-8179",
                    },
                    {
                        "surname": "Bhat",
                        "given_names": "I.R.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Jammu, Jammu, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Bhat",
                        "given_names": "M.A.",
                        "affiliations": [
                            {
                                "value": "Bose Institute, Department of Physics and Centre for Astroparticle Physics and Space Science (CAPSS), Kolkata, India",
                                "organization": "Bose Institute",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-3643-1502",
                    },
                    {
                        "surname": "Bhattacharjee",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Gauhati University, Department of Physics, Guwahati, India",
                                "organization": "Gauhati University",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-3755-0992",
                    },
                    {
                        "surname": "Bianchi",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-1664-8189",
                    },
                    {
                        "surname": "Bianchi",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "INFN, Laboratori Nazionali di Frascati, Frascati, Italy",
                                "organization": "INFN, Laboratori Nazionali di Frascati",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-6861-2810",
                    },
                    {
                        "surname": "Bielčík",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Faculty of Nuclear Sciences and Physical Engineering, Czech Technical University in Prague, Prague, Czech Republic",
                                "organization": "Faculty of Nuclear Sciences and Physical Engineering",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0003-4940-2441",
                    },
                    {
                        "surname": "Bielčíková",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Nuclear Physics Institute of the Czech Academy of Sciences, Husinec-Řež, Czech Republic",
                                "organization": "Nuclear Physics Institute of the Czech Academy of Sciences",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0003-1659-0394",
                    },
                    {
                        "surname": "Biernat",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "The Henryk Niewodniczanski Institute of Nuclear Physics, Polish Academy of Sciences, Cracow, Poland",
                                "organization": "The Henryk Niewodniczanski Institute of Nuclear Physics",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0001-5613-7629",
                    },
                    {
                        "surname": "Bilandzic",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-0002-4654",
                    },
                    {
                        "surname": "Biro",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Wigner Research Centre for Physics, Budapest, Hungary",
                                "organization": "Wigner Research Centre for Physics",
                                "country": "Hungary",
                            }
                        ],
                        "orcid": "0000-0003-2849-0120",
                    },
                    {
                        "surname": "Biswas",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Bose Institute, Department of Physics and Centre for Astroparticle Physics and Space Science (CAPSS), Kolkata, India",
                                "organization": "Bose Institute",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0003-3578-5373",
                    },
                    {
                        "surname": "Blair",
                        "given_names": "J.T.",
                        "affiliations": [
                            {
                                "value": "The University of Texas at Austin, Austin, TX, United States",
                                "organization": "The University of Texas at Austin",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-4681-3002",
                    },
                    {
                        "surname": "Blau",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-4266-8338",
                    },
                    {
                        "surname": "Blidaru",
                        "given_names": "M.B.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-8085-8597",
                    },
                    {
                        "surname": "Bluhme",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Frankfurt Institute for Advanced Studies, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Frankfurt Institute for Advanced Studies",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Blume",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-6800-3465",
                    },
                    {
                        "surname": "Boca",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica, Università di Pavia, Pavia, Italy",
                                "organization": "Dipartimento di Fisica",
                                "country": "Italy",
                            },
                            {
                                "value": "INFN, Sezione di Pavia, Pavia, Italy",
                                "organization": "INFN, Sezione di Pavia",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0002-2829-5950",
                    },
                    {
                        "surname": "Bock",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Oak Ridge National Laboratory, Oak Ridge, TN, United States",
                                "organization": "Oak Ridge National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0003-4185-2093",
                    },
                    {
                        "surname": "Bodova",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Department of Physics and Technology, University of Bergen, Bergen, Norway",
                                "organization": "Department of Physics and Technology",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0009-0001-4479-0417",
                    },
                    {
                        "surname": "Bogdanov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                    },
                    {
                        "surname": "Boi",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Cagliari, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-5942-812X",
                    },
                    {
                        "surname": "Bok",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Inha University, Incheon, Republic of Korea",
                                "organization": "Inha University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0001-6283-2927",
                    },
                    {
                        "surname": "Boldizsár",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Wigner Research Centre for Physics, Budapest, Hungary",
                                "organization": "Wigner Research Centre for Physics",
                                "country": "Hungary",
                            }
                        ],
                        "orcid": "0009-0009-8669-3875",
                    },
                    {
                        "surname": "Bolozdynya",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-8224-4302",
                    },
                    {
                        "surname": "Bombara",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Faculty of Science, P.J. Šafárik University, Košice, Slovak Republic",
                                "organization": "Faculty of Science",
                                "country": "Slovak Republic",
                            }
                        ],
                        "orcid": "0000-0001-7333-224X",
                    },
                    {
                        "surname": "Bond",
                        "given_names": "P.M.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0009-0004-0514-1723",
                    },
                    {
                        "surname": "Bonomi",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Università di Brescia, Brescia, Italy",
                                "organization": "Università di Brescia",
                                "country": "Italy",
                            },
                            {
                                "value": "INFN, Sezione di Pavia, Pavia, Italy",
                                "organization": "INFN, Sezione di Pavia",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0003-1618-9648",
                    },
                    {
                        "surname": "Borel",
                        "given_names": "H.",
                        "affiliations": [
                            {
                                "value": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA), IRFU, Départment de Physique Nucléaire (DPhN), Saclay, France",
                                "organization": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA)",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0001-8879-6290",
                    },
                    {
                        "surname": "Borissov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0003-2881-9635",
                    },
                    {
                        "surname": "Bossi",
                        "given_names": "H.",
                        "affiliations": [
                            {
                                "value": "Yale University, New Haven, CT, United States",
                                "organization": "Yale University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0001-7602-6432",
                    },
                    {
                        "surname": "Botta",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-5054-1521",
                    },
                    {
                        "surname": "Bratrud",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-3069-5822",
                    },
                    {
                        "surname": "Braun-Munzinger",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-2527-0720",
                    },
                    {
                        "surname": "Bregant",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Universidade de São Paulo (USP), São Paulo, Brazil",
                                "organization": "Universidade de São Paulo (USP)",
                                "country": "Brazil",
                            }
                        ],
                        "orcid": "0000-0001-9610-5218",
                    },
                    {
                        "surname": "Broz",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Faculty of Nuclear Sciences and Physical Engineering, Czech Technical University in Prague, Prague, Czech Republic",
                                "organization": "Faculty of Nuclear Sciences and Physical Engineering",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0002-3075-1556",
                    },
                    {
                        "surname": "Bruno",
                        "given_names": "G.E.",
                        "affiliations": [
                            {
                                "value": "Politecnico di Bari and Sezione INFN, Bari, Italy",
                                "organization": "Politecnico di Bari",
                                "country": "Italy",
                            },
                            {
                                "value": "Dipartimento Interateneo di Fisica ‘M. Merlin’ and Sezione INFN, Bari, Italy",
                                "organization": "Dipartimento Interateneo di Fisica ‘M. Merlin’",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0001-6247-9633",
                    },
                    {
                        "surname": "Buckland",
                        "given_names": "M.D.",
                        "affiliations": [
                            {
                                "value": "University of Liverpool, Liverpool, United Kingdom",
                                "organization": "University of Liverpool",
                                "country": "United Kingdom",
                            }
                        ],
                        "orcid": "0009-0008-2547-0419",
                    },
                    {
                        "surname": "Budnikov",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0009-0009-7215-3122",
                    },
                    {
                        "surname": "Buesching",
                        "given_names": "H.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0009-4284-8943",
                    },
                    {
                        "surname": "Bufalino",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Dipartimento DISAT del Politecnico and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento DISAT del Politecnico",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-0413-9478",
                    },
                    {
                        "surname": "Bugnon",
                        "given_names": "O.",
                        "affiliations": [
                            {
                                "value": "SUBATECH, IMT Atlantique, Nantes Université, CNRS-IN2P3, Nantes, France",
                                "organization": "SUBATECH",
                                "country": "France",
                            }
                        ],
                    },
                    {
                        "surname": "Buhler",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Stefan Meyer Institut für Subatomare Physik (SMI), Vienna, Austria",
                                "organization": "Stefan Meyer Institut für Subatomare Physik (SMI)",
                                "country": "Austria",
                            }
                        ],
                        "orcid": "0000-0003-2049-1380",
                    },
                    {
                        "surname": "Buthelezi",
                        "given_names": "Z.",
                        "affiliations": [
                            {
                                "value": "iThemba LABS, National Research Foundation, Somerset West, South Africa",
                                "organization": "iThemba LABS",
                                "country": "South Africa",
                            },
                            {
                                "value": "University of the Witwatersrand, Johannesburg, South Africa",
                                "organization": "University of the Witwatersrand",
                                "country": "South Africa",
                            },
                        ],
                        "orcid": "0000-0002-8880-1608",
                    },
                    {
                        "surname": "Butt",
                        "given_names": "J.B.",
                        "affiliations": [
                            {
                                "value": "COMSATS University Islamabad, Islamabad, Pakistan",
                                "organization": "COMSATS University Islamabad",
                                "country": "Pakistan",
                            }
                        ],
                    },
                    {
                        "surname": "Bylinkin",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "University of Kansas, Lawrence, KS, United States",
                                "organization": "University of Kansas",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0001-6286-120X",
                    },
                    {
                        "surname": "Bysiak",
                        "given_names": "S.A.",
                        "affiliations": [
                            {
                                "value": "The Henryk Niewodniczanski Institute of Nuclear Physics, Polish Academy of Sciences, Cracow, Poland",
                                "organization": "The Henryk Niewodniczanski Institute of Nuclear Physics",
                                "country": "Poland",
                            }
                        ],
                    },
                    {
                        "surname": "Cai",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Padova, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            },
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            },
                        ],
                        "orcid": "0009-0001-3424-1553",
                    },
                    {
                        "surname": "Caines",
                        "given_names": "H.",
                        "affiliations": [
                            {
                                "value": "Yale University, New Haven, CT, United States",
                                "organization": "Yale University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-1595-411X",
                    },
                    {
                        "surname": "Caliva",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-2543-0336",
                    },
                    {
                        "surname": "Calvo Villar",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Sección Física, Departamento de Ciencias, Pontificia Universidad Católica del Perú, Lima, Peru",
                                "organization": "Sección Física",
                                "country": "Peru",
                            }
                        ],
                        "orcid": "0000-0002-5269-9779",
                    },
                    {
                        "surname": "Camacho",
                        "given_names": "J.M.M.",
                        "affiliations": [
                            {
                                "value": "Universidad Autónoma de Sinaloa, Culiacán, Mexico",
                                "organization": "Universidad Autónoma de Sinaloa",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0000-0001-5945-3424",
                    },
                    {
                        "surname": "Camacho",
                        "given_names": "R.S.",
                        "affiliations": [
                            {
                                "value": "High Energy Physics Group, Universidad Autónoma de Puebla, Puebla, Mexico",
                                "organization": "High Energy Physics Group",
                                "country": "Mexico",
                            }
                        ],
                    },
                    {
                        "surname": "Camerini",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Trieste, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-9261-9497",
                    },
                    {
                        "surname": "Canedo",
                        "given_names": "F.D.M.",
                        "affiliations": [
                            {
                                "value": "Universidade de São Paulo (USP), São Paulo, Brazil",
                                "organization": "Universidade de São Paulo (USP)",
                                "country": "Brazil",
                            }
                        ],
                        "orcid": "0000-0003-0604-2044",
                    },
                    {
                        "surname": "Carabas",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "University Politehnica of Bucharest, Bucharest, Romania",
                                "organization": "University Politehnica of Bucharest",
                                "country": "Romania",
                            }
                        ],
                        "orcid": "0000-0002-4008-9922",
                    },
                    {
                        "surname": "Carnesecchi",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0001-9981-7536",
                    },
                    {
                        "surname": "Caron",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Université de Lyon, CNRS/IN2P3, Institut de Physique des 2 Infinis de Lyon, Lyon, France",
                                "organization": "Université de Lyon",
                                "country": "France",
                            },
                            {
                                "value": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA), IRFU, Départment de Physique Nucléaire (DPhN), Saclay, France",
                                "organization": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA)",
                                "country": "France",
                            },
                        ],
                        "orcid": "0000-0001-7610-8673",
                    },
                    {
                        "surname": "Castillo Castellanos",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA), IRFU, Départment de Physique Nucléaire (DPhN), Saclay, France",
                                "organization": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA)",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-5187-2779",
                    },
                    {
                        "surname": "Catalano",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Dipartimento DISAT del Politecnico and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento DISAT del Politecnico",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-0722-7692",
                    },
                    {
                        "surname": "Ceballos Sanchez",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-0985-4155",
                    },
                    {
                        "surname": "Chakaberia",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Lawrence Berkeley National Laboratory, Berkeley, CA, United States",
                                "organization": "Lawrence Berkeley National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-9614-4046",
                    },
                    {
                        "surname": "Chakraborty",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Bombay (IIT), Mumbai, India",
                                "organization": "Indian Institute of Technology Bombay (IIT)",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-3311-1175",
                    },
                    {
                        "surname": "Chandra",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Variable Energy Cyclotron Centre, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Variable Energy Cyclotron Centre",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0003-4238-2302",
                    },
                    {
                        "surname": "Chapeland",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0003-4511-4784",
                    },
                    {
                        "surname": "Chartier",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "University of Liverpool, Liverpool, United Kingdom",
                                "organization": "University of Liverpool",
                                "country": "United Kingdom",
                            }
                        ],
                        "orcid": "0000-0003-0578-5567",
                    },
                    {
                        "surname": "Chattopadhyay",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Variable Energy Cyclotron Centre, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Variable Energy Cyclotron Centre",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0003-1097-8806",
                    },
                    {
                        "surname": "Chattopadhyay",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Saha Institute of Nuclear Physics, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Saha Institute of Nuclear Physics",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-8789-0004",
                    },
                    {
                        "surname": "Chavez",
                        "given_names": "T.G.",
                        "affiliations": [
                            {
                                "value": "High Energy Physics Group, Universidad Autónoma de Puebla, Puebla, Mexico",
                                "organization": "High Energy Physics Group",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0000-0002-6224-1577",
                    },
                    {
                        "surname": "Cheng",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0009-0004-0724-7003",
                    },
                    {
                        "surname": "Cheshkov",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Université de Lyon, CNRS/IN2P3, Institut de Physique des 2 Infinis de Lyon, Lyon, France",
                                "organization": "Université de Lyon",
                                "country": "France",
                            }
                        ],
                        "orcid": "0009-0002-8368-9407",
                    },
                    {
                        "surname": "Cheynis",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Université de Lyon, CNRS/IN2P3, Institut de Physique des 2 Infinis de Lyon, Lyon, France",
                                "organization": "Université de Lyon",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-4891-5168",
                    },
                    {
                        "surname": "Chibante Barroso",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0001-6837-3362",
                    },
                    {
                        "surname": "Chinellato",
                        "given_names": "D.D.",
                        "affiliations": [
                            {
                                "value": "Universidade Estadual de Campinas (UNICAMP), Campinas, Brazil",
                                "organization": "Universidade Estadual de Campinas (UNICAMP)",
                                "country": "Brazil",
                            }
                        ],
                        "orcid": "0000-0002-9982-9577",
                    },
                    {
                        "surname": "Chizzali",
                        "given_names": "E.S.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0009-7059-0601",
                    },
                    {
                        "surname": "Cho",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Inha University, Incheon, Republic of Korea",
                                "organization": "Inha University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0009-0001-4181-8891",
                    },
                    {
                        "surname": "Cho",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Inha University, Incheon, Republic of Korea",
                                "organization": "Inha University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0003-0000-2674",
                    },
                    {
                        "surname": "Chochula",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0009-0009-5292-9579",
                    },
                    {
                        "surname": "Christakoglou",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Nikhef, National institute for subatomic physics, Amsterdam, Netherlands",
                                "organization": "Nikhef, National institute for subatomic physics",
                                "country": "Netherlands",
                            }
                        ],
                        "orcid": "0000-0002-4325-0646",
                    },
                    {
                        "surname": "Christensen",
                        "given_names": "C.H.",
                        "affiliations": [
                            {
                                "value": "Niels Bohr Institute, University of Copenhagen, Copenhagen, Denmark",
                                "organization": "Niels Bohr Institute",
                                "country": "Denmark",
                            }
                        ],
                        "orcid": "0000-0002-1850-0121",
                    },
                    {
                        "surname": "Christiansen",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Lund University Department of Physics, Division of Particle Physics, Lund, Sweden",
                                "organization": "Lund University Department of Physics",
                                "country": "Sweden",
                            }
                        ],
                        "orcid": "0000-0001-7066-3473",
                    },
                    {
                        "surname": "Chujo",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "University of Tsukuba, Tsukuba, Japan",
                                "organization": "University of Tsukuba",
                                "country": "Japan",
                            }
                        ],
                        "orcid": "0000-0001-5433-969X",
                    },
                    {
                        "surname": "Ciacco",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Dipartimento DISAT del Politecnico and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento DISAT del Politecnico",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-8804-1100",
                    },
                    {
                        "surname": "Cicalo",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Cagliari, Cagliari, Italy",
                                "organization": "INFN, Sezione di Cagliari",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-5129-1723",
                    },
                    {
                        "surname": "Cifarelli",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Bologna, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-6806-3206",
                    },
                    {
                        "surname": "Cindolo",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bologna, Bologna, Italy",
                                "organization": "INFN, Sezione di Bologna",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-4255-7347",
                    },
                    {
                        "surname": "Ciupek",
                        "given_names": "M.R.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Clai",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bologna, Bologna, Italy",
                                "organization": "INFN, Sezione di Bologna",
                                "country": "Italy",
                            }
                        ],
                    },
                    {
                        "surname": "Colamaria",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bari, Bari, Italy",
                                "organization": "INFN, Sezione di Bari",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-2677-7961",
                    },
                    {
                        "surname": "Colburn",
                        "given_names": "J.S.",
                        "affiliations": [
                            {
                                "value": "School of Physics and Astronomy, University of Birmingham, Birmingham, United Kingdom",
                                "organization": "School of Physics and Astronomy",
                                "country": "United Kingdom",
                            }
                        ],
                    },
                    {
                        "surname": "Colella",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Politecnico di Bari and Sezione INFN, Bari, Italy",
                                "organization": "Politecnico di Bari",
                                "country": "Italy",
                            },
                            {
                                "value": "Dipartimento Interateneo di Fisica ‘M. Merlin’ and Sezione INFN, Bari, Italy",
                                "organization": "Dipartimento Interateneo di Fisica ‘M. Merlin’",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0001-9102-9500",
                    },
                    {
                        "surname": "Collu",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Lawrence Berkeley National Laboratory, Berkeley, CA, United States",
                                "organization": "Lawrence Berkeley National Laboratory",
                                "country": "United States",
                            }
                        ],
                    },
                    {
                        "surname": "Colocci",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0001-7804-0721",
                    },
                    {
                        "surname": "Concas",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Torino, Turin, Italy",
                                "organization": "INFN, Sezione di Torino",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-4167-9665",
                    },
                    {
                        "surname": "Conesa Balbastre",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Laboratoire de Physique Subatomique et de Cosmologie, Université Grenoble-Alpes, CNRS-IN2P3, Grenoble, France",
                                "organization": "Laboratoire de Physique Subatomique et de Cosmologie",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0001-5283-3520",
                    },
                    {
                        "surname": "Conesa del Valle",
                        "given_names": "Z.",
                        "affiliations": [
                            {
                                "value": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie, Orsay, France",
                                "organization": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-7602-2930",
                    },
                    {
                        "surname": "Contin",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Trieste, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-9504-2702",
                    },
                    {
                        "surname": "Contreras",
                        "given_names": "J.G.",
                        "affiliations": [
                            {
                                "value": "Faculty of Nuclear Sciences and Physical Engineering, Czech Technical University in Prague, Prague, Czech Republic",
                                "organization": "Faculty of Nuclear Sciences and Physical Engineering",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0002-9677-5294",
                    },
                    {
                        "surname": "Coquet",
                        "given_names": "M.L.",
                        "affiliations": [
                            {
                                "value": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA), IRFU, Départment de Physique Nucléaire (DPhN), Saclay, France",
                                "organization": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA)",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-8343-8758",
                    },
                    {
                        "surname": "Cormier",
                        "given_names": "T.M.",
                        "affiliations": [
                            {
                                "value": "Oak Ridge National Laboratory, Oak Ridge, TN, United States",
                                "organization": "Oak Ridge National Laboratory",
                                "country": "United States",
                            }
                        ],
                    },
                    {
                        "surname": "Cortese",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Università del Piemonte Orientale, Vercelli, Italy",
                                "organization": "Università del Piemonte Orientale",
                                "country": "Italy",
                            },
                            {
                                "value": "INFN, Sezione di Torino, Turin, Italy",
                                "organization": "INFN, Sezione di Torino",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0003-2778-6421",
                    },
                    {
                        "surname": "Cosentino",
                        "given_names": "M.R.",
                        "affiliations": [
                            {
                                "value": "Universidade Federal do ABC, Santo Andre, Brazil",
                                "organization": "Universidade Federal do ABC",
                                "country": "Brazil",
                            }
                        ],
                        "orcid": "0000-0002-7880-8611",
                    },
                    {
                        "surname": "Costa",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0001-6955-3314",
                    },
                    {
                        "surname": "Costanza",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica, Università di Pavia, Pavia, Italy",
                                "organization": "Dipartimento di Fisica",
                                "country": "Italy",
                            },
                            {
                                "value": "INFN, Sezione di Pavia, Pavia, Italy",
                                "organization": "INFN, Sezione di Pavia",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0002-5860-585X",
                    },
                    {
                        "surname": "Crochet",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Université Clermont Auvergne, CNRS/IN2P3, LPC, Clermont-Ferrand, France",
                                "organization": "Université Clermont Auvergne",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0001-7528-6523",
                    },
                    {
                        "surname": "Cruz-Torres",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Lawrence Berkeley National Laboratory, Berkeley, CA, United States",
                                "organization": "Lawrence Berkeley National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0001-6359-0608",
                    },
                    {
                        "surname": "Cuautle",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Instituto de Ciencias Nucleares, Universidad Nacional Autónoma de México, Mexico City, Mexico",
                                "organization": "Instituto de Ciencias Nucleares",
                                "country": "Mexico",
                            }
                        ],
                    },
                    {
                        "surname": "Cui",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0001-5140-9816",
                    },
                    {
                        "surname": "Cunqueiro",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Oak Ridge National Laboratory, Oak Ridge, TN, United States",
                                "organization": "Oak Ridge National Laboratory",
                                "country": "United States",
                            }
                        ],
                    },
                    {
                        "surname": "Dainese",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Padova, Padova, Italy",
                                "organization": "INFN, Sezione di Padova",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-2166-1874",
                    },
                    {
                        "surname": "Danisch",
                        "given_names": "M.C.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-5165-6638",
                    },
                    {
                        "surname": "Danu",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Institute of Space Science (ISS), Bucharest, Romania",
                                "organization": "Institute of Space Science (ISS)",
                                "country": "Romania",
                            }
                        ],
                        "orcid": "0000-0002-8899-3654",
                    },
                    {
                        "surname": "Das",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "National Institute of Science Education and Research, Homi Bhabha National Institute, Jatni, India",
                                "organization": "National Institute of Science Education and Research",
                                "country": "India",
                            }
                        ],
                        "orcid": "0009-0002-3904-8872",
                    },
                    {
                        "surname": "Das",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Bose Institute, Department of Physics and Centre for Astroparticle Physics and Space Science (CAPSS), Kolkata, India",
                                "organization": "Bose Institute",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0003-2771-9069",
                    },
                    {
                        "surname": "Das",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Bose Institute, Department of Physics and Centre for Astroparticle Physics and Space Science (CAPSS), Kolkata, India",
                                "organization": "Bose Institute",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-2678-6780",
                    },
                    {
                        "surname": "Dash",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Bombay (IIT), Mumbai, India",
                                "organization": "Indian Institute of Technology Bombay (IIT)",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0001-5008-6859",
                    },
                    {
                        "surname": "David",
                        "given_names": "R.M.H.",
                        "affiliations": [
                            {
                                "value": "High Energy Physics Group, Universidad Autónoma de Puebla, Puebla, Mexico",
                                "organization": "High Energy Physics Group",
                                "country": "Mexico",
                            }
                        ],
                    },
                    {
                        "surname": "De Caro",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica ‘E.R. Caianiello’ dell'Università and Gruppo Collegato INFN, Salerno, Italy",
                                "organization": "Dipartimento di Fisica ‘E.R. Caianiello’ dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-7865-4202",
                    },
                    {
                        "surname": "de Cataldo",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bari, Bari, Italy",
                                "organization": "INFN, Sezione di Bari",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-3220-4505",
                    },
                    {
                        "surname": "De Cilladi",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-5986-3842",
                    },
                    {
                        "surname": "de Cuveland",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Frankfurt Institute for Advanced Studies, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Frankfurt Institute for Advanced Studies",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "De Falco",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Cagliari, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-0830-4872",
                    },
                    {
                        "surname": "De Gruttola",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica ‘E.R. Caianiello’ dell'Università and Gruppo Collegato INFN, Salerno, Italy",
                                "organization": "Dipartimento di Fisica ‘E.R. Caianiello’ dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-7055-6181",
                    },
                    {
                        "surname": "De Marco",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Torino, Turin, Italy",
                                "organization": "INFN, Sezione di Torino",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-5884-4404",
                    },
                    {
                        "surname": "De Martin",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Trieste, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-0711-4022",
                    },
                    {
                        "surname": "De Pasquale",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica ‘E.R. Caianiello’ dell'Università and Gruppo Collegato INFN, Salerno, Italy",
                                "organization": "Dipartimento di Fisica ‘E.R. Caianiello’ dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-9236-0748",
                    },
                    {
                        "surname": "Deb",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Indore, Indore, India",
                                "organization": "Indian Institute of Technology Indore",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-0175-3712",
                    },
                    {
                        "surname": "Degenhardt",
                        "given_names": "H.F.",
                        "affiliations": [
                            {
                                "value": "Universidade de São Paulo (USP), São Paulo, Brazil",
                                "organization": "Universidade de São Paulo (USP)",
                                "country": "Brazil",
                            }
                        ],
                    },
                    {
                        "surname": "Deja",
                        "given_names": "K.R.",
                        "affiliations": [
                            {
                                "value": "Warsaw University of Technology, Warsaw, Poland",
                                "organization": "Warsaw University of Technology",
                                "country": "Poland",
                            }
                        ],
                    },
                    {
                        "surname": "Del Grande",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-7599-2716",
                    },
                    {
                        "surname": "Dello Stritto",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica ‘E.R. Caianiello’ dell'Università and Gruppo Collegato INFN, Salerno, Italy",
                                "organization": "Dipartimento di Fisica ‘E.R. Caianiello’ dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-6700-7950",
                    },
                    {
                        "surname": "Deng",
                        "given_names": "W.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0003-2860-9881",
                    },
                    {
                        "surname": "Dhankher",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, University of California, Berkeley, CA, United States",
                                "organization": "Department of Physics",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-6562-5082",
                    },
                    {
                        "surname": "Di Bari",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Dipartimento Interateneo di Fisica ‘M. Merlin’ and Sezione INFN, Bari, Italy",
                                "organization": "Dipartimento Interateneo di Fisica ‘M. Merlin’",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-5559-8906",
                    },
                    {
                        "surname": "Di Mauro",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0003-0348-092X",
                    },
                    {
                        "surname": "Diaz",
                        "given_names": "R.A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN"
                            },
                            {
                                "value": "Centro de Aplicaciones Tecnológicas y Desarrollo Nuclear (CEADEN), Havana, Cuba",
                                "organization": "Centro de Aplicaciones Tecnológicas y Desarrollo Nuclear (CEADEN)",
                                "country": "Cuba",
                            },
                        ],
                        "orcid": "0000-0002-4886-6052",
                    },
                    {
                        "surname": "Dietel",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "University of Cape Town, Cape Town, South Africa",
                                "organization": "University of Cape Town",
                                "country": "South Africa",
                            }
                        ],
                        "orcid": "0000-0002-2065-6256",
                    },
                    {
                        "surname": "Ding",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Université de Lyon, CNRS/IN2P3, Institut de Physique des 2 Infinis de Lyon, Lyon, France",
                                "organization": "Université de Lyon",
                                "country": "France",
                            },
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            },
                        ],
                        "orcid": "0009-0005-3775-1945",
                    },
                    {
                        "surname": "Divià",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-6357-7857",
                    },
                    {
                        "surname": "Dixit",
                        "given_names": "D.U.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, University of California, Berkeley, CA, United States",
                                "organization": "Department of Physics",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0009-0000-1217-7768",
                    },
                    {
                        "surname": "Djuvsland",
                        "given_names": "Ø.",
                        "affiliations": [
                            {
                                "value": "Department of Physics and Technology, University of Bergen, Bergen, Norway",
                                "organization": "Department of Physics and Technology",
                                "country": "Norway",
                            }
                        ],
                    },
                    {
                        "surname": "Dmitrieva",
                        "given_names": "U.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0001-6853-8905",
                    },
                    {
                        "surname": "Dobrin",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Institute of Space Science (ISS), Bucharest, Romania",
                                "organization": "Institute of Space Science (ISS)",
                                "country": "Romania",
                            }
                        ],
                        "orcid": "0000-0003-4432-4026",
                    },
                    {
                        "surname": "Dönigus",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-0739-0120",
                    },
                    {
                        "surname": "Dubey",
                        "given_names": "A.K.",
                        "affiliations": [
                            {
                                "value": "Variable Energy Cyclotron Centre, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Variable Energy Cyclotron Centre",
                                "country": "India",
                            }
                        ],
                        "orcid": "0009-0001-6339-1104",
                    },
                    {
                        "surname": "Dubinski",
                        "given_names": "J.M.",
                        "affiliations": [
                            {
                                "value": "Warsaw University of Technology, Warsaw, Poland",
                                "organization": "Warsaw University of Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0002-2568-0132",
                    },
                    {
                        "surname": "Dubla",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-9582-8948",
                    },
                    {
                        "surname": "Dudi",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Physics Department, Panjab University, Chandigarh, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                        "orcid": "0009-0007-4091-5327",
                    },
                    {
                        "surname": "Dupieux",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Université Clermont Auvergne, CNRS/IN2P3, LPC, Clermont-Ferrand, France",
                                "organization": "Université Clermont Auvergne",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-0207-2871",
                    },
                    {
                        "surname": "Durkac",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Technical University of Košice, Košice, Slovak Republic",
                                "organization": "Technical University of Košice",
                                "country": "Slovak Republic",
                            }
                        ],
                    },
                    {
                        "surname": "Dzalaiova",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Comenius University Bratislava, Faculty of Mathematics, Physics and Informatics, Bratislava, Slovak Republic",
                                "organization": "Comenius University Bratislava",
                                "country": "Slovak Republic",
                            }
                        ],
                    },
                    {
                        "surname": "Eder",
                        "given_names": "T.M.",
                        "affiliations": [
                            {
                                "value": "Westfälische Wilhelms-Universität Münster, Institut für Kernphysik, Münster, Germany",
                                "organization": "Westfälische Wilhelms-Universität Münster",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0008-9752-4391",
                    },
                    {
                        "surname": "Ehlers",
                        "given_names": "R.J.",
                        "affiliations": [
                            {
                                "value": "Oak Ridge National Laboratory, Oak Ridge, TN, United States",
                                "organization": "Oak Ridge National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-3897-0876",
                    },
                    {
                        "surname": "Eikeland",
                        "given_names": "V.N.",
                        "affiliations": [
                            {
                                "value": "Department of Physics and Technology, University of Bergen, Bergen, Norway",
                                "organization": "Department of Physics and Technology",
                                "country": "Norway",
                            }
                        ],
                    },
                    {
                        "surname": "Eisenhut",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0006-9458-8723",
                    },
                    {
                        "surname": "Elia",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bari, Bari, Italy",
                                "organization": "INFN, Sezione di Bari",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-6351-2378",
                    },
                    {
                        "surname": "Erazmus",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "SUBATECH, IMT Atlantique, Nantes Université, CNRS-IN2P3, Nantes, France",
                                "organization": "SUBATECH",
                                "country": "France",
                            }
                        ],
                        "orcid": "0009-0003-4464-3366",
                    },
                    {
                        "surname": "Ercolessi",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Bologna, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-7873-0968",
                    },
                    {
                        "surname": "Erhardt",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Physics department, Faculty of science, University of Zagreb, Zagreb, Croatia",
                                "organization": "Physics department",
                                "country": "Croatia",
                            }
                        ],
                        "orcid": "0000-0001-9410-246X",
                    },
                    {
                        "surname": "Ersdal",
                        "given_names": "M.R.",
                        "affiliations": [
                            {
                                "value": "Department of Physics and Technology, University of Bergen, Bergen, Norway",
                                "organization": "Department of Physics and Technology",
                                "country": "Norway",
                            }
                        ],
                    },
                    {
                        "surname": "Espagnon",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie, Orsay, France",
                                "organization": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0003-2449-3172",
                    },
                    {
                        "surname": "Eulisse",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0003-1795-6212",
                    },
                    {
                        "surname": "Evans",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "School of Physics and Astronomy, University of Birmingham, Birmingham, United Kingdom",
                                "organization": "School of Physics and Astronomy",
                                "country": "United Kingdom",
                            }
                        ],
                        "orcid": "0000-0002-8427-322X",
                    },
                    {
                        "surname": "Evdokimov",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-4239-6424",
                    },
                    {
                        "surname": "Fabbietti",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-2325-8368",
                    },
                    {
                        "surname": "Faggin",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Padova, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-2202-5906",
                    },
                    {
                        "surname": "Faivre",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Laboratoire de Physique Subatomique et de Cosmologie, Université Grenoble-Alpes, CNRS-IN2P3, Grenoble, France",
                                "organization": "Laboratoire de Physique Subatomique et de Cosmologie",
                                "country": "France",
                            }
                        ],
                        "orcid": "0009-0007-8219-3334",
                    },
                    {
                        "surname": "Fan",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0003-3573-3389",
                    },
                    {
                        "surname": "Fan",
                        "given_names": "W.",
                        "affiliations": [
                            {
                                "value": "Lawrence Berkeley National Laboratory, Berkeley, CA, United States",
                                "organization": "Lawrence Berkeley National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-0844-3282",
                    },
                    {
                        "surname": "Fantoni",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "INFN, Laboratori Nazionali di Frascati, Frascati, Italy",
                                "organization": "INFN, Laboratori Nazionali di Frascati",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-6270-9283",
                    },
                    {
                        "surname": "Fasel",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Oak Ridge National Laboratory, Oak Ridge, TN, United States",
                                "organization": "Oak Ridge National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0009-0005-4586-0930",
                    },
                    {
                        "surname": "Fecchio",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Dipartimento DISAT del Politecnico and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento DISAT del Politecnico",
                                "country": "Italy",
                            }
                        ],
                    },
                    {
                        "surname": "Feliciello",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Torino, Turin, Italy",
                                "organization": "INFN, Sezione di Torino",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-5823-9733",
                    },
                    {
                        "surname": "Feofilov",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0003-3700-8623",
                    },
                    {
                        "surname": "Fernández Téllez",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "High Energy Physics Group, Universidad Autónoma de Puebla, Puebla, Mexico",
                                "organization": "High Energy Physics Group",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0000-0003-0152-4220",
                    },
                    {
                        "surname": "Ferrer",
                        "given_names": "M.B.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0001-9723-1291",
                    },
                    {
                        "surname": "Ferrero",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA), IRFU, Départment de Physique Nucléaire (DPhN), Saclay, France",
                                "organization": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA)",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0003-1089-6632",
                    },
                    {
                        "surname": "Ferretti",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-9084-5784",
                    },
                    {
                        "surname": "Feuillard",
                        "given_names": "V.J.G.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0002-0542-4454",
                    },
                    {
                        "surname": "Figiel",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "The Henryk Niewodniczanski Institute of Nuclear Physics, Polish Academy of Sciences, Cracow, Poland",
                                "organization": "The Henryk Niewodniczanski Institute of Nuclear Physics",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0002-7692-0079",
                    },
                    {
                        "surname": "Filova",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Faculty of Nuclear Sciences and Physical Engineering, Czech Technical University in Prague, Prague, Czech Republic",
                                "organization": "Faculty of Nuclear Sciences and Physical Engineering",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0002-6444-4669",
                    },
                    {
                        "surname": "Finogeev",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-7104-7477",
                    },
                    {
                        "surname": "Fionda",
                        "given_names": "F.M.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Cagliari, Cagliari, Italy",
                                "organization": "INFN, Sezione di Cagliari",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-8632-5580",
                    },
                    {
                        "surname": "Fiorenza",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Politecnico di Bari and Sezione INFN, Bari, Italy",
                                "organization": "Politecnico di Bari",
                                "country": "Italy",
                            }
                        ],
                    },
                    {
                        "surname": "Flor",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "University of Houston, Houston, TX, United States",
                                "organization": "University of Houston",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-0194-1318",
                    },
                    {
                        "surname": "Flores",
                        "given_names": "A.N.",
                        "affiliations": [
                            {
                                "value": "The University of Texas at Austin, Austin, TX, United States",
                                "organization": "The University of Texas at Austin",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0009-0006-6140-676X",
                    },
                    {
                        "surname": "Foertsch",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "iThemba LABS, National Research Foundation, Somerset West, South Africa",
                                "organization": "iThemba LABS",
                                "country": "South Africa",
                            }
                        ],
                        "orcid": "0009-0007-2053-4869",
                    },
                    {
                        "surname": "Fokin",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-0642-2047",
                    },
                    {
                        "surname": "Fokin",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-2136-778X",
                    },
                    {
                        "surname": "Fragiacomo",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Trieste, Trieste, Italy",
                                "organization": "INFN, Sezione di Trieste",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-8216-396X",
                    },
                    {
                        "surname": "Frajna",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Wigner Research Centre for Physics, Budapest, Hungary",
                                "organization": "Wigner Research Centre for Physics",
                                "country": "Hungary",
                            }
                        ],
                        "orcid": "0000-0002-3420-6301",
                    },
                    {
                        "surname": "Fuchs",
                        "given_names": "U.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0009-0005-2155-0460",
                    },
                    {
                        "surname": "Funicello",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica ‘E.R. Caianiello’ dell'Università and Gruppo Collegato INFN, Salerno, Italy",
                                "organization": "Dipartimento di Fisica ‘E.R. Caianiello’ dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-7814-319X",
                    },
                    {
                        "surname": "Furget",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Laboratoire de Physique Subatomique et de Cosmologie, Université Grenoble-Alpes, CNRS-IN2P3, Grenoble, France",
                                "organization": "Laboratoire de Physique Subatomique et de Cosmologie",
                                "country": "France",
                            }
                        ],
                        "orcid": "0009-0004-9666-7156",
                    },
                    {
                        "surname": "Furs",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-2582-1927",
                    },
                    {
                        "surname": "Gaardhøje",
                        "given_names": "J.J.",
                        "affiliations": [
                            {
                                "value": "Niels Bohr Institute, University of Copenhagen, Copenhagen, Denmark",
                                "organization": "Niels Bohr Institute",
                                "country": "Denmark",
                            }
                        ],
                        "orcid": "0000-0001-6122-4698",
                    },
                    {
                        "surname": "Gagliardi",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-6314-7419",
                    },
                    {
                        "surname": "Gago",
                        "given_names": "A.M.",
                        "affiliations": [
                            {
                                "value": "Sección Física, Departamento de Ciencias, Pontificia Universidad Católica del Perú, Lima, Peru",
                                "organization": "Sección Física",
                                "country": "Peru",
                            }
                        ],
                        "orcid": "0000-0002-0019-9692",
                    },
                    {
                        "surname": "Gal",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Université de Strasbourg, CNRS, IPHC UMR 7178, F-67000 Strasbourg, France",
                                "organization": "Université de Strasbourg",
                                "country": "France",
                            }
                        ],
                    },
                    {
                        "surname": "Galvan",
                        "given_names": "C.D.",
                        "affiliations": [
                            {
                                "value": "Universidad Autónoma de Sinaloa, Culiacán, Mexico",
                                "organization": "Universidad Autónoma de Sinaloa",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0000-0001-5496-8533",
                    },
                    {
                        "surname": "Ganoti",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "National and Kapodistrian University of Athens, School of Science, Department of Physics , Athens, Greece",
                                "organization": "National and Kapodistrian University of Athens",
                                "country": "Greece",
                            }
                        ],
                        "orcid": "0000-0003-4871-4064",
                    },
                    {
                        "surname": "Garabatos",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0007-2395-8130",
                    },
                    {
                        "surname": "Garcia",
                        "given_names": "J.R.A.",
                        "affiliations": [
                            {
                                "value": "High Energy Physics Group, Universidad Autónoma de Puebla, Puebla, Mexico",
                                "organization": "High Energy Physics Group",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0000-0002-5038-1337",
                    },
                    {
                        "surname": "Garcia-Solis",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Chicago State University, Chicago, IL, United States",
                                "organization": "Chicago State University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-6847-8671",
                    },
                    {
                        "surname": "Garg",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "SUBATECH, IMT Atlantique, Nantes Université, CNRS-IN2P3, Nantes, France",
                                "organization": "SUBATECH",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-8512-8219",
                    },
                    {
                        "surname": "Gargiulo",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0009-0001-4753-577X",
                    },
                    {
                        "surname": "Garibli",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "National Nuclear Research Center, Baku, Azerbaijan",
                                "organization": "National Nuclear Research Center",
                                "country": "Azerbaijan",
                            }
                        ],
                    },
                    {
                        "surname": "Garner",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "Westfälische Wilhelms-Universität Münster, Institut für Kernphysik, Münster, Germany",
                                "organization": "Westfälische Wilhelms-Universität Münster",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Gauger",
                        "given_names": "E.F.",
                        "affiliations": [
                            {
                                "value": "The University of Texas at Austin, Austin, TX, United States",
                                "organization": "The University of Texas at Austin",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-0015-6713",
                    },
                    {
                        "surname": "Gautam",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "University of Kansas, Lawrence, KS, United States",
                                "organization": "University of Kansas",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0001-7039-535X",
                    },
                    {
                        "surname": "Gay Ducati",
                        "given_names": "M.B.",
                        "affiliations": [
                            {
                                "value": "Instituto de Física, Universidade Federal do Rio Grande do Sul (UFRGS), Porto Alegre, Brazil",
                                "organization": "Instituto de Física",
                                "country": "Brazil",
                            }
                        ],
                        "orcid": "0000-0002-8450-5318",
                    },
                    {
                        "surname": "Germain",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "SUBATECH, IMT Atlantique, Nantes Université, CNRS-IN2P3, Nantes, France",
                                "organization": "SUBATECH",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0001-7382-1609",
                    },
                    {
                        "surname": "Ghosh",
                        "given_names": "S.K.",
                        "affiliations": [
                            {
                                "value": "Bose Institute, Department of Physics and Centre for Astroparticle Physics and Space Science (CAPSS), Kolkata, India",
                                "organization": "Bose Institute",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Giacalone",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Bologna, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-4831-5808",
                    },
                    {
                        "surname": "Gianotti",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "INFN, Laboratori Nazionali di Frascati, Frascati, Italy",
                                "organization": "INFN, Laboratori Nazionali di Frascati",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-4167-7176",
                    },
                    {
                        "surname": "Giubellino",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            },
                            {
                                "value": "INFN, Sezione di Torino, Turin, Italy",
                                "organization": "INFN, Sezione di Torino",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0002-1383-6160",
                    },
                    {
                        "surname": "Giubilato",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Padova, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-4358-5355",
                    },
                    {
                        "surname": "Glaenzer",
                        "given_names": "A.M.C.",
                        "affiliations": [
                            {
                                "value": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA), IRFU, Départment de Physique Nucléaire (DPhN), Saclay, France",
                                "organization": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA)",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0001-7400-7019",
                    },
                    {
                        "surname": "Glässel",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-3793-5291",
                    },
                    {
                        "surname": "Glimos",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "University of Tennessee, Knoxville, TN, United States",
                                "organization": "University of Tennessee",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0009-0008-1162-7067",
                    },
                    {
                        "surname": "Goh",
                        "given_names": "D.J.Q.",
                        "affiliations": [
                            {
                                "value": "Nagasaki Institute of Applied Science, Nagasaki, Japan",
                                "organization": "Nagasaki Institute of Applied Science",
                                "country": "Japan",
                            }
                        ],
                    },
                    {
                        "surname": "Gonzalez",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Wayne State University, Detroit, MI, United States",
                                "organization": "Wayne State University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-7607-3965",
                    },
                    {
                        "surname": "González-Trueba",
                        "given_names": "L.H.",
                        "affiliations": [
                            {
                                "value": "Instituto de Física, Universidad Nacional Autónoma de México, Mexico City, Mexico",
                                "organization": "Instituto de Física",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0009-0006-9202-262X",
                    },
                    {
                        "surname": "Gorbunov",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Frankfurt Institute for Advanced Studies, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Frankfurt Institute for Advanced Studies",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Gorgon",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "AGH University of Science and Technology, Cracow, Poland",
                                "organization": "AGH University of Science and Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0003-1746-1279",
                    },
                    {
                        "surname": "Görlich",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "The Henryk Niewodniczanski Institute of Nuclear Physics, Polish Academy of Sciences, Cracow, Poland",
                                "organization": "The Henryk Niewodniczanski Institute of Nuclear Physics",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0001-7792-2247",
                    },
                    {
                        "surname": "Gotovac",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Faculty of Electrical Engineering, Mechanical Engineering and Naval Architecture, University of Split, Split, Croatia",
                                "organization": "Faculty of Electrical Engineering, Mechanical Engineering and Naval Architecture",
                                "country": "Croatia",
                            }
                        ],
                    },
                    {
                        "surname": "Grabski",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Instituto de Física, Universidad Nacional Autónoma de México, Mexico City, Mexico",
                                "organization": "Instituto de Física",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0000-0002-9581-0879",
                    },
                    {
                        "surname": "Graczykowski",
                        "given_names": "L.K.",
                        "affiliations": [
                            {
                                "value": "Warsaw University of Technology, Warsaw, Poland",
                                "organization": "Warsaw University of Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0002-4442-5727",
                    },
                    {
                        "surname": "Grecka",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Nuclear Physics Institute of the Czech Academy of Sciences, Husinec-Řež, Czech Republic",
                                "organization": "Nuclear Physics Institute of the Czech Academy of Sciences",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0009-0002-9826-4989",
                    },
                    {
                        "surname": "Greiner",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Lawrence Berkeley National Laboratory, Berkeley, CA, United States",
                                "organization": "Lawrence Berkeley National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0003-1476-6245",
                    },
                    {
                        "surname": "Grelli",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Institute for Gravitational and Subatomic Physics (GRASP), Utrecht University/Nikhef, Utrecht, Netherlands",
                                "organization": "Institute for Gravitational and Subatomic Physics (GRASP)",
                                "country": "Netherlands",
                            }
                        ],
                        "orcid": "0000-0003-0562-9820",
                    },
                    {
                        "surname": "Grigoras",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0009-0006-9035-556X",
                    },
                    {
                        "surname": "Grigoriev",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-0661-5220",
                    },
                    {
                        "surname": "Grigoryan",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN"
                            },
                            {
                                "value": "A.I. Alikhanyan National Science Laboratory (Yerevan Physics Institute) Foundation, Yerevan, Armenia",
                                "organization": "A.I. Alikhanyan National Science Laboratory (Yerevan Physics Institute) Foundation",
                                "country": "Armenia",
                            },
                        ],
                        "orcid": "0000-0002-0658-5949",
                    },
                    {
                        "surname": "Grosa",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-1469-9022",
                    },
                    {
                        "surname": "Grosse-Oetringhaus",
                        "given_names": "J.F.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0001-8372-5135",
                    },
                    {
                        "surname": "Grosso",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-9960-2594",
                    },
                    {
                        "surname": "Grund",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Faculty of Nuclear Sciences and Physical Engineering, Czech Technical University in Prague, Prague, Czech Republic",
                                "organization": "Faculty of Nuclear Sciences and Physical Engineering",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0001-9785-2215",
                    },
                    {
                        "surname": "Guardiano",
                        "given_names": "G.G.",
                        "affiliations": [
                            {
                                "value": "Universidade Estadual de Campinas (UNICAMP), Campinas, Brazil",
                                "organization": "Universidade Estadual de Campinas (UNICAMP)",
                                "country": "Brazil",
                            }
                        ],
                        "orcid": "0000-0002-5298-2881",
                    },
                    {
                        "surname": "Guernane",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Laboratoire de Physique Subatomique et de Cosmologie, Université Grenoble-Alpes, CNRS-IN2P3, Grenoble, France",
                                "organization": "Laboratoire de Physique Subatomique et de Cosmologie",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0003-0626-9724",
                    },
                    {
                        "surname": "Guilbaud",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "SUBATECH, IMT Atlantique, Nantes Université, CNRS-IN2P3, Nantes, France",
                                "organization": "SUBATECH",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0001-5990-482X",
                    },
                    {
                        "surname": "Gulbrandsen",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "Niels Bohr Institute, University of Copenhagen, Copenhagen, Denmark",
                                "organization": "Niels Bohr Institute",
                                "country": "Denmark",
                            }
                        ],
                        "orcid": "0000-0002-3809-4984",
                    },
                    {
                        "surname": "Gunji",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "University of Tokyo, Tokyo, Japan",
                                "organization": "University of Tokyo",
                                "country": "Japan",
                            }
                        ],
                        "orcid": "0000-0002-6769-599X",
                    },
                    {
                        "surname": "Guo",
                        "given_names": "W.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0002-2843-2556",
                    },
                    {
                        "surname": "Gupta",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Jammu, Jammu, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0001-6178-648X",
                    },
                    {
                        "surname": "Gupta",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Jammu, Jammu, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0001-7474-0755",
                    },
                    {
                        "surname": "Guzman",
                        "given_names": "S.P.",
                        "affiliations": [
                            {
                                "value": "High Energy Physics Group, Universidad Autónoma de Puebla, Puebla, Mexico",
                                "organization": "High Energy Physics Group",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0009-0008-0106-3130",
                    },
                    {
                        "surname": "Gyulai",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Wigner Research Centre for Physics, Budapest, Hungary",
                                "organization": "Wigner Research Centre for Physics",
                                "country": "Hungary",
                            }
                        ],
                        "orcid": "0000-0002-2420-7650",
                    },
                    {
                        "surname": "Habib",
                        "given_names": "M.K.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Hadjidakis",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie, Orsay, France",
                                "organization": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-9336-5169",
                    },
                    {
                        "surname": "Hamagaki",
                        "given_names": "H.",
                        "affiliations": [
                            {
                                "value": "Nagasaki Institute of Applied Science, Nagasaki, Japan",
                                "organization": "Nagasaki Institute of Applied Science",
                                "country": "Japan",
                            }
                        ],
                        "orcid": "0000-0003-3808-7917",
                    },
                    {
                        "surname": "Hamid",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                    },
                    {
                        "surname": "Han",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Yonsei University, Seoul, Republic of Korea",
                                "organization": "Yonsei University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0009-0008-6551-4180",
                    },
                    {
                        "surname": "Hannigan",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "The University of Texas at Austin, Austin, TX, United States",
                                "organization": "The University of Texas at Austin",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0003-4518-3528",
                    },
                    {
                        "surname": "Haque",
                        "given_names": "M.R.",
                        "affiliations": [
                            {
                                "value": "Warsaw University of Technology, Warsaw, Poland",
                                "organization": "Warsaw University of Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0001-7978-9638",
                    },
                    {
                        "surname": "Harlenderova",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Harris",
                        "given_names": "J.W.",
                        "affiliations": [
                            {
                                "value": "Yale University, New Haven, CT, United States",
                                "organization": "Yale University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-8535-3061",
                    },
                    {
                        "surname": "Harton",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Chicago State University, Chicago, IL, United States",
                                "organization": "Chicago State University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0009-0004-3528-4709",
                    },
                    {
                        "surname": "Hasenbichler",
                        "given_names": "J.A.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                    },
                    {
                        "surname": "Hassan",
                        "given_names": "H.",
                        "affiliations": [
                            {
                                "value": "Oak Ridge National Laboratory, Oak Ridge, TN, United States",
                                "organization": "Oak Ridge National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-6529-560X",
                    },
                    {
                        "surname": "Hatzifotiadou",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bologna, Bologna, Italy",
                                "organization": "INFN, Sezione di Bologna",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-7638-2047",
                    },
                    {
                        "surname": "Hauer",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Helmholtz-Institut für Strahlen- und Kernphysik, Rheinische Friedrich-Wilhelms-Universität Bonn, Bonn, Germany",
                                "organization": "Helmholtz-Institut für Strahlen- und Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-9593-6730",
                    },
                    {
                        "surname": "Havener",
                        "given_names": "L.B.",
                        "affiliations": [
                            {
                                "value": "Yale University, New Haven, CT, United States",
                                "organization": "Yale University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-4743-2885",
                    },
                    {
                        "surname": "Heckel",
                        "given_names": "S.T.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-9083-4484",
                    },
                    {
                        "surname": "Hellbär",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-7404-8723",
                    },
                    {
                        "surname": "Helstrup",
                        "given_names": "H.",
                        "affiliations": [
                            {
                                "value": "Faculty of Engineering and Science, Western Norway University of Applied Sciences, Bergen, Norway",
                                "organization": "Faculty of Engineering and Science",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0000-0002-9335-9076",
                    },
                    {
                        "surname": "Herman",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Faculty of Nuclear Sciences and Physical Engineering, Czech Technical University in Prague, Prague, Czech Republic",
                                "organization": "Faculty of Nuclear Sciences and Physical Engineering",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0003-4004-5265",
                    },
                    {
                        "surname": "Herrera Corral",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Centro de Investigación y de Estudios Avanzados (CINVESTAV), Mexico City and Mérida, Mexico",
                                "organization": "Centro de Investigación y de Estudios Avanzados (CINVESTAV)",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0000-0003-4692-7410",
                    },
                    {
                        "surname": "Herrmann",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Westfälische Wilhelms-Universität Münster, Institut für Kernphysik, Münster, Germany",
                                "organization": "Westfälische Wilhelms-Universität Münster",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Hetland",
                        "given_names": "K.F.",
                        "affiliations": [
                            {
                                "value": "Faculty of Engineering and Science, Western Norway University of Applied Sciences, Bergen, Norway",
                                "organization": "Faculty of Engineering and Science",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0009-0004-3122-4872",
                    },
                    {
                        "surname": "Heybeck",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0009-1031-8307",
                    },
                    {
                        "surname": "Hillemanns",
                        "given_names": "H.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-6527-1245",
                    },
                    {
                        "surname": "Hills",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "University of Liverpool, Liverpool, United Kingdom",
                                "organization": "University of Liverpool",
                                "country": "United Kingdom",
                            }
                        ],
                        "orcid": "0000-0003-4647-4159",
                    },
                    {
                        "surname": "Hippolyte",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Université de Strasbourg, CNRS, IPHC UMR 7178, F-67000 Strasbourg, France",
                                "organization": "Université de Strasbourg",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0003-4562-2922",
                    },
                    {
                        "surname": "Hofman",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Institute for Gravitational and Subatomic Physics (GRASP), Utrecht University/Nikhef, Utrecht, Netherlands",
                                "organization": "Institute for Gravitational and Subatomic Physics (GRASP)",
                                "country": "Netherlands",
                            }
                        ],
                        "orcid": "0000-0002-3850-8884",
                    },
                    {
                        "surname": "Hohlweger",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Nikhef, National institute for subatomic physics, Amsterdam, Netherlands",
                                "organization": "Nikhef, National institute for subatomic physics",
                                "country": "Netherlands",
                            }
                        ],
                        "orcid": "0000-0001-6925-3469",
                    },
                    {
                        "surname": "Honermann",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Westfälische Wilhelms-Universität Münster, Institut für Kernphysik, Münster, Germany",
                                "organization": "Westfälische Wilhelms-Universität Münster",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-1437-6108",
                    },
                    {
                        "surname": "Hong",
                        "given_names": "G.H.",
                        "affiliations": [
                            {
                                "value": "Yonsei University, Seoul, Republic of Korea",
                                "organization": "Yonsei University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0002-3632-4547",
                    },
                    {
                        "surname": "Horak",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Faculty of Nuclear Sciences and Physical Engineering, Czech Technical University in Prague, Prague, Czech Republic",
                                "organization": "Faculty of Nuclear Sciences and Physical Engineering",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0002-7078-3093",
                    },
                    {
                        "surname": "Horzyk",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "AGH University of Science and Technology, Cracow, Poland",
                                "organization": "AGH University of Science and Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0001-9001-4198",
                    },
                    {
                        "surname": "Hosokawa",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Creighton University, Omaha, NE, United States",
                                "organization": "Creighton University",
                                "country": "United States",
                            }
                        ],
                    },
                    {
                        "surname": "Hou",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0009-0003-2644-3643",
                    },
                    {
                        "surname": "Hristov",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0003-1477-8414",
                    },
                    {
                        "surname": "Hughes",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "University of Tennessee, Knoxville, TN, United States",
                                "organization": "University of Tennessee",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-2442-4583",
                    },
                    {
                        "surname": "Huhn",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Huhta",
                        "given_names": "L.M.",
                        "affiliations": [
                            {
                                "value": "University of Jyväskylä, Jyväskylä, Finland",
                                "organization": "University of Jyväskylä",
                                "country": "Finland",
                            }
                        ],
                        "orcid": "0000-0001-9352-5049",
                    },
                    {
                        "surname": "Hulse",
                        "given_names": "C.V.",
                        "affiliations": [
                            {
                                "value": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie, Orsay, France",
                                "organization": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-5397-6782",
                    },
                    {
                        "surname": "Humanic",
                        "given_names": "T.J.",
                        "affiliations": [
                            {
                                "value": "Ohio State University, Columbus, OH, United States",
                                "organization": "Ohio State University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0003-1008-5119",
                    },
                    {
                        "surname": "Hushnud",
                        "given_names": "H.",
                        "affiliations": [
                            {
                                "value": "Saha Institute of Nuclear Physics, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Saha Institute of Nuclear Physics",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Hutson",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "University of Houston, Houston, TX, United States",
                                "organization": "University of Houston",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0009-0008-7787-9304",
                    },
                    {
                        "surname": "Hutter",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Frankfurt Institute for Advanced Studies, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Frankfurt Institute for Advanced Studies",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-1488-4009",
                    },
                    {
                        "surname": "Iddon",
                        "given_names": "J.P.",
                        "affiliations": [
                            {
                                "value": "University of Liverpool, Liverpool, United Kingdom",
                                "organization": "University of Liverpool",
                                "country": "United Kingdom",
                            }
                        ],
                        "orcid": "0000-0002-2851-5554",
                    },
                    {
                        "surname": "Ilkaev",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                    },
                    {
                        "surname": "Ilyas",
                        "given_names": "H.",
                        "affiliations": [
                            {
                                "value": "COMSATS University Islamabad, Islamabad, Pakistan",
                                "organization": "COMSATS University Islamabad",
                                "country": "Pakistan",
                            }
                        ],
                        "orcid": "0000-0002-3693-2649",
                    },
                    {
                        "surname": "Inaba",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "University of Tsukuba, Tsukuba, Japan",
                                "organization": "University of Tsukuba",
                                "country": "Japan",
                            }
                        ],
                        "orcid": "0000-0003-3895-9092",
                    },
                    {
                        "surname": "Innocenti",
                        "given_names": "G.M.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0003-2478-9651",
                    },
                    {
                        "surname": "Ippolitov",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0001-9059-2414",
                    },
                    {
                        "surname": "Isakov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Nuclear Physics Institute of the Czech Academy of Sciences, Husinec-Řež, Czech Republic",
                                "organization": "Nuclear Physics Institute of the Czech Academy of Sciences",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0002-2134-967X",
                    },
                    {
                        "surname": "Isidori",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "University of Kansas, Lawrence, KS, United States",
                                "organization": "University of Kansas",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-7934-4038",
                    },
                    {
                        "surname": "Islam",
                        "given_names": "M.S.",
                        "affiliations": [
                            {
                                "value": "Saha Institute of Nuclear Physics, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Saha Institute of Nuclear Physics",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0001-9047-4856",
                    },
                    {
                        "surname": "Ivanov",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-7461-7327",
                    },
                    {
                        "surname": "Ivanov",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0009-0002-2983-9494",
                    },
                    {
                        "surname": "Izucheev",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                    },
                    {
                        "surname": "Jablonski",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "AGH University of Science and Technology, Cracow, Poland",
                                "organization": "AGH University of Science and Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0003-2406-911X",
                    },
                    {
                        "surname": "Jacak",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Lawrence Berkeley National Laboratory, Berkeley, CA, United States",
                                "organization": "Lawrence Berkeley National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0003-2889-2234",
                    },
                    {
                        "surname": "Jacazio",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-3066-855X",
                    },
                    {
                        "surname": "Jacobs",
                        "given_names": "P.M.",
                        "affiliations": [
                            {
                                "value": "Lawrence Berkeley National Laboratory, Berkeley, CA, United States",
                                "organization": "Lawrence Berkeley National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0001-9980-5199",
                    },
                    {
                        "surname": "Jadlovska",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Technical University of Košice, Košice, Slovak Republic",
                                "organization": "Technical University of Košice",
                                "country": "Slovak Republic",
                            }
                        ],
                    },
                    {
                        "surname": "Jadlovsky",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Technical University of Košice, Košice, Slovak Republic",
                                "organization": "Technical University of Košice",
                                "country": "Slovak Republic",
                            }
                        ],
                    },
                    {
                        "surname": "Jaffe",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Frankfurt Institute for Advanced Studies, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Frankfurt Institute for Advanced Studies",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Jahnke",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Universidade Estadual de Campinas (UNICAMP), Campinas, Brazil",
                                "organization": "Universidade Estadual de Campinas (UNICAMP)",
                                "country": "Brazil",
                            }
                        ],
                        "orcid": "0000-0003-1969-6960",
                    },
                    {
                        "surname": "Janik",
                        "given_names": "M.A.",
                        "affiliations": [
                            {
                                "value": "Warsaw University of Technology, Warsaw, Poland",
                                "organization": "Warsaw University of Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0001-9087-4665",
                    },
                    {
                        "surname": "Janson",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Johann-Wolfgang-Goethe Universität Frankfurt Institut für Informatik, Fachbereich Informatik und Mathematik, Frankfurt, Germany",
                                "organization": "Johann-Wolfgang-Goethe Universität Frankfurt Institut für Informatik",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Jercic",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Physics department, Faculty of science, University of Zagreb, Zagreb, Croatia",
                                "organization": "Physics department",
                                "country": "Croatia",
                            }
                        ],
                    },
                    {
                        "surname": "Jevons",
                        "given_names": "O.",
                        "affiliations": [
                            {
                                "value": "School of Physics and Astronomy, University of Birmingham, Birmingham, United Kingdom",
                                "organization": "School of Physics and Astronomy",
                                "country": "United Kingdom",
                            }
                        ],
                    },
                    {
                        "surname": "Jimenez",
                        "given_names": "A.A.P.",
                        "affiliations": [
                            {
                                "value": "Instituto de Ciencias Nucleares, Universidad Nacional Autónoma de México, Mexico City, Mexico",
                                "organization": "Instituto de Ciencias Nucleares",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0000-0002-7685-0808",
                    },
                    {
                        "surname": "Jonas",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Oak Ridge National Laboratory, Oak Ridge, TN, United States",
                                "organization": "Oak Ridge National Laboratory",
                                "country": "United States",
                            },
                            {
                                "value": "Westfälische Wilhelms-Universität Münster, Institut für Kernphysik, Münster, Germany",
                                "organization": "Westfälische Wilhelms-Universität Münster",
                                "country": "Germany",
                            },
                        ],
                        "orcid": "0000-0002-1605-5837",
                    },
                    {
                        "surname": "Jones",
                        "given_names": "P.G.",
                        "affiliations": [
                            {
                                "value": "School of Physics and Astronomy, University of Birmingham, Birmingham, United Kingdom",
                                "organization": "School of Physics and Astronomy",
                                "country": "United Kingdom",
                            }
                        ],
                    },
                    {
                        "surname": "Jowett",
                        "given_names": "J.M.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            },
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            },
                        ],
                        "orcid": "0000-0002-9492-3775",
                    },
                    {
                        "surname": "Jung",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-6811-5240",
                    },
                    {
                        "surname": "Jung",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0004-0872-2785",
                    },
                    {
                        "surname": "Junique",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0009-0002-4730-9489",
                    },
                    {
                        "surname": "Jusko",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "School of Physics and Astronomy, University of Birmingham, Birmingham, United Kingdom",
                                "organization": "School of Physics and Astronomy",
                                "country": "United Kingdom",
                            }
                        ],
                        "orcid": "0009-0009-3972-0631",
                    },
                    {
                        "surname": "Kabus",
                        "given_names": "M.J.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            },
                            {
                                "value": "Warsaw University of Technology, Warsaw, Poland",
                                "organization": "Warsaw University of Technology",
                                "country": "Poland",
                            },
                        ],
                        "orcid": "0000-0001-7602-1121",
                    },
                    {
                        "surname": "Kaewjai",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Suranaree University of Technology, Nakhon Ratchasima, Thailand",
                                "organization": "Suranaree University of Technology",
                                "country": "Thailand",
                            }
                        ],
                    },
                    {
                        "surname": "Kalinak",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Institute of Experimental Physics, Slovak Academy of Sciences, Košice, Slovak Republic",
                                "organization": "Institute of Experimental Physics",
                                "country": "Slovak Republic",
                            }
                        ],
                        "orcid": "0000-0002-0559-6697",
                    },
                    {
                        "surname": "Kalteyer",
                        "given_names": "A.S.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-0618-4843",
                    },
                    {
                        "surname": "Kalweit",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0001-6907-0486",
                    },
                    {
                        "surname": "Kaplin",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-1513-2845",
                    },
                    {
                        "surname": "Karasu Uysal",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "KTO Karatay University, Konya, Turkey",
                                "organization": "KTO Karatay University",
                                "country": "Turkey",
                            }
                        ],
                        "orcid": "0000-0001-6297-2532",
                    },
                    {
                        "surname": "Karatovic",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Physics department, Faculty of science, University of Zagreb, Zagreb, Croatia",
                                "organization": "Physics department",
                                "country": "Croatia",
                            }
                        ],
                        "orcid": "0000-0002-1726-5684",
                    },
                    {
                        "surname": "Karavichev",
                        "given_names": "O.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-5629-5181",
                    },
                    {
                        "surname": "Karavicheva",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-9355-6379",
                    },
                    {
                        "surname": "Karczmarczyk",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Warsaw University of Technology, Warsaw, Poland",
                                "organization": "Warsaw University of Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0002-9057-9719",
                    },
                    {
                        "surname": "Karpechev",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-6603-6693",
                    },
                    {
                        "surname": "Kashyap",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "National Institute of Science Education and Research, Homi Bhabha National Institute, Jatni, India",
                                "organization": "National Institute of Science Education and Research",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Kazantsev",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                    },
                    {
                        "surname": "Kebschull",
                        "given_names": "U.",
                        "affiliations": [
                            {
                                "value": "Johann-Wolfgang-Goethe Universität Frankfurt Institut für Informatik, Fachbereich Informatik und Mathematik, Frankfurt, Germany",
                                "organization": "Johann-Wolfgang-Goethe Universität Frankfurt Institut für Informatik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-1831-7957",
                    },
                    {
                        "surname": "Keidel",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Zentrum für Technologie und Transfer (ZTT), Worms, Germany",
                                "organization": "Zentrum für Technologie und Transfer (ZTT)",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-1474-6191",
                    },
                    {
                        "surname": "Keijdener",
                        "given_names": "D.L.D.",
                        "affiliations": [
                            {
                                "value": "Institute for Gravitational and Subatomic Physics (GRASP), Utrecht University/Nikhef, Utrecht, Netherlands",
                                "organization": "Institute for Gravitational and Subatomic Physics (GRASP)",
                                "country": "Netherlands",
                            }
                        ],
                    },
                    {
                        "surname": "Keil",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0009-0003-1055-0356",
                    },
                    {
                        "surname": "Ketzer",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Helmholtz-Institut für Strahlen- und Kernphysik, Rheinische Friedrich-Wilhelms-Universität Bonn, Bonn, Germany",
                                "organization": "Helmholtz-Institut für Strahlen- und Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-3493-3891",
                    },
                    {
                        "surname": "Khan",
                        "given_names": "A.M.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0001-6189-3242",
                    },
                    {
                        "surname": "Khan",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Aligarh Muslim University, Aligarh, India",
                                "organization": "Department of Physics",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0003-3075-2871",
                    },
                    {
                        "surname": "Khanzadeev",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-5741-7144",
                    },
                    {
                        "surname": "Kharlov",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0001-6653-6164",
                    },
                    {
                        "surname": "Khatun",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Aligarh Muslim University, Aligarh, India",
                                "organization": "Department of Physics",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-2724-668X",
                    },
                    {
                        "surname": "Khuntia",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "The Henryk Niewodniczanski Institute of Nuclear Physics, Polish Academy of Sciences, Cracow, Poland",
                                "organization": "The Henryk Niewodniczanski Institute of Nuclear Physics",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0003-0996-8547",
                    },
                    {
                        "surname": "Kileng",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Faculty of Engineering and Science, Western Norway University of Applied Sciences, Bergen, Norway",
                                "organization": "Faculty of Engineering and Science",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0009-0009-9098-9839",
                    },
                    {
                        "surname": "Kim",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Pusan National University, Pusan, Republic of Korea",
                                "organization": "Department of Physics",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0002-7504-2809",
                    },
                    {
                        "surname": "Kim",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Pusan National University, Pusan, Republic of Korea",
                                "organization": "Department of Physics",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0002-6434-7084",
                    },
                    {
                        "surname": "Kim",
                        "given_names": "D.J.",
                        "affiliations": [
                            {
                                "value": "University of Jyväskylä, Jyväskylä, Finland",
                                "organization": "University of Jyväskylä",
                                "country": "Finland",
                            }
                        ],
                        "orcid": "0000-0002-4816-283X",
                    },
                    {
                        "surname": "Kim",
                        "given_names": "E.J.",
                        "affiliations": [
                            {
                                "value": "Jeonbuk National University, Jeonju, Republic of Korea",
                                "organization": "Jeonbuk National University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0003-1433-6018",
                    },
                    {
                        "surname": "Kim",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Yonsei University, Seoul, Republic of Korea",
                                "organization": "Yonsei University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0009-0000-0438-5567",
                    },
                    {
                        "surname": "Kim",
                        "given_names": "J.S.",
                        "affiliations": [
                            {
                                "value": "Gangneung-Wonju National University, Gangneung, Republic of Korea",
                                "organization": "Gangneung-Wonju National University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0009-0006-7951-7118",
                    },
                    {
                        "surname": "Kim",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-9676-3309",
                    },
                    {
                        "surname": "Kim",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Jeonbuk National University, Jeonju, Republic of Korea",
                                "organization": "Jeonbuk National University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0003-0078-8398",
                    },
                    {
                        "surname": "Kim",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-0906-062X",
                    },
                    {
                        "surname": "Kim",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Sejong University, Seoul, Republic of Korea",
                                "organization": "Department of Physics",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0002-2102-7398",
                    },
                    {
                        "surname": "Kim",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Yonsei University, Seoul, Republic of Korea",
                                "organization": "Yonsei University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0003-4558-7856",
                    },
                    {
                        "surname": "Kirsch",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0003-8978-9852",
                    },
                    {
                        "surname": "Kisel",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Frankfurt Institute for Advanced Studies, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Frankfurt Institute for Advanced Studies",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-4808-419X",
                    },
                    {
                        "surname": "Kiselev",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-8354-7786",
                    },
                    {
                        "surname": "Kisiel",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Warsaw University of Technology, Warsaw, Poland",
                                "organization": "Warsaw University of Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0001-8322-9510",
                    },
                    {
                        "surname": "Kitowski",
                        "given_names": "J.P.",
                        "affiliations": [
                            {
                                "value": "AGH University of Science and Technology, Cracow, Poland",
                                "organization": "AGH University of Science and Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0003-3902-8310",
                    },
                    {
                        "surname": "Klay",
                        "given_names": "J.L.",
                        "affiliations": [
                            {
                                "value": "California Polytechnic State University, San Luis Obispo, CA, United States",
                                "organization": "California Polytechnic State University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-5592-0758",
                    },
                    {
                        "surname": "Klein",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-1301-1636",
                    },
                    {
                        "surname": "Klein",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Lawrence Berkeley National Laboratory, Berkeley, CA, United States",
                                "organization": "Lawrence Berkeley National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0003-2841-6553",
                    },
                    {
                        "surname": "Klein-Bösing",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Westfälische Wilhelms-Universität Münster, Institut für Kernphysik, Münster, Germany",
                                "organization": "Westfälische Wilhelms-Universität Münster",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-7285-3411",
                    },
                    {
                        "surname": "Kleiner",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0003-0133-319X",
                    },
                    {
                        "surname": "Klemenz",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-4116-7002",
                    },
                    {
                        "surname": "Kluge",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-6497-3974",
                    },
                    {
                        "surname": "Knospe",
                        "given_names": "A.G.",
                        "affiliations": [
                            {
                                "value": "University of Houston, Houston, TX, United States",
                                "organization": "University of Houston",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-2211-715X",
                    },
                    {
                        "surname": "Kobdaj",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Suranaree University of Technology, Nakhon Ratchasima, Thailand",
                                "organization": "Suranaree University of Technology",
                                "country": "Thailand",
                            }
                        ],
                        "orcid": "0000-0001-7296-5248",
                    },
                    {
                        "surname": "Kollegger",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Kondratyev",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0001-6203-9160",
                    },
                    {
                        "surname": "Kondratyeva",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0009-0001-5996-0685",
                    },
                    {
                        "surname": "Kondratyuk",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-9249-0435",
                    },
                    {
                        "surname": "Konig",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-8831-4009",
                    },
                    {
                        "surname": "Konigstorfer",
                        "given_names": "S.A.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-4824-2458",
                    },
                    {
                        "surname": "Konopka",
                        "given_names": "P.J.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0001-8738-7268",
                    },
                    {
                        "surname": "Kornakov",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Warsaw University of Technology, Warsaw, Poland",
                                "organization": "Warsaw University of Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0002-3652-6683",
                    },
                    {
                        "surname": "Koryciak",
                        "given_names": "S.D.",
                        "affiliations": [
                            {
                                "value": "AGH University of Science and Technology, Cracow, Poland",
                                "organization": "AGH University of Science and Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0001-6810-6897",
                    },
                    {
                        "surname": "Kotliarov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Nuclear Physics Institute of the Czech Academy of Sciences, Husinec-Řež, Czech Republic",
                                "organization": "Nuclear Physics Institute of the Czech Academy of Sciences",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0003-3576-4185",
                    },
                    {
                        "surname": "Kovalenko",
                        "given_names": "O.",
                        "affiliations": [
                            {
                                "value": "National Centre for Nuclear Research, Warsaw, Poland",
                                "organization": "National Centre for Nuclear Research",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0009-0005-8435-0001",
                    },
                    {
                        "surname": "Kovalenko",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0001-6012-6615",
                    },
                    {
                        "surname": "Kowalski",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "The Henryk Niewodniczanski Institute of Nuclear Physics, Polish Academy of Sciences, Cracow, Poland",
                                "organization": "The Henryk Niewodniczanski Institute of Nuclear Physics",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0002-7568-7498",
                    },
                    {
                        "surname": "Králik",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Institute of Experimental Physics, Slovak Academy of Sciences, Košice, Slovak Republic",
                                "organization": "Institute of Experimental Physics",
                                "country": "Slovak Republic",
                            }
                        ],
                        "orcid": "0000-0001-6441-9300",
                    },
                    {
                        "surname": "Kravčáková",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Faculty of Science, P.J. Šafárik University, Košice, Slovak Republic",
                                "organization": "Faculty of Science",
                                "country": "Slovak Republic",
                            }
                        ],
                        "orcid": "0000-0002-1381-3436",
                    },
                    {
                        "surname": "Kreis",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Krivda",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "School of Physics and Astronomy, University of Birmingham, Birmingham, United Kingdom",
                                "organization": "School of Physics and Astronomy",
                                "country": "United Kingdom",
                            },
                            {
                                "value": "Institute of Experimental Physics, Slovak Academy of Sciences, Košice, Slovak Republic",
                                "organization": "Institute of Experimental Physics",
                                "country": "Slovak Republic",
                            },
                        ],
                        "orcid": "0000-0001-5091-4159",
                    },
                    {
                        "surname": "Krizek",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Nuclear Physics Institute of the Czech Academy of Sciences, Husinec-Řež, Czech Republic",
                                "organization": "Nuclear Physics Institute of the Czech Academy of Sciences",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0001-6593-4574",
                    },
                    {
                        "surname": "Krizkova Gajdosova",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "Faculty of Nuclear Sciences and Physical Engineering, Czech Technical University in Prague, Prague, Czech Republic",
                                "organization": "Faculty of Nuclear Sciences and Physical Engineering",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0002-5569-1254",
                    },
                    {
                        "surname": "Kroesen",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0001-6795-6109",
                    },
                    {
                        "surname": "Krüger",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-7174-6617",
                    },
                    {
                        "surname": "Krupova",
                        "given_names": "D.M.",
                        "affiliations": [
                            {
                                "value": "Faculty of Nuclear Sciences and Physical Engineering, Czech Technical University in Prague, Prague, Czech Republic",
                                "organization": "Faculty of Nuclear Sciences and Physical Engineering",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0002-1706-4428",
                    },
                    {
                        "surname": "Kryshen",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-2197-4109",
                    },
                    {
                        "surname": "Krzewicki",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Frankfurt Institute for Advanced Studies, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Frankfurt Institute for Advanced Studies",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Kučera",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-3567-5177",
                    },
                    {
                        "surname": "Kuhn",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Université de Strasbourg, CNRS, IPHC UMR 7178, F-67000 Strasbourg, France",
                                "organization": "Université de Strasbourg",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-7998-5046",
                    },
                    {
                        "surname": "Kuijer",
                        "given_names": "P.G.",
                        "affiliations": [
                            {
                                "value": "Nikhef, National institute for subatomic physics, Amsterdam, Netherlands",
                                "organization": "Nikhef, National institute for subatomic physics",
                                "country": "Netherlands",
                            }
                        ],
                        "orcid": "0000-0002-6987-2048",
                    },
                    {
                        "surname": "Kumaoka",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "University of Tsukuba, Tsukuba, Japan",
                                "organization": "University of Tsukuba",
                                "country": "Japan",
                            }
                        ],
                    },
                    {
                        "surname": "Kumar",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Variable Energy Cyclotron Centre, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Variable Energy Cyclotron Centre",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Kumar",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Physics Department, Panjab University, Chandigarh, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-2746-9840",
                    },
                    {
                        "surname": "Kumar",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Physics Department, Panjab University, Chandigarh, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Kundu",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0003-3150-2831",
                    },
                    {
                        "surname": "Kurashvili",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "National Centre for Nuclear Research, Warsaw, Poland",
                                "organization": "National Centre for Nuclear Research",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0002-0613-5278",
                    },
                    {
                        "surname": "Kurepin",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0001-7672-2067",
                    },
                    {
                        "surname": "Kurepin",
                        "given_names": "A.B.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-1851-4136",
                    },
                    {
                        "surname": "Kushpil",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Nuclear Physics Institute of the Czech Academy of Sciences, Husinec-Řež, Czech Republic",
                                "organization": "Nuclear Physics Institute of the Czech Academy of Sciences",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0001-9289-2840",
                    },
                    {
                        "surname": "Kvapil",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "School of Physics and Astronomy, University of Birmingham, Birmingham, United Kingdom",
                                "organization": "School of Physics and Astronomy",
                                "country": "United Kingdom",
                            }
                        ],
                        "orcid": "0000-0002-0298-9073",
                    },
                    {
                        "surname": "Kweon",
                        "given_names": "M.J.",
                        "affiliations": [
                            {
                                "value": "Inha University, Incheon, Republic of Korea",
                                "organization": "Inha University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0002-8958-4190",
                    },
                    {
                        "surname": "Kwon",
                        "given_names": "J.Y.",
                        "affiliations": [
                            {
                                "value": "Inha University, Incheon, Republic of Korea",
                                "organization": "Inha University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0002-6586-9300",
                    },
                    {
                        "surname": "Kwon",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Yonsei University, Seoul, Republic of Korea",
                                "organization": "Yonsei University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0009-0001-4180-0413",
                    },
                    {
                        "surname": "La Pointe",
                        "given_names": "S.L.",
                        "affiliations": [
                            {
                                "value": "Frankfurt Institute for Advanced Studies, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Frankfurt Institute for Advanced Studies",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-5267-0140",
                    },
                    {
                        "surname": "La Rocca",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Catania, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-7291-8166",
                    },
                    {
                        "surname": "Lai",
                        "given_names": "Y.S.",
                        "affiliations": [
                            {
                                "value": "Lawrence Berkeley National Laboratory, Berkeley, CA, United States",
                                "organization": "Lawrence Berkeley National Laboratory",
                                "country": "United States",
                            }
                        ],
                    },
                    {
                        "surname": "Lakrathok",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Suranaree University of Technology, Nakhon Ratchasima, Thailand",
                                "organization": "Suranaree University of Technology",
                                "country": "Thailand",
                            }
                        ],
                    },
                    {
                        "surname": "Lamanna",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0009-0006-1840-462X",
                    },
                    {
                        "surname": "Langoy",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "University of South-Eastern Norway, Kongsberg, Norway",
                                "organization": "University of South-Eastern Norway",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0000-0001-9471-1804",
                    },
                    {
                        "surname": "Larionov",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "INFN, Laboratori Nazionali di Frascati, Frascati, Italy",
                                "organization": "INFN, Laboratori Nazionali di Frascati",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-5489-3751",
                    },
                    {
                        "surname": "Laudi",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0009-0006-8424-015X",
                    },
                    {
                        "surname": "Lautner",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            },
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            },
                        ],
                        "orcid": "0000-0002-7017-4183",
                    },
                    {
                        "surname": "Lavicka",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Stefan Meyer Institut für Subatomare Physik (SMI), Vienna, Austria",
                                "organization": "Stefan Meyer Institut für Subatomare Physik (SMI)",
                                "country": "Austria",
                            }
                        ],
                        "orcid": "0000-0002-8384-0384",
                    },
                    {
                        "surname": "Lazareva",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-8068-8786",
                    },
                    {
                        "surname": "Lea",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Università di Brescia, Brescia, Italy",
                                "organization": "Università di Brescia",
                                "country": "Italy",
                            },
                            {
                                "value": "INFN, Sezione di Pavia, Pavia, Italy",
                                "organization": "INFN, Sezione di Pavia",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0001-5955-0769",
                    },
                    {
                        "surname": "Lehrbach",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Frankfurt Institute for Advanced Studies, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Frankfurt Institute for Advanced Studies",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0001-3545-3275",
                    },
                    {
                        "surname": "Lemmon",
                        "given_names": "R.C.",
                        "affiliations": [
                            {
                                "value": "Nuclear Physics Group, STFC Daresbury Laboratory, Daresbury, United Kingdom",
                                "organization": "Nuclear Physics Group",
                                "country": "United Kingdom",
                            }
                        ],
                        "orcid": "0000-0002-1259-979X",
                    },
                    {
                        "surname": "León Monzón",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Universidad Autónoma de Sinaloa, Culiacán, Mexico",
                                "organization": "Universidad Autónoma de Sinaloa",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0000-0002-7919-2150",
                    },
                    {
                        "surname": "Lesch",
                        "given_names": "M.M.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-7480-7558",
                    },
                    {
                        "surname": "Lesser",
                        "given_names": "E.D.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, University of California, Berkeley, CA, United States",
                                "organization": "Department of Physics",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0001-8367-8703",
                    },
                    {
                        "surname": "Lettrich",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Lévai",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Wigner Research Centre for Physics, Budapest, Hungary",
                                "organization": "Wigner Research Centre for Physics",
                                "country": "Hungary",
                            }
                        ],
                        "orcid": "0009-0006-9345-9620",
                    },
                    {
                        "surname": "Li",
                        "given_names": "X.",
                        "affiliations": [
                            {
                                "value": "China Institute of Atomic Energy, Beijing, China",
                                "organization": "China Institute of Atomic Energy",
                                "country": "China",
                            }
                        ],
                    },
                    {
                        "surname": "Li",
                        "given_names": "X.L.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                    },
                    {
                        "surname": "Lien",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "University of South-Eastern Norway, Kongsberg, Norway",
                                "organization": "University of South-Eastern Norway",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0000-0002-0425-9138",
                    },
                    {
                        "surname": "Lietava",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "School of Physics and Astronomy, University of Birmingham, Birmingham, United Kingdom",
                                "organization": "School of Physics and Astronomy",
                                "country": "United Kingdom",
                            }
                        ],
                        "orcid": "0000-0002-9188-9428",
                    },
                    {
                        "surname": "Lim",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Pusan National University, Pusan, Republic of Korea",
                                "organization": "Department of Physics",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0002-1904-296X",
                    },
                    {
                        "surname": "Lim",
                        "given_names": "S.H.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Pusan National University, Pusan, Republic of Korea",
                                "organization": "Department of Physics",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0001-6335-7427",
                    },
                    {
                        "surname": "Lindenstruth",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Frankfurt Institute for Advanced Studies, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Frankfurt Institute for Advanced Studies",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0006-7301-988X",
                    },
                    {
                        "surname": "Lindner",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Horia Hulubei National Institute of Physics and Nuclear Engineering, Bucharest, Romania",
                                "organization": "Horia Hulubei National Institute of Physics and Nuclear Engineering",
                                "country": "Romania",
                            }
                        ],
                    },
                    {
                        "surname": "Lippmann",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-0062-0536",
                    },
                    {
                        "surname": "Liu",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, University of California, Berkeley, CA, United States",
                                "organization": "Department of Physics",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0001-6895-4829",
                    },
                    {
                        "surname": "Liu",
                        "given_names": "D.H.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0009-0006-6383-6069",
                    },
                    {
                        "surname": "Liu",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "University of Liverpool, Liverpool, United Kingdom",
                                "organization": "University of Liverpool",
                                "country": "United Kingdom",
                            }
                        ],
                        "orcid": "0000-0002-8397-7620",
                    },
                    {
                        "surname": "Lofnes",
                        "given_names": "I.M.",
                        "affiliations": [
                            {
                                "value": "Department of Physics and Technology, University of Bergen, Bergen, Norway",
                                "organization": "Department of Physics and Technology",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0000-0002-9063-1599",
                    },
                    {
                        "surname": "Loginov",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                    },
                    {
                        "surname": "Loizides",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Oak Ridge National Laboratory, Oak Ridge, TN, United States",
                                "organization": "Oak Ridge National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0001-8635-8465",
                    },
                    {
                        "surname": "Loncar",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Faculty of Electrical Engineering, Mechanical Engineering and Naval Architecture, University of Split, Split, Croatia",
                                "organization": "Faculty of Electrical Engineering, Mechanical Engineering and Naval Architecture",
                                "country": "Croatia",
                            }
                        ],
                        "orcid": "0000-0001-6486-2230",
                    },
                    {
                        "surname": "Lopez",
                        "given_names": "J.A.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-5648-4206",
                    },
                    {
                        "surname": "Lopez",
                        "given_names": "X.",
                        "affiliations": [
                            {
                                "value": "Université Clermont Auvergne, CNRS/IN2P3, LPC, Clermont-Ferrand, France",
                                "organization": "Université Clermont Auvergne",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0001-8159-8603",
                    },
                    {
                        "surname": "López Torres",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Centro de Aplicaciones Tecnológicas y Desarrollo Nuclear (CEADEN), Havana, Cuba",
                                "organization": "Centro de Aplicaciones Tecnológicas y Desarrollo Nuclear (CEADEN)",
                                "country": "Cuba",
                            }
                        ],
                        "orcid": "0000-0002-2850-4222",
                    },
                    {
                        "surname": "Lu",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            },
                            {
                                "value": "University of Science and Technology of China, Hefei, China",
                                "organization": "University of Science and Technology of China",
                                "country": "China",
                            },
                        ],
                        "orcid": "0000-0002-7002-0061",
                    },
                    {
                        "surname": "Luhder",
                        "given_names": "J.R.",
                        "affiliations": [
                            {
                                "value": "Westfälische Wilhelms-Universität Münster, Institut für Kernphysik, Münster, Germany",
                                "organization": "Westfälische Wilhelms-Universität Münster",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0006-1802-5857",
                    },
                    {
                        "surname": "Lunardon",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Padova, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-6027-0024",
                    },
                    {
                        "surname": "Luparello",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Trieste, Trieste, Italy",
                                "organization": "INFN, Sezione di Trieste",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-9901-2014",
                    },
                    {
                        "surname": "Ma",
                        "given_names": "Y.G.",
                        "affiliations": [
                            {
                                "value": "Fudan University, Shanghai, China",
                                "organization": "Fudan University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0002-0233-9900",
                    },
                    {
                        "surname": "Maevskaya",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                    },
                    {
                        "surname": "Mager",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0009-0002-2291-691X",
                    },
                    {
                        "surname": "Mahmoud",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Helmholtz-Institut für Strahlen- und Kernphysik, Rheinische Friedrich-Wilhelms-Universität Bonn, Bonn, Germany",
                                "organization": "Helmholtz-Institut für Strahlen- und Kernphysik",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Maire",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Université de Strasbourg, CNRS, IPHC UMR 7178, F-67000 Strasbourg, France",
                                "organization": "Université de Strasbourg",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-4831-2367",
                    },
                    {
                        "surname": "Malaev",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0009-0001-9974-0169",
                    },
                    {
                        "surname": "Malik",
                        "given_names": "N.M.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Jammu, Jammu, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0001-5682-0903",
                    },
                    {
                        "surname": "Malik",
                        "given_names": "Q.W.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, University of Oslo, Oslo, Norway",
                                "organization": "Department of Physics",
                                "country": "Norway",
                            }
                        ],
                    },
                    {
                        "surname": "Malik",
                        "given_names": "S.K.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Jammu, Jammu, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0003-0311-9552",
                    },
                    {
                        "surname": "Malinina",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0003-1723-4121",
                    },
                    {
                        "surname": "Mal'Kevich",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-6683-7626",
                    },
                    {
                        "surname": "Mallick",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "National Institute of Science Education and Research, Homi Bhabha National Institute, Jatni, India",
                                "organization": "National Institute of Science Education and Research",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-4256-052X",
                    },
                    {
                        "surname": "Mallick",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Indore, Indore, India",
                                "organization": "Indian Institute of Technology Indore",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0003-2706-1025",
                    },
                    {
                        "surname": "Mandaglio",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Scienze MIFT, Università di Messina, Messina, Italy",
                                "organization": "Dipartimento di Scienze MIFT",
                                "country": "Italy",
                            },
                            {
                                "value": "INFN, Sezione di Catania, Catania, Italy",
                                "organization": "INFN, Sezione di Catania",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0003-4486-4807",
                    },
                    {
                        "surname": "Manko",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-4772-3615",
                    },
                    {
                        "surname": "Manso",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Université Clermont Auvergne, CNRS/IN2P3, LPC, Clermont-Ferrand, France",
                                "organization": "Université Clermont Auvergne",
                                "country": "France",
                            }
                        ],
                        "orcid": "0009-0008-5115-943X",
                    },
                    {
                        "surname": "Manzari",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bari, Bari, Italy",
                                "organization": "INFN, Sezione di Bari",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-3102-1504",
                    },
                    {
                        "surname": "Mao",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0002-0786-8545",
                    },
                    {
                        "surname": "Margagliotti",
                        "given_names": "G.V.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Trieste, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-1965-7953",
                    },
                    {
                        "surname": "Margotti",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bologna, Bologna, Italy",
                                "organization": "INFN, Sezione di Bologna",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-2146-0391",
                    },
                    {
                        "surname": "Marín",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-9069-0353",
                    },
                    {
                        "surname": "Markert",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "The University of Texas at Austin, Austin, TX, United States",
                                "organization": "The University of Texas at Austin",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0001-9675-4322",
                    },
                    {
                        "surname": "Marquard",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Martin",
                        "given_names": "N.A.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Martinengo",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0003-0288-202X",
                    },
                    {
                        "surname": "Martinez",
                        "given_names": "J.L.",
                        "affiliations": [
                            {
                                "value": "University of Houston, Houston, TX, United States",
                                "organization": "University of Houston",
                                "country": "United States",
                            }
                        ],
                    },
                    {
                        "surname": "Martínez",
                        "given_names": "M.I.",
                        "affiliations": [
                            {
                                "value": "High Energy Physics Group, Universidad Autónoma de Puebla, Puebla, Mexico",
                                "organization": "High Energy Physics Group",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0000-0002-8503-3009",
                    },
                    {
                        "surname": "Martínez García",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "SUBATECH, IMT Atlantique, Nantes Université, CNRS-IN2P3, Nantes, France",
                                "organization": "SUBATECH",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-8657-6742",
                    },
                    {
                        "surname": "Masciocchi",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-2064-6517",
                    },
                    {
                        "surname": "Masera",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-1880-5467",
                    },
                    {
                        "surname": "Masoni",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Cagliari, Cagliari, Italy",
                                "organization": "INFN, Sezione di Cagliari",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-2699-1522",
                    },
                    {
                        "surname": "Massacrier",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie, Orsay, France",
                                "organization": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-5475-5092",
                    },
                    {
                        "surname": "Mastroserio",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Università degli Studi di Foggia, Foggia, Italy",
                                "organization": "Università degli Studi di Foggia",
                                "country": "Italy",
                            },
                            {
                                "value": "INFN, Sezione di Bari, Bari, Italy",
                                "organization": "INFN, Sezione di Bari",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0003-3711-8902",
                    },
                    {
                        "surname": "Mathis",
                        "given_names": "A.M.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-7604-9116",
                    },
                    {
                        "surname": "Matonoha",
                        "given_names": "O.",
                        "affiliations": [
                            {
                                "value": "Lund University Department of Physics, Division of Particle Physics, Lund, Sweden",
                                "organization": "Lund University Department of Physics",
                                "country": "Sweden",
                            }
                        ],
                        "orcid": "0000-0002-0015-9367",
                    },
                    {
                        "surname": "Matuoka",
                        "given_names": "P.F.T.",
                        "affiliations": [
                            {
                                "value": "Universidade de São Paulo (USP), São Paulo, Brazil",
                                "organization": "Universidade de São Paulo (USP)",
                                "country": "Brazil",
                            }
                        ],
                    },
                    {
                        "surname": "Matyja",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "The Henryk Niewodniczanski Institute of Nuclear Physics, Polish Academy of Sciences, Cracow, Poland",
                                "organization": "The Henryk Niewodniczanski Institute of Nuclear Physics",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0002-4524-563X",
                    },
                    {
                        "surname": "Mayer",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "The Henryk Niewodniczanski Institute of Nuclear Physics, Polish Academy of Sciences, Cracow, Poland",
                                "organization": "The Henryk Niewodniczanski Institute of Nuclear Physics",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0003-2570-8278",
                    },
                    {
                        "surname": "Mazuecos",
                        "given_names": "A.L.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0009-0009-7230-3792",
                    },
                    {
                        "surname": "Mazzaschi",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-2613-2901",
                    },
                    {
                        "surname": "Mazzilli",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-1415-4559",
                    },
                    {
                        "surname": "Mdhluli",
                        "given_names": "J.E.",
                        "affiliations": [
                            {
                                "value": "University of the Witwatersrand, Johannesburg, South Africa",
                                "organization": "University of the Witwatersrand",
                                "country": "South Africa",
                            }
                        ],
                        "orcid": "0000-0002-9745-0504",
                    },
                    {
                        "surname": "Mechler",
                        "given_names": "A.F.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Melikyan",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-4165-505X",
                    },
                    {
                        "surname": "Menchaca-Rocha",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Instituto de Física, Universidad Nacional Autónoma de México, Mexico City, Mexico",
                                "organization": "Instituto de Física",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0000-0002-4856-8055",
                    },
                    {
                        "surname": "Meninno",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Stefan Meyer Institut für Subatomare Physik (SMI), Vienna, Austria",
                                "organization": "Stefan Meyer Institut für Subatomare Physik (SMI)",
                                "country": "Austria",
                            },
                            {
                                "value": "Dipartimento di Fisica ‘E.R. Caianiello’ dell'Università and Gruppo Collegato INFN, Salerno, Italy",
                                "organization": "Dipartimento di Fisica ‘E.R. Caianiello’ dell'Università",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0003-4389-7711",
                    },
                    {
                        "surname": "Menon",
                        "given_names": "A.S.",
                        "affiliations": [
                            {
                                "value": "University of Houston, Houston, TX, United States",
                                "organization": "University of Houston",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0009-0003-3911-1744",
                    },
                    {
                        "surname": "Meres",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Comenius University Bratislava, Faculty of Mathematics, Physics and Informatics, Bratislava, Slovak Republic",
                                "organization": "Comenius University Bratislava",
                                "country": "Slovak Republic",
                            }
                        ],
                        "orcid": "0009-0005-3106-8571",
                    },
                    {
                        "surname": "Mhlanga",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "University of Cape Town, Cape Town, South Africa",
                                "organization": "University of Cape Town",
                                "country": "South Africa",
                            },
                            {
                                "value": "iThemba LABS, National Research Foundation, Somerset West, South Africa",
                                "organization": "iThemba LABS",
                                "country": "South Africa",
                            },
                        ],
                    },
                    {
                        "surname": "Miake",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "University of Tsukuba, Tsukuba, Japan",
                                "organization": "University of Tsukuba",
                                "country": "Japan",
                            }
                        ],
                    },
                    {
                        "surname": "Micheletti",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Torino, Turin, Italy",
                                "organization": "INFN, Sezione di Torino",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-1430-6655",
                    },
                    {
                        "surname": "Migliorin",
                        "given_names": "L.C.",
                        "affiliations": [
                            {
                                "value": "Université de Lyon, CNRS/IN2P3, Institut de Physique des 2 Infinis de Lyon, Lyon, France",
                                "organization": "Université de Lyon",
                                "country": "France",
                            }
                        ],
                    },
                    {
                        "surname": "Mihaylov",
                        "given_names": "D.L.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0004-2669-5696",
                    },
                    {
                        "surname": "Mikhaylov",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN"
                            },
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            },
                        ],
                        "orcid": "0000-0002-6726-6407",
                    },
                    {
                        "surname": "Mishra",
                        "given_names": "A.N.",
                        "affiliations": [
                            {
                                "value": "Wigner Research Centre for Physics, Budapest, Hungary",
                                "organization": "Wigner Research Centre for Physics",
                                "country": "Hungary",
                            }
                        ],
                        "orcid": "0000-0002-3892-2719",
                    },
                    {
                        "surname": "Miśkowiec",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-8627-9721",
                    },
                    {
                        "surname": "Modak",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Bose Institute, Department of Physics and Centre for Astroparticle Physics and Space Science (CAPSS), Kolkata, India",
                                "organization": "Bose Institute",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0003-3056-8353",
                    },
                    {
                        "surname": "Mohanty",
                        "given_names": "A.P.",
                        "affiliations": [
                            {
                                "value": "Institute for Gravitational and Subatomic Physics (GRASP), Utrecht University/Nikhef, Utrecht, Netherlands",
                                "organization": "Institute for Gravitational and Subatomic Physics (GRASP)",
                                "country": "Netherlands",
                            }
                        ],
                        "orcid": "0000-0002-7634-8949",
                    },
                    {
                        "surname": "Mohanty",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "National Institute of Science Education and Research, Homi Bhabha National Institute, Jatni, India",
                                "organization": "National Institute of Science Education and Research",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Mohisin Khan",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Aligarh Muslim University, Aligarh, India",
                                "organization": "Department of Physics",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-4767-1464",
                    },
                    {
                        "surname": "Molander",
                        "given_names": "M.A.",
                        "affiliations": [
                            {
                                "value": "Helsinki Institute of Physics (HIP), Helsinki, Finland",
                                "organization": "Helsinki Institute of Physics (HIP)",
                                "country": "Finland",
                            }
                        ],
                        "orcid": "0000-0003-2845-8702",
                    },
                    {
                        "surname": "Moravcova",
                        "given_names": "Z.",
                        "affiliations": [
                            {
                                "value": "Niels Bohr Institute, University of Copenhagen, Copenhagen, Denmark",
                                "organization": "Niels Bohr Institute",
                                "country": "Denmark",
                            }
                        ],
                        "orcid": "0000-0002-4512-1645",
                    },
                    {
                        "surname": "Mordasini",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-3265-9614",
                    },
                    {
                        "surname": "Moreira De Godoy",
                        "given_names": "D.A.",
                        "affiliations": [
                            {
                                "value": "Westfälische Wilhelms-Universität Münster, Institut für Kernphysik, Münster, Germany",
                                "organization": "Westfälische Wilhelms-Universität Münster",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-3941-7607",
                    },
                    {
                        "surname": "Morozov",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0001-7286-4543",
                    },
                    {
                        "surname": "Morsch",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-3276-0464",
                    },
                    {
                        "surname": "Mrnjavac",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0003-1281-8291",
                    },
                    {
                        "surname": "Muccifora",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "INFN, Laboratori Nazionali di Frascati, Frascati, Italy",
                                "organization": "INFN, Laboratori Nazionali di Frascati",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-5624-6486",
                    },
                    {
                        "surname": "Mudnic",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Faculty of Electrical Engineering, Mechanical Engineering and Naval Architecture, University of Split, Split, Croatia",
                                "organization": "Faculty of Electrical Engineering, Mechanical Engineering and Naval Architecture",
                                "country": "Croatia",
                            }
                        ],
                    },
                    {
                        "surname": "Muhuri",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Variable Energy Cyclotron Centre, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Variable Energy Cyclotron Centre",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0003-2378-9553",
                    },
                    {
                        "surname": "Mulligan",
                        "given_names": "J.D.",
                        "affiliations": [
                            {
                                "value": "Lawrence Berkeley National Laboratory, Berkeley, CA, United States",
                                "organization": "Lawrence Berkeley National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-6905-4352",
                    },
                    {
                        "surname": "Mulliri",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Cagliari, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                    },
                    {
                        "surname": "Munhoz",
                        "given_names": "M.G.",
                        "affiliations": [
                            {
                                "value": "Universidade de São Paulo (USP), São Paulo, Brazil",
                                "organization": "Universidade de São Paulo (USP)",
                                "country": "Brazil",
                            }
                        ],
                        "orcid": "0000-0003-3695-3180",
                    },
                    {
                        "surname": "Munzer",
                        "given_names": "R.H.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-8334-6933",
                    },
                    {
                        "surname": "Murakami",
                        "given_names": "H.",
                        "affiliations": [
                            {
                                "value": "University of Tokyo, Tokyo, Japan",
                                "organization": "University of Tokyo",
                                "country": "Japan",
                            }
                        ],
                        "orcid": "0000-0001-6548-6775",
                    },
                    {
                        "surname": "Murray",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "University of Cape Town, Cape Town, South Africa",
                                "organization": "University of Cape Town",
                                "country": "South Africa",
                            }
                        ],
                        "orcid": "0000-0003-0548-588X",
                    },
                    {
                        "surname": "Musa",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0001-8814-2254",
                    },
                    {
                        "surname": "Musinsky",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Institute of Experimental Physics, Slovak Academy of Sciences, Košice, Slovak Republic",
                                "organization": "Institute of Experimental Physics",
                                "country": "Slovak Republic",
                            }
                        ],
                        "orcid": "0000-0002-5729-4535",
                    },
                    {
                        "surname": "Myrcha",
                        "given_names": "J.W.",
                        "affiliations": [
                            {
                                "value": "Warsaw University of Technology, Warsaw, Poland",
                                "organization": "Warsaw University of Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0001-8506-2275",
                    },
                    {
                        "surname": "Naik",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "University of the Witwatersrand, Johannesburg, South Africa",
                                "organization": "University of the Witwatersrand",
                                "country": "South Africa",
                            }
                        ],
                        "orcid": "0000-0002-0172-6976",
                    },
                    {
                        "surname": "Nair",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "National Centre for Nuclear Research, Warsaw, Poland",
                                "organization": "National Centre for Nuclear Research",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0001-8326-9846",
                    },
                    {
                        "surname": "Nandi",
                        "given_names": "B.K.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Bombay (IIT), Mumbai, India",
                                "organization": "Indian Institute of Technology Bombay (IIT)",
                                "country": "India",
                            }
                        ],
                        "orcid": "0009-0007-3988-5095",
                    },
                    {
                        "surname": "Nania",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bologna, Bologna, Italy",
                                "organization": "INFN, Sezione di Bologna",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-6039-190X",
                    },
                    {
                        "surname": "Nappi",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bari, Bari, Italy",
                                "organization": "INFN, Sezione di Bari",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-2080-9010",
                    },
                    {
                        "surname": "Nassirpour",
                        "given_names": "A.F.",
                        "affiliations": [
                            {
                                "value": "Lund University Department of Physics, Division of Particle Physics, Lund, Sweden",
                                "organization": "Lund University Department of Physics",
                                "country": "Sweden",
                            }
                        ],
                        "orcid": "0000-0001-8927-2798",
                    },
                    {
                        "surname": "Nath",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0005-1524-5654",
                    },
                    {
                        "surname": "Nattrass",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "University of Tennessee, Knoxville, TN, United States",
                                "organization": "University of Tennessee",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-8768-6468",
                    },
                    {
                        "surname": "Neagu",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, University of Oslo, Oslo, Norway",
                                "organization": "Department of Physics",
                                "country": "Norway",
                            }
                        ],
                    },
                    {
                        "surname": "Negru",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "University Politehnica of Bucharest, Bucharest, Romania",
                                "organization": "University Politehnica of Bucharest",
                                "country": "Romania",
                            }
                        ],
                    },
                    {
                        "surname": "Nellen",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Instituto de Ciencias Nucleares, Universidad Nacional Autónoma de México, Mexico City, Mexico",
                                "organization": "Instituto de Ciencias Nucleares",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0000-0003-1059-8731",
                    },
                    {
                        "surname": "Nesbo",
                        "given_names": "S.V.",
                        "affiliations": [
                            {
                                "value": "Faculty of Engineering and Science, Western Norway University of Applied Sciences, Bergen, Norway",
                                "organization": "Faculty of Engineering and Science",
                                "country": "Norway",
                            }
                        ],
                    },
                    {
                        "surname": "Neskovic",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Frankfurt Institute for Advanced Studies, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Frankfurt Institute for Advanced Studies",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-8585-7991",
                    },
                    {
                        "surname": "Nesterov",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0009-0008-6321-4889",
                    },
                    {
                        "surname": "Nielsen",
                        "given_names": "B.S.",
                        "affiliations": [
                            {
                                "value": "Niels Bohr Institute, University of Copenhagen, Copenhagen, Denmark",
                                "organization": "Niels Bohr Institute",
                                "country": "Denmark",
                            }
                        ],
                        "orcid": "0000-0002-0091-1934",
                    },
                    {
                        "surname": "Nielsen",
                        "given_names": "E.G.",
                        "affiliations": [
                            {
                                "value": "Niels Bohr Institute, University of Copenhagen, Copenhagen, Denmark",
                                "organization": "Niels Bohr Institute",
                                "country": "Denmark",
                            }
                        ],
                        "orcid": "0000-0002-9394-1066",
                    },
                    {
                        "surname": "Nikolaev",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0003-1242-4866",
                    },
                    {
                        "surname": "Nikulin",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0001-8573-0851",
                    },
                    {
                        "surname": "Nikulin",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-4826-6516",
                    },
                    {
                        "surname": "Noferini",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bologna, Bologna, Italy",
                                "organization": "INFN, Sezione di Bologna",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-6704-0256",
                    },
                    {
                        "surname": "Noh",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Chungbuk National University, Cheongju, Republic of Korea",
                                "organization": "Chungbuk National University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0001-6104-1752",
                    },
                    {
                        "surname": "Nomokonov",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0009-0002-1220-1443",
                    },
                    {
                        "surname": "Norman",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "University of Liverpool, Liverpool, United Kingdom",
                                "organization": "University of Liverpool",
                                "country": "United Kingdom",
                            }
                        ],
                        "orcid": "0000-0002-3783-5760",
                    },
                    {
                        "surname": "Novitzky",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "University of Tsukuba, Tsukuba, Japan",
                                "organization": "University of Tsukuba",
                                "country": "Japan",
                            }
                        ],
                        "orcid": "0000-0002-9609-566X",
                    },
                    {
                        "surname": "Nowakowski",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Warsaw University of Technology, Warsaw, Poland",
                                "organization": "Warsaw University of Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0001-8971-0874",
                    },
                    {
                        "surname": "Nyanin",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-7877-2006",
                    },
                    {
                        "surname": "Nystrand",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Department of Physics and Technology, University of Bergen, Bergen, Norway",
                                "organization": "Department of Physics and Technology",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0009-0005-4425-586X",
                    },
                    {
                        "surname": "Ogino",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Nagasaki Institute of Applied Science, Nagasaki, Japan",
                                "organization": "Nagasaki Institute of Applied Science",
                                "country": "Japan",
                            }
                        ],
                        "orcid": "0000-0003-3390-2804",
                    },
                    {
                        "surname": "Ohlson",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Lund University Department of Physics, Division of Particle Physics, Lund, Sweden",
                                "organization": "Lund University Department of Physics",
                                "country": "Sweden",
                            }
                        ],
                        "orcid": "0000-0002-4214-5844",
                    },
                    {
                        "surname": "Okorokov",
                        "given_names": "V.A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-7162-5345",
                    },
                    {
                        "surname": "Oleniacz",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Warsaw University of Technology, Warsaw, Poland",
                                "organization": "Warsaw University of Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0003-2966-4903",
                    },
                    {
                        "surname": "Oliveira Da Silva",
                        "given_names": "A.C.",
                        "affiliations": [
                            {
                                "value": "University of Tennessee, Knoxville, TN, United States",
                                "organization": "University of Tennessee",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-9421-5568",
                    },
                    {
                        "surname": "Oliver",
                        "given_names": "M.H.",
                        "affiliations": [
                            {
                                "value": "Yale University, New Haven, CT, United States",
                                "organization": "Yale University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0001-5241-6735",
                    },
                    {
                        "surname": "Onnerstad",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "University of Jyväskylä, Jyväskylä, Finland",
                                "organization": "University of Jyväskylä",
                                "country": "Finland",
                            }
                        ],
                        "orcid": "0000-0002-8848-1800",
                    },
                    {
                        "surname": "Oppedisano",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Torino, Turin, Italy",
                                "organization": "INFN, Sezione di Torino",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-6194-4601",
                    },
                    {
                        "surname": "Ortiz Velasquez",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Instituto de Ciencias Nucleares, Universidad Nacional Autónoma de México, Mexico City, Mexico",
                                "organization": "Instituto de Ciencias Nucleares",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0000-0002-4788-7943",
                    },
                    {
                        "surname": "Oskarsson",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Lund University Department of Physics, Division of Particle Physics, Lund, Sweden",
                                "organization": "Lund University Department of Physics",
                                "country": "Sweden",
                            }
                        ],
                    },
                    {
                        "surname": "Otwinowski",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "The Henryk Niewodniczanski Institute of Nuclear Physics, Polish Academy of Sciences, Cracow, Poland",
                                "organization": "The Henryk Niewodniczanski Institute of Nuclear Physics",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0002-5471-6595",
                    },
                    {
                        "surname": "Oya",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Physics Program and International Institute for Sustainability with Knotted Chiral Meta Matter (SKCM2), Hiroshima University, Hiroshima, Japan",
                                "organization": "Physics Program and International Institute for Sustainability with Knotted Chiral Meta Matter (SKCM2)",
                                "country": "Japan",
                            }
                        ],
                    },
                    {
                        "surname": "Oyama",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "Nagasaki Institute of Applied Science, Nagasaki, Japan",
                                "organization": "Nagasaki Institute of Applied Science",
                                "country": "Japan",
                            }
                        ],
                        "orcid": "0000-0002-8576-1268",
                    },
                    {
                        "surname": "Pachmayer",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-6142-1528",
                    },
                    {
                        "surname": "Padhan",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Bombay (IIT), Mumbai, India",
                                "organization": "Indian Institute of Technology Bombay (IIT)",
                                "country": "India",
                            }
                        ],
                        "orcid": "0009-0007-8144-2829",
                    },
                    {
                        "surname": "Pagano",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Università di Brescia, Brescia, Italy",
                                "organization": "Università di Brescia",
                                "country": "Italy",
                            },
                            {
                                "value": "INFN, Sezione di Pavia, Pavia, Italy",
                                "organization": "INFN, Sezione di Pavia",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0003-0333-448X",
                    },
                    {
                        "surname": "Paić",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Instituto de Ciencias Nucleares, Universidad Nacional Autónoma de México, Mexico City, Mexico",
                                "organization": "Instituto de Ciencias Nucleares",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0000-0003-2513-2459",
                    },
                    {
                        "surname": "Palasciano",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bari, Bari, Italy",
                                "organization": "INFN, Sezione di Bari",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-5686-6626",
                    },
                    {
                        "surname": "Panebianco",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA), IRFU, Départment de Physique Nucléaire (DPhN), Saclay, France",
                                "organization": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA)",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-0343-2082",
                    },
                    {
                        "surname": "Park",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Inha University, Incheon, Republic of Korea",
                                "organization": "Inha University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0002-2540-2394",
                    },
                    {
                        "surname": "Parkkila",
                        "given_names": "J.E.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            },
                            {
                                "value": "University of Jyväskylä, Jyväskylä, Finland",
                                "organization": "University of Jyväskylä",
                                "country": "Finland",
                            },
                        ],
                        "orcid": "0000-0002-5166-5788",
                    },
                    {
                        "surname": "Pathak",
                        "given_names": "S.P.",
                        "affiliations": [
                            {
                                "value": "University of Houston, Houston, TX, United States",
                                "organization": "University of Houston",
                                "country": "United States",
                            }
                        ],
                    },
                    {
                        "surname": "Patra",
                        "given_names": "R.N.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Jammu, Jammu, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Paul",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Cagliari, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-1461-3743",
                    },
                    {
                        "surname": "Pei",
                        "given_names": "H.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0002-5078-3336",
                    },
                    {
                        "surname": "Peitzmann",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Institute for Gravitational and Subatomic Physics (GRASP), Utrecht University/Nikhef, Utrecht, Netherlands",
                                "organization": "Institute for Gravitational and Subatomic Physics (GRASP)",
                                "country": "Netherlands",
                            }
                        ],
                        "orcid": "0000-0002-7116-899X",
                    },
                    {
                        "surname": "Peng",
                        "given_names": "X.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0003-0759-2283",
                    },
                    {
                        "surname": "Pereira",
                        "given_names": "L.G.",
                        "affiliations": [
                            {
                                "value": "Instituto de Física, Universidade Federal do Rio Grande do Sul (UFRGS), Porto Alegre, Brazil",
                                "organization": "Instituto de Física",
                                "country": "Brazil",
                            }
                        ],
                        "orcid": "0000-0001-5496-580X",
                    },
                    {
                        "surname": "Pereira Da Costa",
                        "given_names": "H.",
                        "affiliations": [
                            {
                                "value": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA), IRFU, Départment de Physique Nucléaire (DPhN), Saclay, France",
                                "organization": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA)",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-3863-352X",
                    },
                    {
                        "surname": "Peresunko",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0003-3709-5130",
                    },
                    {
                        "surname": "Perez",
                        "given_names": "G.M.",
                        "affiliations": [
                            {
                                "value": "Centro de Aplicaciones Tecnológicas y Desarrollo Nuclear (CEADEN), Havana, Cuba",
                                "organization": "Centro de Aplicaciones Tecnológicas y Desarrollo Nuclear (CEADEN)",
                                "country": "Cuba",
                            }
                        ],
                        "orcid": "0000-0001-8817-5013",
                    },
                    {
                        "surname": "Perrin",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA), IRFU, Départment de Physique Nucléaire (DPhN), Saclay, France",
                                "organization": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA)",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-1192-137X",
                    },
                    {
                        "surname": "Pestov",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                    },
                    {
                        "surname": "Petráček",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Faculty of Nuclear Sciences and Physical Engineering, Czech Technical University in Prague, Prague, Czech Republic",
                                "organization": "Faculty of Nuclear Sciences and Physical Engineering",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0002-4057-3415",
                    },
                    {
                        "surname": "Petrov",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0009-0001-4054-2336",
                    },
                    {
                        "surname": "Petrovici",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Horia Hulubei National Institute of Physics and Nuclear Engineering, Bucharest, Romania",
                                "organization": "Horia Hulubei National Institute of Physics and Nuclear Engineering",
                                "country": "Romania",
                            }
                        ],
                        "orcid": "0000-0002-2291-6955",
                    },
                    {
                        "surname": "Pezzi",
                        "given_names": "R.P.",
                        "affiliations": [
                            {
                                "value": "SUBATECH, IMT Atlantique, Nantes Université, CNRS-IN2P3, Nantes, France",
                                "organization": "SUBATECH",
                                "country": "France",
                            },
                            {
                                "value": "Instituto de Física, Universidade Federal do Rio Grande do Sul (UFRGS), Porto Alegre, Brazil",
                                "organization": "Instituto de Física",
                                "country": "Brazil",
                            },
                        ],
                        "orcid": "0000-0002-0452-3103",
                    },
                    {
                        "surname": "Piano",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Trieste, Trieste, Italy",
                                "organization": "INFN, Sezione di Trieste",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-4903-9865",
                    },
                    {
                        "surname": "Pikna",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Comenius University Bratislava, Faculty of Mathematics, Physics and Informatics, Bratislava, Slovak Republic",
                                "organization": "Comenius University Bratislava",
                                "country": "Slovak Republic",
                            }
                        ],
                        "orcid": "0009-0004-8574-2392",
                    },
                    {
                        "surname": "Pillot",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "SUBATECH, IMT Atlantique, Nantes Université, CNRS-IN2P3, Nantes, France",
                                "organization": "SUBATECH",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-9067-0803",
                    },
                    {
                        "surname": "Pinazza",
                        "given_names": "O.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bologna, Bologna, Italy",
                                "organization": "INFN, Sezione di Bologna",
                                "country": "Italy",
                            },
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            },
                        ],
                        "orcid": "0000-0001-8923-4003",
                    },
                    {
                        "surname": "Pinsky",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "University of Houston, Houston, TX, United States",
                                "organization": "University of Houston",
                                "country": "United States",
                            }
                        ],
                    },
                    {
                        "surname": "Pinto",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            },
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Catania, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0001-7454-4324",
                    },
                    {
                        "surname": "Pisano",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "INFN, Laboratori Nazionali di Frascati, Frascati, Italy",
                                "organization": "INFN, Laboratori Nazionali di Frascati",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-4080-6562",
                    },
                    {
                        "surname": "Płoskoń",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Lawrence Berkeley National Laboratory, Berkeley, CA, United States",
                                "organization": "Lawrence Berkeley National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0003-3161-9183",
                    },
                    {
                        "surname": "Planinic",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Physics department, Faculty of science, University of Zagreb, Zagreb, Croatia",
                                "organization": "Physics department",
                                "country": "Croatia",
                            }
                        ],
                    },
                    {
                        "surname": "Pliquett",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Poghosyan",
                        "given_names": "M.G.",
                        "affiliations": [
                            {
                                "value": "Oak Ridge National Laboratory, Oak Ridge, TN, United States",
                                "organization": "Oak Ridge National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-1832-595X",
                    },
                    {
                        "surname": "Politano",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Dipartimento DISAT del Politecnico and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento DISAT del Politecnico",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-0414-5525",
                    },
                    {
                        "surname": "Poljak",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Physics department, Faculty of science, University of Zagreb, Zagreb, Croatia",
                                "organization": "Physics department",
                                "country": "Croatia",
                            }
                        ],
                        "orcid": "0000-0002-4512-9620",
                    },
                    {
                        "surname": "Pop",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Horia Hulubei National Institute of Physics and Nuclear Engineering, Bucharest, Romania",
                                "organization": "Horia Hulubei National Institute of Physics and Nuclear Engineering",
                                "country": "Romania",
                            }
                        ],
                        "orcid": "0000-0003-0425-5724",
                    },
                    {
                        "surname": "Porteboeuf-Houssais",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Université Clermont Auvergne, CNRS/IN2P3, LPC, Clermont-Ferrand, France",
                                "organization": "Université Clermont Auvergne",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-2646-6189",
                    },
                    {
                        "surname": "Porter",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Lawrence Berkeley National Laboratory, Berkeley, CA, United States",
                                "organization": "Lawrence Berkeley National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-6265-8794",
                    },
                    {
                        "surname": "Pozdniakov",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-3362-7411",
                    },
                    {
                        "surname": "Prasad",
                        "given_names": "S.K.",
                        "affiliations": [
                            {
                                "value": "Bose Institute, Department of Physics and Centre for Astroparticle Physics and Space Science (CAPSS), Kolkata, India",
                                "organization": "Bose Institute",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-7394-8834",
                    },
                    {
                        "surname": "Prasad",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Indore, Indore, India",
                                "organization": "Indian Institute of Technology Indore",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0003-0607-2841",
                    },
                    {
                        "surname": "Preghenella",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bologna, Bologna, Italy",
                                "organization": "INFN, Sezione di Bologna",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-1539-9275",
                    },
                    {
                        "surname": "Prino",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Torino, Turin, Italy",
                                "organization": "INFN, Sezione di Torino",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-6179-150X",
                    },
                    {
                        "surname": "Pruneau",
                        "given_names": "C.A.",
                        "affiliations": [
                            {
                                "value": "Wayne State University, Detroit, MI, United States",
                                "organization": "Wayne State University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-0458-538X",
                    },
                    {
                        "surname": "Pshenichnov",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0003-1752-4524",
                    },
                    {
                        "surname": "Puccio",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-8118-9049",
                    },
                    {
                        "surname": "Qiu",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Nikhef, National institute for subatomic physics, Amsterdam, Netherlands",
                                "organization": "Nikhef, National institute for subatomic physics",
                                "country": "Netherlands",
                            }
                        ],
                        "orcid": "0000-0003-1401-5900",
                    },
                    {
                        "surname": "Quaglia",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-0793-8275",
                    },
                    {
                        "surname": "Quishpe",
                        "given_names": "R.E.",
                        "affiliations": [
                            {
                                "value": "University of Houston, Houston, TX, United States",
                                "organization": "University of Houston",
                                "country": "United States",
                            }
                        ],
                    },
                    {
                        "surname": "Ragoni",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "School of Physics and Astronomy, University of Birmingham, Birmingham, United Kingdom",
                                "organization": "School of Physics and Astronomy",
                                "country": "United Kingdom",
                            }
                        ],
                        "orcid": "0000-0001-9765-5668",
                    },
                    {
                        "surname": "Rakotozafindrabe",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA), IRFU, Départment de Physique Nucléaire (DPhN), Saclay, France",
                                "organization": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA)",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0003-4484-6430",
                    },
                    {
                        "surname": "Ramello",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Università del Piemonte Orientale, Vercelli, Italy",
                                "organization": "Università del Piemonte Orientale",
                                "country": "Italy",
                            },
                            {
                                "value": "INFN, Sezione di Torino, Turin, Italy",
                                "organization": "INFN, Sezione di Torino",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0003-2325-8680",
                    },
                    {
                        "surname": "Rami",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Université de Strasbourg, CNRS, IPHC UMR 7178, F-67000 Strasbourg, France",
                                "organization": "Université de Strasbourg",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-6101-5981",
                    },
                    {
                        "surname": "Ramirez",
                        "given_names": "S.A.R.",
                        "affiliations": [
                            {
                                "value": "High Energy Physics Group, Universidad Autónoma de Puebla, Puebla, Mexico",
                                "organization": "High Energy Physics Group",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0000-0003-2864-8565",
                    },
                    {
                        "surname": "Rancien",
                        "given_names": "T.A.",
                        "affiliations": [
                            {
                                "value": "Laboratoire de Physique Subatomique et de Cosmologie, Université Grenoble-Alpes, CNRS-IN2P3, Grenoble, France",
                                "organization": "Laboratoire de Physique Subatomique et de Cosmologie",
                                "country": "France",
                            }
                        ],
                    },
                    {
                        "surname": "Raniwala",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Rajasthan, Jaipur, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-9172-5474",
                    },
                    {
                        "surname": "Raniwala",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Rajasthan, Jaipur, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Räsänen",
                        "given_names": "S.S.",
                        "affiliations": [
                            {
                                "value": "Helsinki Institute of Physics (HIP), Helsinki, Finland",
                                "organization": "Helsinki Institute of Physics (HIP)",
                                "country": "Finland",
                            }
                        ],
                        "orcid": "0000-0001-6792-7773",
                    },
                    {
                        "surname": "Rath",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Indore, Indore, India",
                                "organization": "Indian Institute of Technology Indore",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-0118-3131",
                    },
                    {
                        "surname": "Ravasenga",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Nikhef, National institute for subatomic physics, Amsterdam, Netherlands",
                                "organization": "Nikhef, National institute for subatomic physics",
                                "country": "Netherlands",
                            }
                        ],
                        "orcid": "0000-0001-6120-4726",
                    },
                    {
                        "surname": "Read",
                        "given_names": "K.F.",
                        "affiliations": [
                            {
                                "value": "Oak Ridge National Laboratory, Oak Ridge, TN, United States",
                                "organization": "Oak Ridge National Laboratory",
                                "country": "United States",
                            },
                            {
                                "value": "University of Tennessee, Knoxville, TN, United States",
                                "organization": "University of Tennessee",
                                "country": "United States",
                            },
                        ],
                        "orcid": "0000-0002-3358-7667",
                    },
                    {
                        "surname": "Redelbach",
                        "given_names": "A.R.",
                        "affiliations": [
                            {
                                "value": "Frankfurt Institute for Advanced Studies, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Frankfurt Institute for Advanced Studies",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-8102-9686",
                    },
                    {
                        "surname": "Redlich",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "National Centre for Nuclear Research, Warsaw, Poland",
                                "organization": "National Centre for Nuclear Research",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0002-2629-1710",
                    },
                    {
                        "surname": "Rehman",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Department of Physics and Technology, University of Bergen, Bergen, Norway",
                                "organization": "Department of Physics and Technology",
                                "country": "Norway",
                            }
                        ],
                    },
                    {
                        "surname": "Reichelt",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Reidt",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-5263-3593",
                    },
                    {
                        "surname": "Reme-Ness",
                        "given_names": "H.A.",
                        "affiliations": [
                            {
                                "value": "Faculty of Engineering and Science, Western Norway University of Applied Sciences, Bergen, Norway",
                                "organization": "Faculty of Engineering and Science",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0009-0006-8025-735X",
                    },
                    {
                        "surname": "Rescakova",
                        "given_names": "Z.",
                        "affiliations": [
                            {
                                "value": "Faculty of Science, P.J. Šafárik University, Košice, Slovak Republic",
                                "organization": "Faculty of Science",
                                "country": "Slovak Republic",
                            }
                        ],
                    },
                    {
                        "surname": "Reygers",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-9808-1811",
                    },
                    {
                        "surname": "Riabov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0009-0007-9874-9819",
                    },
                    {
                        "surname": "Riabov",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-8142-6374",
                    },
                    {
                        "surname": "Ricci",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica ‘E.R. Caianiello’ dell'Università and Gruppo Collegato INFN, Salerno, Italy",
                                "organization": "Dipartimento di Fisica ‘E.R. Caianiello’ dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-5208-6657",
                    },
                    {
                        "surname": "Richert",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Lund University Department of Physics, Division of Particle Physics, Lund, Sweden",
                                "organization": "Lund University Department of Physics",
                                "country": "Sweden",
                            }
                        ],
                    },
                    {
                        "surname": "Richter",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, University of Oslo, Oslo, Norway",
                                "organization": "Department of Physics",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0009-0008-3492-3758",
                    },
                    {
                        "surname": "Riegler",
                        "given_names": "W.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0009-0002-1824-0822",
                    },
                    {
                        "surname": "Riggi",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Catania, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-0030-8377",
                    },
                    {
                        "surname": "Ristea",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Institute of Space Science (ISS), Bucharest, Romania",
                                "organization": "Institute of Space Science (ISS)",
                                "country": "Romania",
                            }
                        ],
                        "orcid": "0000-0002-9760-645X",
                    },
                    {
                        "surname": "Rodríguez Cahuantzi",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "High Energy Physics Group, Universidad Autónoma de Puebla, Puebla, Mexico",
                                "organization": "High Energy Physics Group",
                                "country": "Mexico",
                            }
                        ],
                        "orcid": "0000-0002-9596-1060",
                    },
                    {
                        "surname": "Røed",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, University of Oslo, Oslo, Norway",
                                "organization": "Department of Physics",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0000-0001-7803-9640",
                    },
                    {
                        "surname": "Rogalev",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-4680-4413",
                    },
                    {
                        "surname": "Rogochaya",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-4278-5999",
                    },
                    {
                        "surname": "Rogoschinski",
                        "given_names": "T.S.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-0649-2283",
                    },
                    {
                        "surname": "Rohr",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0003-4101-0160",
                    },
                    {
                        "surname": "Röhrich",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Department of Physics and Technology, University of Bergen, Bergen, Norway",
                                "organization": "Department of Physics and Technology",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0000-0003-4966-9584",
                    },
                    {
                        "surname": "Rojas",
                        "given_names": "P.F.",
                        "affiliations": [
                            {
                                "value": "High Energy Physics Group, Universidad Autónoma de Puebla, Puebla, Mexico",
                                "organization": "High Energy Physics Group",
                                "country": "Mexico",
                            }
                        ],
                    },
                    {
                        "surname": "Rojas Torres",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Faculty of Nuclear Sciences and Physical Engineering, Czech Technical University in Prague, Prague, Czech Republic",
                                "organization": "Faculty of Nuclear Sciences and Physical Engineering",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0002-2361-2662",
                    },
                    {
                        "surname": "Rokita",
                        "given_names": "P.S.",
                        "affiliations": [
                            {
                                "value": "Warsaw University of Technology, Warsaw, Poland",
                                "organization": "Warsaw University of Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0002-4433-2133",
                    },
                    {
                        "surname": "Ronchetti",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "INFN, Laboratori Nazionali di Frascati, Frascati, Italy",
                                "organization": "INFN, Laboratori Nazionali di Frascati",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-5245-8441",
                    },
                    {
                        "surname": "Rosano",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Scienze MIFT, Università di Messina, Messina, Italy",
                                "organization": "Dipartimento di Scienze MIFT",
                                "country": "Italy",
                            },
                            {
                                "value": "INFN, Sezione di Catania, Catania, Italy",
                                "organization": "INFN, Sezione di Catania",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0002-6467-2418",
                    },
                    {
                        "surname": "Rosas",
                        "given_names": "E.D.",
                        "affiliations": [
                            {
                                "value": "Instituto de Ciencias Nucleares, Universidad Nacional Autónoma de México, Mexico City, Mexico",
                                "organization": "Instituto de Ciencias Nucleares",
                                "country": "Mexico",
                            }
                        ],
                    },
                    {
                        "surname": "Rossi",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Padova, Padova, Italy",
                                "organization": "INFN, Sezione di Padova",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-6067-6294",
                    },
                    {
                        "surname": "Roy",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Indore, Indore, India",
                                "organization": "Indian Institute of Technology Indore",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-1142-3186",
                    },
                    {
                        "surname": "Roy",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Saha Institute of Nuclear Physics, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Saha Institute of Nuclear Physics",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Roy",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Bombay (IIT), Mumbai, India",
                                "organization": "Indian Institute of Technology Bombay (IIT)",
                                "country": "India",
                            }
                        ],
                        "orcid": "0009-0002-1397-8334",
                    },
                    {
                        "surname": "Rubini",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Bologna, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-9874-7249",
                    },
                    {
                        "surname": "Rueda",
                        "given_names": "O.V.",
                        "affiliations": [
                            {
                                "value": "Lund University Department of Physics, Division of Particle Physics, Lund, Sweden",
                                "organization": "Lund University Department of Physics",
                                "country": "Sweden",
                            }
                        ],
                        "orcid": "0000-0002-6365-3258",
                    },
                    {
                        "surname": "Ruggiano",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Warsaw University of Technology, Warsaw, Poland",
                                "organization": "Warsaw University of Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0001-7082-5890",
                    },
                    {
                        "surname": "Rui",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Trieste, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-6993-0332",
                    },
                    {
                        "surname": "Rumyantsev",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN"
                            }
                        ],
                    },
                    {
                        "surname": "Russek",
                        "given_names": "P.G.",
                        "affiliations": [
                            {
                                "value": "AGH University of Science and Technology, Cracow, Poland",
                                "organization": "AGH University of Science and Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0003-3858-4278",
                    },
                    {
                        "surname": "Russo",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Nikhef, National institute for subatomic physics, Amsterdam, Netherlands",
                                "organization": "Nikhef, National institute for subatomic physics",
                                "country": "Netherlands",
                            }
                        ],
                        "orcid": "0000-0002-7492-974X",
                    },
                    {
                        "surname": "Rustamov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "National Nuclear Research Center, Baku, Azerbaijan",
                                "organization": "National Nuclear Research Center",
                                "country": "Azerbaijan",
                            }
                        ],
                        "orcid": "0000-0001-8678-6400",
                    },
                    {
                        "surname": "Ryabinkin",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0009-0006-8982-9510",
                    },
                    {
                        "surname": "Ryabov",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-3028-8776",
                    },
                    {
                        "surname": "Rybicki",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "The Henryk Niewodniczanski Institute of Nuclear Physics, Polish Academy of Sciences, Cracow, Poland",
                                "organization": "The Henryk Niewodniczanski Institute of Nuclear Physics",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0003-3076-0505",
                    },
                    {
                        "surname": "Rytkonen",
                        "given_names": "H.",
                        "affiliations": [
                            {
                                "value": "University of Jyväskylä, Jyväskylä, Finland",
                                "organization": "University of Jyväskylä",
                                "country": "Finland",
                            }
                        ],
                        "orcid": "0000-0001-7493-5552",
                    },
                    {
                        "surname": "Rzesa",
                        "given_names": "W.",
                        "affiliations": [
                            {
                                "value": "Warsaw University of Technology, Warsaw, Poland",
                                "organization": "Warsaw University of Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0002-3274-9986",
                    },
                    {
                        "surname": "Saarimaki",
                        "given_names": "O.A.M.",
                        "affiliations": [
                            {
                                "value": "Helsinki Institute of Physics (HIP), Helsinki, Finland",
                                "organization": "Helsinki Institute of Physics (HIP)",
                                "country": "Finland",
                            }
                        ],
                        "orcid": "0000-0003-3346-3645",
                    },
                    {
                        "surname": "Sadek",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "SUBATECH, IMT Atlantique, Nantes Université, CNRS-IN2P3, Nantes, France",
                                "organization": "SUBATECH",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0003-0438-8359",
                    },
                    {
                        "surname": "Sadovsky",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-6781-416X",
                    },
                    {
                        "surname": "Saetre",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Department of Physics and Technology, University of Bergen, Bergen, Norway",
                                "organization": "Department of Physics and Technology",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0000-0001-8769-0865",
                    },
                    {
                        "surname": "Šafařík",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "Faculty of Nuclear Sciences and Physical Engineering, Czech Technical University in Prague, Prague, Czech Republic",
                                "organization": "Faculty of Nuclear Sciences and Physical Engineering",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0003-2512-5451",
                    },
                    {
                        "surname": "Saha",
                        "given_names": "S.K.",
                        "affiliations": [
                            {
                                "value": "Variable Energy Cyclotron Centre, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Variable Energy Cyclotron Centre",
                                "country": "India",
                            }
                        ],
                        "orcid": "0009-0005-0580-829X",
                    },
                    {
                        "surname": "Saha",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "National Institute of Science Education and Research, Homi Bhabha National Institute, Jatni, India",
                                "organization": "National Institute of Science Education and Research",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-4159-3549",
                    },
                    {
                        "surname": "Sahoo",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Bombay (IIT), Mumbai, India",
                                "organization": "Indian Institute of Technology Bombay (IIT)",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0001-7383-4418",
                    },
                    {
                        "surname": "Sahoo",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Bombay (IIT), Mumbai, India",
                                "organization": "Indian Institute of Technology Bombay (IIT)",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Sahoo",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Indore, Indore, India",
                                "organization": "Indian Institute of Technology Indore",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0003-3334-0661",
                    },
                    {
                        "surname": "Sahoo",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Institute of Physics, Homi Bhabha National Institute, Bhubaneswar, India",
                                "organization": "Institute of Physics",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Sahu",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Indore, Indore, India",
                                "organization": "Indian Institute of Technology Indore",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0001-8980-1362",
                    },
                    {
                        "surname": "Sahu",
                        "given_names": "P.K.",
                        "affiliations": [
                            {
                                "value": "Institute of Physics, Homi Bhabha National Institute, Bhubaneswar, India",
                                "organization": "Institute of Physics",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0003-3546-3390",
                    },
                    {
                        "surname": "Saini",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Variable Energy Cyclotron Centre, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Variable Energy Cyclotron Centre",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0003-3266-9959",
                    },
                    {
                        "surname": "Sajdakova",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "Faculty of Science, P.J. Šafárik University, Košice, Slovak Republic",
                                "organization": "Faculty of Science",
                                "country": "Slovak Republic",
                            }
                        ],
                    },
                    {
                        "surname": "Sakai",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "University of Tsukuba, Tsukuba, Japan",
                                "organization": "University of Tsukuba",
                                "country": "Japan",
                            }
                        ],
                        "orcid": "0000-0003-1380-0392",
                    },
                    {
                        "surname": "Salvan",
                        "given_names": "M.P.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-8111-5576",
                    },
                    {
                        "surname": "Sambyal",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Jammu, Jammu, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-5018-6902",
                    },
                    {
                        "surname": "Saramela",
                        "given_names": "T.B.",
                        "affiliations": [
                            {
                                "value": "Universidade de São Paulo (USP), São Paulo, Brazil",
                                "organization": "Universidade de São Paulo (USP)",
                                "country": "Brazil",
                            }
                        ],
                    },
                    {
                        "surname": "Sarkar",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Wayne State University, Detroit, MI, United States",
                                "organization": "Wayne State University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-2393-0804",
                    },
                    {
                        "surname": "Sarkar",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Variable Energy Cyclotron Centre, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Variable Energy Cyclotron Centre",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Sarma",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Gauhati University, Department of Physics, Guwahati, India",
                                "organization": "Gauhati University",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-3191-4513",
                    },
                    {
                        "surname": "Sarritzu",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Cagliari, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-9879-1119",
                    },
                    {
                        "surname": "Sarti",
                        "given_names": "V.M.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-8438-3966",
                    },
                    {
                        "surname": "Sas",
                        "given_names": "M.H.P.",
                        "affiliations": [
                            {
                                "value": "Yale University, New Haven, CT, United States",
                                "organization": "Yale University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0003-1419-2085",
                    },
                    {
                        "surname": "Schambach",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Oak Ridge National Laboratory, Oak Ridge, TN, United States",
                                "organization": "Oak Ridge National Laboratory",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0003-3266-1332",
                    },
                    {
                        "surname": "Scheid",
                        "given_names": "H.S.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-1184-9627",
                    },
                    {
                        "surname": "Schiaua",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Horia Hulubei National Institute of Physics and Nuclear Engineering, Bucharest, Romania",
                                "organization": "Horia Hulubei National Institute of Physics and Nuclear Engineering",
                                "country": "Romania",
                            }
                        ],
                        "orcid": "0009-0009-3728-8849",
                    },
                    {
                        "surname": "Schicker",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-1230-4274",
                    },
                    {
                        "surname": "Schmah",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Schmidt",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-2295-6199",
                    },
                    {
                        "surname": "Schmidt",
                        "given_names": "H.R.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Eberhard-Karls-Universität Tübingen, Tübingen, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Schmidt",
                        "given_names": "M.O.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0001-5335-1515",
                    },
                    {
                        "surname": "Schmidt",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Eberhard-Karls-Universität Tübingen, Tübingen, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Schmidt",
                        "given_names": "N.V.",
                        "affiliations": [
                            {
                                "value": "Oak Ridge National Laboratory, Oak Ridge, TN, United States",
                                "organization": "Oak Ridge National Laboratory",
                                "country": "United States",
                            },
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            },
                        ],
                        "orcid": "0000-0002-5795-4871",
                    },
                    {
                        "surname": "Schmier",
                        "given_names": "A.R.",
                        "affiliations": [
                            {
                                "value": "University of Tennessee, Knoxville, TN, United States",
                                "organization": "University of Tennessee",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0001-9093-4461",
                    },
                    {
                        "surname": "Schotter",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Université de Strasbourg, CNRS, IPHC UMR 7178, F-67000 Strasbourg, France",
                                "organization": "Université de Strasbourg",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-4791-5481",
                    },
                    {
                        "surname": "Schukraft",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-6638-2932",
                    },
                    {
                        "surname": "Schwarz",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Schweda",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-9935-6995",
                    },
                    {
                        "surname": "Scioli",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Bologna, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-0144-0713",
                    },
                    {
                        "surname": "Scomparin",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Torino, Turin, Italy",
                                "organization": "INFN, Sezione di Torino",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0001-9015-9610",
                    },
                    {
                        "surname": "Seger",
                        "given_names": "J.E.",
                        "affiliations": [
                            {
                                "value": "Creighton University, Omaha, NE, United States",
                                "organization": "Creighton University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0003-1423-6973",
                    },
                    {
                        "surname": "Sekiguchi",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "University of Tokyo, Tokyo, Japan",
                                "organization": "University of Tokyo",
                                "country": "Japan",
                            }
                        ],
                    },
                    {
                        "surname": "Sekihata",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "University of Tokyo, Tokyo, Japan",
                                "organization": "University of Tokyo",
                                "country": "Japan",
                            }
                        ],
                        "orcid": "0009-0000-9692-8812",
                    },
                    {
                        "surname": "Selyuzhenkov",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            },
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            },
                        ],
                        "orcid": "0000-0002-8042-4924",
                    },
                    {
                        "surname": "Senyukov",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Université de Strasbourg, CNRS, IPHC UMR 7178, F-67000 Strasbourg, France",
                                "organization": "Université de Strasbourg",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0003-1907-9786",
                    },
                    {
                        "surname": "Seo",
                        "given_names": "J.J.",
                        "affiliations": [
                            {
                                "value": "Inha University, Incheon, Republic of Korea",
                                "organization": "Inha University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0002-6368-3350",
                    },
                    {
                        "surname": "Serebryakov",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-5546-6524",
                    },
                    {
                        "surname": "Šerkšnytė",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-5657-5351",
                    },
                    {
                        "surname": "Sevcenco",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Institute of Space Science (ISS), Bucharest, Romania",
                                "organization": "Institute of Space Science (ISS)",
                                "country": "Romania",
                            }
                        ],
                        "orcid": "0000-0002-4151-1056",
                    },
                    {
                        "surname": "Shaba",
                        "given_names": "T.J.",
                        "affiliations": [
                            {
                                "value": "iThemba LABS, National Research Foundation, Somerset West, South Africa",
                                "organization": "iThemba LABS",
                                "country": "South Africa",
                            }
                        ],
                        "orcid": "0000-0003-2290-9031",
                    },
                    {
                        "surname": "Shabanov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                    },
                    {
                        "surname": "Shabetai",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "SUBATECH, IMT Atlantique, Nantes Université, CNRS-IN2P3, Nantes, France",
                                "organization": "SUBATECH",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0003-3069-726X",
                    },
                    {
                        "surname": "Shahoyan",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                    },
                    {
                        "surname": "Shaikh",
                        "given_names": "W.",
                        "affiliations": [
                            {
                                "value": "Saha Institute of Nuclear Physics, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Saha Institute of Nuclear Physics",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Shangaraev",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-5053-7506",
                    },
                    {
                        "surname": "Sharma",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Physics Department, Panjab University, Chandigarh, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Sharma",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Bombay (IIT), Mumbai, India",
                                "organization": "Indian Institute of Technology Bombay (IIT)",
                                "country": "India",
                            }
                        ],
                        "orcid": "0009-0001-9105-0729",
                    },
                    {
                        "surname": "Sharma",
                        "given_names": "H.",
                        "affiliations": [
                            {
                                "value": "The Henryk Niewodniczanski Institute of Nuclear Physics, Polish Academy of Sciences, Cracow, Poland",
                                "organization": "The Henryk Niewodniczanski Institute of Nuclear Physics",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0003-2753-4283",
                    },
                    {
                        "surname": "Sharma",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Jammu, Jammu, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-8256-8200",
                    },
                    {
                        "surname": "Sharma",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Physics Department, Panjab University, Chandigarh, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0001-8046-1752",
                    },
                    {
                        "surname": "Sharma",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Jammu, Jammu, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-7159-6839",
                    },
                    {
                        "surname": "Sharma",
                        "given_names": "U.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Jammu, Jammu, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0001-7686-070X",
                    },
                    {
                        "surname": "Shatat",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie, Orsay, France",
                                "organization": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0001-7432-6669",
                    },
                    {
                        "surname": "Sheibani",
                        "given_names": "O.",
                        "affiliations": [
                            {
                                "value": "University of Houston, Houston, TX, United States",
                                "organization": "University of Houston",
                                "country": "United States",
                            }
                        ],
                    },
                    {
                        "surname": "Shigaki",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "Physics Program and International Institute for Sustainability with Knotted Chiral Meta Matter (SKCM2), Hiroshima University, Hiroshima, Japan",
                                "organization": "Physics Program and International Institute for Sustainability with Knotted Chiral Meta Matter (SKCM2)",
                                "country": "Japan",
                            }
                        ],
                        "orcid": "0000-0001-8416-8617",
                    },
                    {
                        "surname": "Shimomura",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Nara Women's University (NWU), Nara, Japan",
                                "organization": "Nara Women's University (NWU)",
                                "country": "Japan",
                            }
                        ],
                    },
                    {
                        "surname": "Shirinkin",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0009-0006-0106-6054",
                    },
                    {
                        "surname": "Shou",
                        "given_names": "Q.",
                        "affiliations": [
                            {
                                "value": "Fudan University, Shanghai, China",
                                "organization": "Fudan University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0001-5128-6238",
                    },
                    {
                        "surname": "Sibiriak",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-3348-1221",
                    },
                    {
                        "surname": "Siddhanta",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Cagliari, Cagliari, Italy",
                                "organization": "INFN, Sezione di Cagliari",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-0543-9245",
                    },
                    {
                        "surname": "Siemiarczuk",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "National Centre for Nuclear Research, Warsaw, Poland",
                                "organization": "National Centre for Nuclear Research",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0002-2014-5229",
                    },
                    {
                        "surname": "Silva",
                        "given_names": "T.F.",
                        "affiliations": [
                            {
                                "value": "Universidade de São Paulo (USP), São Paulo, Brazil",
                                "organization": "Universidade de São Paulo (USP)",
                                "country": "Brazil",
                            }
                        ],
                        "orcid": "0000-0002-7643-2198",
                    },
                    {
                        "surname": "Silvermyr",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Lund University Department of Physics, Division of Particle Physics, Lund, Sweden",
                                "organization": "Lund University Department of Physics",
                                "country": "Sweden",
                            }
                        ],
                        "orcid": "0000-0002-0526-5791",
                    },
                    {
                        "surname": "Simantathammakul",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Suranaree University of Technology, Nakhon Ratchasima, Thailand",
                                "organization": "Suranaree University of Technology",
                                "country": "Thailand",
                            }
                        ],
                    },
                    {
                        "surname": "Simeonov",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Faculty of Physics, Sofia University, Sofia, Bulgaria",
                                "organization": "Faculty of Physics",
                                "country": "Bulgaria",
                            }
                        ],
                        "orcid": "0000-0001-7729-5503",
                    },
                    {
                        "surname": "Simonetti",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                    },
                    {
                        "surname": "Singh",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Jammu, Jammu, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Singh",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-8997-0019",
                    },
                    {
                        "surname": "Singh",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "National Institute of Science Education and Research, Homi Bhabha National Institute, Jatni, India",
                                "organization": "National Institute of Science Education and Research",
                                "country": "India",
                            }
                        ],
                        "orcid": "0009-0007-7617-1577",
                    },
                    {
                        "surname": "Singh",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Jammu, Jammu, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-6904-9879",
                    },
                    {
                        "surname": "Singh",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Indore, Indore, India",
                                "organization": "Indian Institute of Technology Indore",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-6746-6847",
                    },
                    {
                        "surname": "Singh",
                        "given_names": "V.K.",
                        "affiliations": [
                            {
                                "value": "Variable Energy Cyclotron Centre, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Variable Energy Cyclotron Centre",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-5783-3551",
                    },
                    {
                        "surname": "Singhal",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Variable Energy Cyclotron Centre, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Variable Energy Cyclotron Centre",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-6315-9671",
                    },
                    {
                        "surname": "Sinha",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Saha Institute of Nuclear Physics, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Saha Institute of Nuclear Physics",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-1290-8388",
                    },
                    {
                        "surname": "Sitar",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Comenius University Bratislava, Faculty of Mathematics, Physics and Informatics, Bratislava, Slovak Republic",
                                "organization": "Comenius University Bratislava",
                                "country": "Slovak Republic",
                            }
                        ],
                        "orcid": "0009-0002-7519-0796",
                    },
                    {
                        "surname": "Sitta",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Università del Piemonte Orientale, Vercelli, Italy",
                                "organization": "Università del Piemonte Orientale",
                                "country": "Italy",
                            },
                            {
                                "value": "INFN, Sezione di Torino, Turin, Italy",
                                "organization": "INFN, Sezione di Torino",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0002-4175-148X",
                    },
                    {
                        "surname": "Skaali",
                        "given_names": "T.B.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, University of Oslo, Oslo, Norway",
                                "organization": "Department of Physics",
                                "country": "Norway",
                            }
                        ],
                    },
                    {
                        "surname": "Skorodumovs",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-5747-4096",
                    },
                    {
                        "surname": "Slupecki",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Helsinki Institute of Physics (HIP), Helsinki, Finland",
                                "organization": "Helsinki Institute of Physics (HIP)",
                                "country": "Finland",
                            }
                        ],
                        "orcid": "0000-0003-2966-8445",
                    },
                    {
                        "surname": "Smirnov",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Yale University, New Haven, CT, United States",
                                "organization": "Yale University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-1361-0305",
                    },
                    {
                        "surname": "Snellings",
                        "given_names": "R.J.M.",
                        "affiliations": [
                            {
                                "value": "Institute for Gravitational and Subatomic Physics (GRASP), Utrecht University/Nikhef, Utrecht, Netherlands",
                                "organization": "Institute for Gravitational and Subatomic Physics (GRASP)",
                                "country": "Netherlands",
                            }
                        ],
                        "orcid": "0000-0001-9720-0604",
                    },
                    {
                        "surname": "Solheim",
                        "given_names": "E.H.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, University of Oslo, Oslo, Norway",
                                "organization": "Department of Physics",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0000-0001-6002-8732",
                    },
                    {
                        "surname": "Soncco",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Sección Física, Departamento de Ciencias, Pontificia Universidad Católica del Perú, Lima, Peru",
                                "organization": "Sección Física",
                                "country": "Peru",
                            }
                        ],
                    },
                    {
                        "surname": "Song",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "University of Houston, Houston, TX, United States",
                                "organization": "University of Houston",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-2847-2291",
                    },
                    {
                        "surname": "Songmoolnak",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Suranaree University of Technology, Nakhon Ratchasima, Thailand",
                                "organization": "Suranaree University of Technology",
                                "country": "Thailand",
                            }
                        ],
                    },
                    {
                        "surname": "Soramel",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Padova, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-1018-0987",
                    },
                    {
                        "surname": "Sorensen",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "University of Tennessee, Knoxville, TN, United States",
                                "organization": "University of Tennessee",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-5595-5643",
                    },
                    {
                        "surname": "Spijkers",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Nikhef, National institute for subatomic physics, Amsterdam, Netherlands",
                                "organization": "Nikhef, National institute for subatomic physics",
                                "country": "Netherlands",
                            }
                        ],
                        "orcid": "0000-0001-8625-763X",
                    },
                    {
                        "surname": "Sputowska",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "The Henryk Niewodniczanski Institute of Nuclear Physics, Polish Academy of Sciences, Cracow, Poland",
                                "organization": "The Henryk Niewodniczanski Institute of Nuclear Physics",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0002-7590-7171",
                    },
                    {
                        "surname": "Staa",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Lund University Department of Physics, Division of Particle Physics, Lund, Sweden",
                                "organization": "Lund University Department of Physics",
                                "country": "Sweden",
                            }
                        ],
                        "orcid": "0000-0001-8476-3547",
                    },
                    {
                        "surname": "Stachel",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-0750-6664",
                    },
                    {
                        "surname": "Stan",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Institute of Space Science (ISS), Bucharest, Romania",
                                "organization": "Institute of Space Science (ISS)",
                                "country": "Romania",
                            }
                        ],
                        "orcid": "0000-0003-1336-4092",
                    },
                    {
                        "surname": "Steffanic",
                        "given_names": "P.J.",
                        "affiliations": [
                            {
                                "value": "University of Tennessee, Knoxville, TN, United States",
                                "organization": "University of Tennessee",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-6814-1040",
                    },
                    {
                        "surname": "Stiefelmaier",
                        "given_names": "S.F.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-2269-1490",
                    },
                    {
                        "surname": "Stocco",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "SUBATECH, IMT Atlantique, Nantes Université, CNRS-IN2P3, Nantes, France",
                                "organization": "SUBATECH",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-5377-5163",
                    },
                    {
                        "surname": "Storehaug",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, University of Oslo, Oslo, Norway",
                                "organization": "Department of Physics",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0000-0002-3254-7305",
                    },
                    {
                        "surname": "Storetvedt",
                        "given_names": "M.M.",
                        "affiliations": [
                            {
                                "value": "Faculty of Engineering and Science, Western Norway University of Applied Sciences, Bergen, Norway",
                                "organization": "Faculty of Engineering and Science",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0009-0006-4489-2858",
                    },
                    {
                        "surname": "Stratmann",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Westfälische Wilhelms-Universität Münster, Institut für Kernphysik, Münster, Germany",
                                "organization": "Westfälische Wilhelms-Universität Münster",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0002-1978-3351",
                    },
                    {
                        "surname": "Strazzi",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica e Astronomia dell'Università and Sezione INFN, Bologna, Italy",
                                "organization": "Dipartimento di Fisica e Astronomia dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-2329-0330",
                    },
                    {
                        "surname": "Stylianidis",
                        "given_names": "C.P.",
                        "affiliations": [
                            {
                                "value": "Nikhef, National institute for subatomic physics, Amsterdam, Netherlands",
                                "organization": "Nikhef, National institute for subatomic physics",
                                "country": "Netherlands",
                            }
                        ],
                    },
                    {
                        "surname": "Suaide",
                        "given_names": "A.A.P.",
                        "affiliations": [
                            {
                                "value": "Universidade de São Paulo (USP), São Paulo, Brazil",
                                "organization": "Universidade de São Paulo (USP)",
                                "country": "Brazil",
                            }
                        ],
                        "orcid": "0000-0003-2847-6556",
                    },
                    {
                        "surname": "Suire",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie, Orsay, France",
                                "organization": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0003-1675-503X",
                    },
                    {
                        "surname": "Sukhanov",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-4506-8071",
                    },
                    {
                        "surname": "Suljic",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-4490-1930",
                    },
                    {
                        "surname": "Sumberia",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Physics Department, University of Jammu, Jammu, India",
                                "organization": "Physics Department",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0001-6779-208X",
                    },
                    {
                        "surname": "Sumowidagdo",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "National Research and Innovation Agency - BRIN, Jakarta, Indonesia",
                                "organization": "National Research and Innovation Agency - BRIN",
                                "country": "Indonesia",
                            }
                        ],
                        "orcid": "0000-0003-4252-8877",
                    },
                    {
                        "surname": "Swain",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Institute of Physics, Homi Bhabha National Institute, Bhubaneswar, India",
                                "organization": "Institute of Physics",
                                "country": "India",
                            }
                        ],
                    },
                    {
                        "surname": "Szabo",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Comenius University Bratislava, Faculty of Mathematics, Physics and Informatics, Bratislava, Slovak Republic",
                                "organization": "Comenius University Bratislava",
                                "country": "Slovak Republic",
                            }
                        ],
                    },
                    {
                        "surname": "Szarka",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Comenius University Bratislava, Faculty of Mathematics, Physics and Informatics, Bratislava, Slovak Republic",
                                "organization": "Comenius University Bratislava",
                                "country": "Slovak Republic",
                            }
                        ],
                        "orcid": "0009-0006-4361-0257",
                    },
                    {
                        "surname": "Tabassam",
                        "given_names": "U.",
                        "affiliations": [
                            {
                                "value": "COMSATS University Islamabad, Islamabad, Pakistan",
                                "organization": "COMSATS University Islamabad",
                                "country": "Pakistan",
                            }
                        ],
                    },
                    {
                        "surname": "Taghavi",
                        "given_names": "S.F.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-2642-5720",
                    },
                    {
                        "surname": "Taillepied",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            },
                            {
                                "value": "Université Clermont Auvergne, CNRS/IN2P3, LPC, Clermont-Ferrand, France",
                                "organization": "Université Clermont Auvergne",
                                "country": "France",
                            },
                        ],
                        "orcid": "0000-0003-3470-2230",
                    },
                    {
                        "surname": "Takahashi",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Universidade Estadual de Campinas (UNICAMP), Campinas, Brazil",
                                "organization": "Universidade Estadual de Campinas (UNICAMP)",
                                "country": "Brazil",
                            }
                        ],
                        "orcid": "0000-0002-4091-1779",
                    },
                    {
                        "surname": "Tambave",
                        "given_names": "G.J.",
                        "affiliations": [
                            {
                                "value": "Department of Physics and Technology, University of Bergen, Bergen, Norway",
                                "organization": "Department of Physics and Technology",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0000-0001-7174-3379",
                    },
                    {
                        "surname": "Tang",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Université Clermont Auvergne, CNRS/IN2P3, LPC, Clermont-Ferrand, France",
                                "organization": "Université Clermont Auvergne",
                                "country": "France",
                            },
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            },
                        ],
                        "orcid": "0000-0002-9413-9534",
                    },
                    {
                        "surname": "Tang",
                        "given_names": "Z.",
                        "affiliations": [
                            {
                                "value": "University of Science and Technology of China, Hefei, China",
                                "organization": "University of Science and Technology of China",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0002-4247-0081",
                    },
                    {
                        "surname": "Tapia Takaki",
                        "given_names": "J.D.",
                        "affiliations": [
                            {
                                "value": "University of Kansas, Lawrence, KS, United States",
                                "organization": "University of Kansas",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-0098-4279",
                    },
                    {
                        "surname": "Tapus",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "University Politehnica of Bucharest, Bucharest, Romania",
                                "organization": "University Politehnica of Bucharest",
                                "country": "Romania",
                            }
                        ],
                    },
                    {
                        "surname": "Tarasovicova",
                        "given_names": "L.A.",
                        "affiliations": [
                            {
                                "value": "Westfälische Wilhelms-Universität Münster, Institut für Kernphysik, Münster, Germany",
                                "organization": "Westfälische Wilhelms-Universität Münster",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-5086-8658",
                    },
                    {
                        "surname": "Tarzila",
                        "given_names": "M.G.",
                        "affiliations": [
                            {
                                "value": "Horia Hulubei National Institute of Physics and Nuclear Engineering, Bucharest, Romania",
                                "organization": "Horia Hulubei National Institute of Physics and Nuclear Engineering",
                                "country": "Romania",
                            }
                        ],
                        "orcid": "0000-0002-8865-9613",
                    },
                    {
                        "surname": "Tauro",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0009-0000-3124-9093",
                    },
                    {
                        "surname": "Telesca",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-6783-7230",
                    },
                    {
                        "surname": "Terlizzi",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-4119-7228",
                    },
                    {
                        "surname": "Terrevoli",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "University of Houston, Houston, TX, United States",
                                "organization": "University of Houston",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-1318-684X",
                    },
                    {
                        "surname": "Tersimonov",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Bogolyubov Institute for Theoretical Physics, National Academy of Sciences of Ukraine, Kiev, Ukraine",
                                "organization": "Bogolyubov Institute for Theoretical Physics",
                                "country": "Ukraine",
                            }
                        ],
                    },
                    {
                        "surname": "Thakur",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Variable Energy Cyclotron Centre, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Variable Energy Cyclotron Centre",
                                "country": "India",
                            }
                        ],
                        "orcid": "0009-0008-2329-5039",
                    },
                    {
                        "surname": "Thomas",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "The University of Texas at Austin, Austin, TX, United States",
                                "organization": "The University of Texas at Austin",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0003-3408-3097",
                    },
                    {
                        "surname": "Tieulent",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Université de Lyon, CNRS/IN2P3, Institut de Physique des 2 Infinis de Lyon, Lyon, France",
                                "organization": "Université de Lyon",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-2106-5415",
                    },
                    {
                        "surname": "Tikhonov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0001-7799-8858",
                    },
                    {
                        "surname": "Timmins",
                        "given_names": "A.R.",
                        "affiliations": [
                            {
                                "value": "University of Houston, Houston, TX, United States",
                                "organization": "University of Houston",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0003-1305-8757",
                    },
                    {
                        "surname": "Tkacik",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Technical University of Košice, Košice, Slovak Republic",
                                "organization": "Technical University of Košice",
                                "country": "Slovak Republic",
                            }
                        ],
                    },
                    {
                        "surname": "Tkacik",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Technical University of Košice, Košice, Slovak Republic",
                                "organization": "Technical University of Košice",
                                "country": "Slovak Republic",
                            }
                        ],
                        "orcid": "0000-0001-8308-7882",
                    },
                    {
                        "surname": "Toia",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-9567-3360",
                    },
                    {
                        "surname": "Topilskaya",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-5137-3582",
                    },
                    {
                        "surname": "Toppi",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "INFN, Laboratori Nazionali di Frascati, Frascati, Italy",
                                "organization": "INFN, Laboratori Nazionali di Frascati",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-0392-0895",
                    },
                    {
                        "surname": "Torales-Acosta",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, University of California, Berkeley, CA, United States",
                                "organization": "Department of Physics",
                                "country": "United States",
                            }
                        ],
                    },
                    {
                        "surname": "Tork",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie, Orsay, France",
                                "organization": "Laboratoire de Physique des 2 Infinis, Irène Joliot-Curie",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0001-9753-329X",
                    },
                    {
                        "surname": "Torres Ramos",
                        "given_names": "A.G.",
                        "affiliations": [
                            {
                                "value": "Dipartimento Interateneo di Fisica ‘M. Merlin’ and Sezione INFN, Bari, Italy",
                                "organization": "Dipartimento Interateneo di Fisica ‘M. Merlin’",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-3997-0883",
                    },
                    {
                        "surname": "Trifiró",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Scienze MIFT, Università di Messina, Messina, Italy",
                                "organization": "Dipartimento di Scienze MIFT",
                                "country": "Italy",
                            },
                            {
                                "value": "INFN, Sezione di Catania, Catania, Italy",
                                "organization": "INFN, Sezione di Catania",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0003-1078-1157",
                    },
                    {
                        "surname": "Triolo",
                        "given_names": "A.S.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Scienze MIFT, Università di Messina, Messina, Italy",
                                "organization": "Dipartimento di Scienze MIFT",
                                "country": "Italy",
                            },
                            {
                                "value": "INFN, Sezione di Catania, Catania, Italy",
                                "organization": "INFN, Sezione di Catania",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0009-0002-7570-5972",
                    },
                    {
                        "surname": "Tripathy",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bologna, Bologna, Italy",
                                "organization": "INFN, Sezione di Bologna",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-0061-5107",
                    },
                    {
                        "surname": "Tripathy",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Indian Institute of Technology Bombay (IIT), Mumbai, India",
                                "organization": "Indian Institute of Technology Bombay (IIT)",
                                "country": "India",
                            }
                        ],
                        "orcid": "0000-0002-6719-7130",
                    },
                    {
                        "surname": "Trogolo",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0001-7474-5361",
                    },
                    {
                        "surname": "Trubnikov",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Bogolyubov Institute for Theoretical Physics, National Academy of Sciences of Ukraine, Kiev, Ukraine",
                                "organization": "Bogolyubov Institute for Theoretical Physics",
                                "country": "Ukraine",
                            }
                        ],
                        "orcid": "0009-0008-8143-0956",
                    },
                    {
                        "surname": "Trzaska",
                        "given_names": "W.H.",
                        "affiliations": [
                            {
                                "value": "University of Jyväskylä, Jyväskylä, Finland",
                                "organization": "University of Jyväskylä",
                                "country": "Finland",
                            }
                        ],
                        "orcid": "0000-0003-0672-9137",
                    },
                    {
                        "surname": "Trzcinski",
                        "given_names": "T.P.",
                        "affiliations": [
                            {
                                "value": "Warsaw University of Technology, Warsaw, Poland",
                                "organization": "Warsaw University of Technology",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0002-1486-8906",
                    },
                    {
                        "surname": "Turrisi",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Padova, Padova, Italy",
                                "organization": "INFN, Sezione di Padova",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-5272-337X",
                    },
                    {
                        "surname": "Tveter",
                        "given_names": "T.S.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, University of Oslo, Oslo, Norway",
                                "organization": "Department of Physics",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0009-0003-7140-8644",
                    },
                    {
                        "surname": "Ullaland",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "Department of Physics and Technology, University of Bergen, Bergen, Norway",
                                "organization": "Department of Physics and Technology",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0000-0002-0002-8834",
                    },
                    {
                        "surname": "Ulukutlu",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-9554-2256",
                    },
                    {
                        "surname": "Uras",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Université de Lyon, CNRS/IN2P3, Institut de Physique des 2 Infinis de Lyon, Lyon, France",
                                "organization": "Université de Lyon",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0001-7552-0228",
                    },
                    {
                        "surname": "Urioni",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Pavia, Pavia, Italy",
                                "organization": "INFN, Sezione di Pavia",
                                "country": "Italy",
                            },
                            {
                                "value": "Università di Brescia, Brescia, Italy",
                                "organization": "Università di Brescia",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0002-4455-7383",
                    },
                    {
                        "surname": "Usai",
                        "given_names": "G.L.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Cagliari, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-8659-8378",
                    },
                    {
                        "surname": "Vala",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Faculty of Science, P.J. Šafárik University, Košice, Slovak Republic",
                                "organization": "Faculty of Science",
                                "country": "Slovak Republic",
                            }
                        ],
                    },
                    {
                        "surname": "Valle",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica, Università di Pavia, Pavia, Italy",
                                "organization": "Dipartimento di Fisica",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-4041-4788",
                    },
                    {
                        "surname": "Vallero",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Torino, Turin, Italy",
                                "organization": "INFN, Sezione di Torino",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-1264-9651",
                    },
                    {
                        "surname": "van Doremalen",
                        "given_names": "L.V.R.",
                        "affiliations": [
                            {
                                "value": "Institute for Gravitational and Subatomic Physics (GRASP), Utrecht University/Nikhef, Utrecht, Netherlands",
                                "organization": "Institute for Gravitational and Subatomic Physics (GRASP)",
                                "country": "Netherlands",
                            }
                        ],
                    },
                    {
                        "surname": "van Leeuwen",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Nikhef, National institute for subatomic physics, Amsterdam, Netherlands",
                                "organization": "Nikhef, National institute for subatomic physics",
                                "country": "Netherlands",
                            }
                        ],
                        "orcid": "0000-0002-5222-4888",
                    },
                    {
                        "surname": "van Veen",
                        "given_names": "C.A.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-1199-4445",
                    },
                    {
                        "surname": "van Weelden",
                        "given_names": "R.J.G.",
                        "affiliations": [
                            {
                                "value": "Nikhef, National institute for subatomic physics, Amsterdam, Netherlands",
                                "organization": "Nikhef, National institute for subatomic physics",
                                "country": "Netherlands",
                            }
                        ],
                        "orcid": "0000-0003-4389-203X",
                    },
                    {
                        "surname": "Vande Vyvre",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0001-7277-7706",
                    },
                    {
                        "surname": "Varga",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Wigner Research Centre for Physics, Budapest, Hungary",
                                "organization": "Wigner Research Centre for Physics",
                                "country": "Hungary",
                            }
                        ],
                        "orcid": "0000-0002-2450-1331",
                    },
                    {
                        "surname": "Varga",
                        "given_names": "Z.",
                        "affiliations": [
                            {
                                "value": "Wigner Research Centre for Physics, Budapest, Hungary",
                                "organization": "Wigner Research Centre for Physics",
                                "country": "Hungary",
                            }
                        ],
                        "orcid": "0000-0002-1501-5569",
                    },
                    {
                        "surname": "Varga-Kofarago",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Wigner Research Centre for Physics, Budapest, Hungary",
                                "organization": "Wigner Research Centre for Physics",
                                "country": "Hungary",
                            }
                        ],
                        "orcid": "0000-0002-5638-4440",
                    },
                    {
                        "surname": "Vasileiou",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "National and Kapodistrian University of Athens, School of Science, Department of Physics , Athens, Greece",
                                "organization": "National and Kapodistrian University of Athens",
                                "country": "Greece",
                            }
                        ],
                        "orcid": "0000-0002-3160-8524",
                    },
                    {
                        "surname": "Vasiliev",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0009-0000-1676-234X",
                    },
                    {
                        "surname": "Vázquez Doce",
                        "given_names": "O.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-6459-8134",
                    },
                    {
                        "surname": "Vechernin",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0003-1458-8055",
                    },
                    {
                        "surname": "Vercellin",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Turin, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-9030-5347",
                    },
                    {
                        "surname": "Vergara Limón",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "High Energy Physics Group, Universidad Autónoma de Puebla, Puebla, Mexico",
                                "organization": "High Energy Physics Group",
                                "country": "Mexico",
                            }
                        ],
                    },
                    {
                        "surname": "Vermunt",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Institute for Gravitational and Subatomic Physics (GRASP), Utrecht University/Nikhef, Utrecht, Netherlands",
                                "organization": "Institute for Gravitational and Subatomic Physics (GRASP)",
                                "country": "Netherlands",
                            }
                        ],
                        "orcid": "0000-0002-2640-1342",
                    },
                    {
                        "surname": "Vértesi",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Wigner Research Centre for Physics, Budapest, Hungary",
                                "organization": "Wigner Research Centre for Physics",
                                "country": "Hungary",
                            }
                        ],
                        "orcid": "0000-0003-3706-5265",
                    },
                    {
                        "surname": "Verweij",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Institute for Gravitational and Subatomic Physics (GRASP), Utrecht University/Nikhef, Utrecht, Netherlands",
                                "organization": "Institute for Gravitational and Subatomic Physics (GRASP)",
                                "country": "Netherlands",
                            }
                        ],
                        "orcid": "0000-0002-1504-3420",
                    },
                    {
                        "surname": "Vickovic",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Faculty of Electrical Engineering, Mechanical Engineering and Naval Architecture, University of Split, Split, Croatia",
                                "organization": "Faculty of Electrical Engineering, Mechanical Engineering and Naval Architecture",
                                "country": "Croatia",
                            }
                        ],
                    },
                    {
                        "surname": "Vilakazi",
                        "given_names": "Z.",
                        "affiliations": [
                            {
                                "value": "University of the Witwatersrand, Johannesburg, South Africa",
                                "organization": "University of the Witwatersrand",
                                "country": "South Africa",
                            }
                        ],
                    },
                    {
                        "surname": "Villalobos Baillie",
                        "given_names": "O.",
                        "affiliations": [
                            {
                                "value": "School of Physics and Astronomy, University of Birmingham, Birmingham, United Kingdom",
                                "organization": "School of Physics and Astronomy",
                                "country": "United Kingdom",
                            }
                        ],
                        "orcid": "0000-0002-0983-6504",
                    },
                    {
                        "surname": "Vino",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "INFN, Sezione di Bari, Bari, Italy",
                                "organization": "INFN, Sezione di Bari",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-8470-3648",
                    },
                    {
                        "surname": "Vinogradov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-8850-8540",
                    },
                    {
                        "surname": "Virgili",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica ‘E.R. Caianiello’ dell'Università and Gruppo Collegato INFN, Salerno, Italy",
                                "organization": "Dipartimento di Fisica ‘E.R. Caianiello’ dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-0471-7052",
                    },
                    {
                        "surname": "Vislavicius",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Niels Bohr Institute, University of Copenhagen, Copenhagen, Denmark",
                                "organization": "Niels Bohr Institute",
                                "country": "Denmark",
                            }
                        ],
                    },
                    {
                        "surname": "Vodopyanov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0009-0003-4952-2563",
                    },
                    {
                        "surname": "Volkel",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-8982-5548",
                    },
                    {
                        "surname": "Völkl",
                        "given_names": "M.A.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-3478-4259",
                    },
                    {
                        "surname": "Voloshin",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                    },
                    {
                        "surname": "Voloshin",
                        "given_names": "S.A.",
                        "affiliations": [
                            {
                                "value": "Wayne State University, Detroit, MI, United States",
                                "organization": "Wayne State University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0002-1330-9096",
                    },
                    {
                        "surname": "Volpe",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Dipartimento Interateneo di Fisica ‘M. Merlin’ and Sezione INFN, Bari, Italy",
                                "organization": "Dipartimento Interateneo di Fisica ‘M. Merlin’",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0002-2921-2475",
                    },
                    {
                        "surname": "von Haller",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-3422-4585",
                    },
                    {
                        "surname": "Vorobyev",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Physik Department, Technische Universität München, Munich, Germany",
                                "organization": "Physik Department",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0002-2218-6905",
                    },
                    {
                        "surname": "Vozniuk",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-2784-4516",
                    },
                    {
                        "surname": "Vrláková",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Faculty of Science, P.J. Šafárik University, Košice, Slovak Republic",
                                "organization": "Faculty of Science",
                                "country": "Slovak Republic",
                            }
                        ],
                        "orcid": "0000-0002-5846-8496",
                    },
                    {
                        "surname": "Wagner",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Department of Physics and Technology, University of Bergen, Bergen, Norway",
                                "organization": "Department of Physics and Technology",
                                "country": "Norway",
                            }
                        ],
                    },
                    {
                        "surname": "Wang",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Fudan University, Shanghai, China",
                                "organization": "Fudan University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0001-5383-0970",
                    },
                    {
                        "surname": "Wang",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Fudan University, Shanghai, China",
                                "organization": "Fudan University",
                                "country": "China",
                            }
                        ],
                    },
                    {
                        "surname": "Weber",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Stefan Meyer Institut für Subatomare Physik (SMI), Vienna, Austria",
                                "organization": "Stefan Meyer Institut für Subatomare Physik (SMI)",
                                "country": "Austria",
                            }
                        ],
                        "orcid": "0000-0001-5742-294X",
                    },
                    {
                        "surname": "Wegrzynek",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-3155-0887",
                    },
                    {
                        "surname": "Weiglhofer",
                        "given_names": "F.T.",
                        "affiliations": [
                            {
                                "value": "Frankfurt Institute for Advanced Studies, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Frankfurt Institute for Advanced Studies",
                                "country": "Germany",
                            }
                        ],
                    },
                    {
                        "surname": "Wenzel",
                        "given_names": "S.C.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-3495-4131",
                    },
                    {
                        "surname": "Wessels",
                        "given_names": "J.P.",
                        "affiliations": [
                            {
                                "value": "Westfälische Wilhelms-Universität Münster, Institut für Kernphysik, Münster, Germany",
                                "organization": "Westfälische Wilhelms-Universität Münster",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-1339-286X",
                    },
                    {
                        "surname": "Weyhmiller",
                        "given_names": "S.L.",
                        "affiliations": [
                            {
                                "value": "Yale University, New Haven, CT, United States",
                                "organization": "Yale University",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0000-0001-5405-3480",
                    },
                    {
                        "surname": "Wiechula",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Institut für Kernphysik, Johann Wolfgang Goethe-Universität Frankfurt, Frankfurt, Germany",
                                "organization": "Institut für Kernphysik",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0001-9201-8114",
                    },
                    {
                        "surname": "Wikne",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, University of Oslo, Oslo, Norway",
                                "organization": "Department of Physics",
                                "country": "Norway",
                            }
                        ],
                        "orcid": "0009-0005-9617-3102",
                    },
                    {
                        "surname": "Wilk",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "National Centre for Nuclear Research, Warsaw, Poland",
                                "organization": "National Centre for Nuclear Research",
                                "country": "Poland",
                            }
                        ],
                        "orcid": "0000-0001-5584-2860",
                    },
                    {
                        "surname": "Wilkinson",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0003-0689-2858",
                    },
                    {
                        "surname": "Willems",
                        "given_names": "G.A.",
                        "affiliations": [
                            {
                                "value": "Westfälische Wilhelms-Universität Münster, Institut für Kernphysik, Münster, Germany",
                                "organization": "Westfälische Wilhelms-Universität Münster",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0000-9939-3892",
                    },
                    {
                        "surname": "Windelband",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0007-2759-5453",
                    },
                    {
                        "surname": "Winn",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA), IRFU, Départment de Physique Nucléaire (DPhN), Saclay, France",
                                "organization": "Université Paris-Saclay Centre d'Etudes de Saclay (CEA)",
                                "country": "France",
                            }
                        ],
                        "orcid": "0000-0002-2207-0101",
                    },
                    {
                        "surname": "Wright",
                        "given_names": "J.R.",
                        "affiliations": [
                            {
                                "value": "The University of Texas at Austin, Austin, TX, United States",
                                "organization": "The University of Texas at Austin",
                                "country": "United States",
                            }
                        ],
                        "orcid": "0009-0006-9351-6517",
                    },
                    {
                        "surname": "Wu",
                        "given_names": "W.",
                        "affiliations": [
                            {
                                "value": "Fudan University, Shanghai, China",
                                "organization": "Fudan University",
                                "country": "China",
                            }
                        ],
                    },
                    {
                        "surname": "Wu",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "University of Science and Technology of China, Hefei, China",
                                "organization": "University of Science and Technology of China",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0003-2991-9849",
                    },
                    {
                        "surname": "Xu",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0003-4674-9482",
                    },
                    {
                        "surname": "Yadav",
                        "given_names": "A.K.",
                        "affiliations": [
                            {
                                "value": "Variable Energy Cyclotron Centre, Homi Bhabha National Institute, Kolkata, India",
                                "organization": "Variable Energy Cyclotron Centre",
                                "country": "India",
                            }
                        ],
                        "orcid": "0009-0003-9300-0439",
                    },
                    {
                        "surname": "Yalcin",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "KTO Karatay University, Konya, Turkey",
                                "organization": "KTO Karatay University",
                                "country": "Turkey",
                            }
                        ],
                        "orcid": "0000-0001-8905-8089",
                    },
                    {
                        "surname": "Yamaguchi",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Physics Program and International Institute for Sustainability with Knotted Chiral Meta Matter (SKCM2), Hiroshima University, Hiroshima, Japan",
                                "organization": "Physics Program and International Institute for Sustainability with Knotted Chiral Meta Matter (SKCM2)",
                                "country": "Japan",
                            }
                        ],
                        "orcid": "0009-0009-3842-7345",
                    },
                    {
                        "surname": "Yamakawa",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "Physics Program and International Institute for Sustainability with Knotted Chiral Meta Matter (SKCM2), Hiroshima University, Hiroshima, Japan",
                                "organization": "Physics Program and International Institute for Sustainability with Knotted Chiral Meta Matter (SKCM2)",
                                "country": "Japan",
                            }
                        ],
                    },
                    {
                        "surname": "Yang",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Department of Physics and Technology, University of Bergen, Bergen, Norway",
                                "organization": "Department of Physics and Technology",
                                "country": "Norway",
                            }
                        ],
                    },
                    {
                        "surname": "Yano",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Physics Program and International Institute for Sustainability with Knotted Chiral Meta Matter (SKCM2), Hiroshima University, Hiroshima, Japan",
                                "organization": "Physics Program and International Institute for Sustainability with Knotted Chiral Meta Matter (SKCM2)",
                                "country": "Japan",
                            }
                        ],
                        "orcid": "0000-0002-5563-1884",
                    },
                    {
                        "surname": "Yin",
                        "given_names": "Z.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0003-4532-7544",
                    },
                    {
                        "surname": "Yoo",
                        "given_names": "I.-K.",
                        "affiliations": [
                            {
                                "value": "Department of Physics, Pusan National University, Pusan, Republic of Korea",
                                "organization": "Department of Physics",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0002-2835-5941",
                    },
                    {
                        "surname": "Yoon",
                        "given_names": "J.H.",
                        "affiliations": [
                            {
                                "value": "Inha University, Incheon, Republic of Korea",
                                "organization": "Inha University",
                                "country": "Republic of Korea",
                            }
                        ],
                        "orcid": "0000-0001-7676-0821",
                    },
                    {
                        "surname": "Yuan",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Department of Physics and Technology, University of Bergen, Bergen, Norway",
                                "organization": "Department of Physics and Technology",
                                "country": "Norway",
                            }
                        ],
                    },
                    {
                        "surname": "Yuncu",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0000-0001-9696-9331",
                    },
                    {
                        "surname": "Zaccolo",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Dipartimento di Fisica dell'Università and Sezione INFN, Trieste, Italy",
                                "organization": "Dipartimento di Fisica dell'Università",
                                "country": "Italy",
                            }
                        ],
                        "orcid": "0000-0003-3128-3157",
                    },
                    {
                        "surname": "Zampolli",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            }
                        ],
                        "orcid": "0000-0002-2608-4834",
                    },
                    {
                        "surname": "Zanoli",
                        "given_names": "H.J.C.",
                        "affiliations": [
                            {
                                "value": "Institute for Gravitational and Subatomic Physics (GRASP), Utrecht University/Nikhef, Utrecht, Netherlands",
                                "organization": "Institute for Gravitational and Subatomic Physics (GRASP)",
                                "country": "Netherlands",
                            }
                        ],
                    },
                    {
                        "surname": "Zanone",
                        "given_names": "F.",
                        "affiliations": [
                            {
                                "value": "Physikalisches Institut, Ruprecht-Karls-Universität Heidelberg, Heidelberg, Germany",
                                "organization": "Physikalisches Institut",
                                "country": "Germany",
                            }
                        ],
                        "orcid": "0009-0005-9061-1060",
                    },
                    {
                        "surname": "Zardoshti",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "European Organization for Nuclear Research (CERN), Geneva, Switzerland",
                                "organization": "European Organization for Nuclear Research (CERN)",
                                "country": "Switzerland",
                            },
                            {
                                "value": "School of Physics and Astronomy, University of Birmingham, Birmingham, United Kingdom",
                                "organization": "School of Physics and Astronomy",
                                "country": "United Kingdom",
                            },
                        ],
                        "orcid": "0009-0006-3929-209X",
                    },
                    {
                        "surname": "Zarochentsev",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-3502-8084",
                    },
                    {
                        "surname": "Závada",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Institute of Physics of the Czech Academy of Sciences, Prague, Czech Republic",
                                "organization": "Institute of Physics of the Czech Academy of Sciences",
                                "country": "Czech Republic",
                            }
                        ],
                        "orcid": "0000-0002-8296-2128",
                    },
                    {
                        "surname": "Zaviyalov",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                    },
                    {
                        "surname": "Zhalov",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0003-0419-321X",
                    },
                    {
                        "surname": "Zhang",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0001-6097-1878",
                    },
                    {
                        "surname": "Zhang",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Fudan University, Shanghai, China",
                                "organization": "Fudan University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0003-2782-7801",
                    },
                    {
                        "surname": "Zhang",
                        "given_names": "X.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0002-1881-8711",
                    },
                    {
                        "surname": "Zhang",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "University of Science and Technology of China, Hefei, China",
                                "organization": "University of Science and Technology of China",
                                "country": "China",
                            }
                        ],
                    },
                    {
                        "surname": "Zhao",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "China Institute of Atomic Energy, Beijing, China",
                                "organization": "China Institute of Atomic Energy",
                                "country": "China",
                            }
                        ],
                        "orcid": "0000-0002-2858-2167",
                    },
                    {
                        "surname": "Zherebchevskii",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                        "orcid": "0000-0002-6021-5113",
                    },
                    {
                        "surname": "Zhi",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "China Institute of Atomic Energy, Beijing, China",
                                "organization": "China Institute of Atomic Energy",
                                "country": "China",
                            }
                        ],
                    },
                    {
                        "surname": "Zhigareva",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN"
                            }
                        ],
                    },
                    {
                        "surname": "Zhou",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                        "orcid": "0009-0009-2528-906X",
                    },
                    {
                        "surname": "Zhou",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Niels Bohr Institute, University of Copenhagen, Copenhagen, Denmark",
                                "organization": "Niels Bohr Institute",
                                "country": "Denmark",
                            }
                        ],
                        "orcid": "0000-0002-7868-6706",
                    },
                    {
                        "surname": "Zhu",
                        "given_names": "J.",
                        "affiliations": [
                            {
                                "value": "Research Division and ExtreMe Matter Institute EMMI, GSI Helmholtzzentrum für Schwerionenforschung GmbH, Darmstadt, Germany",
                                "organization": "Research Division",
                                "country": "Germany",
                            },
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            },
                        ],
                        "orcid": "0000-0001-9358-5762",
                    },
                    {
                        "surname": "Zhu",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Central China Normal University, Wuhan, China",
                                "organization": "Central China Normal University",
                                "country": "China",
                            }
                        ],
                    },
                    {
                        "surname": "Zinovjev",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Bogolyubov Institute for Theoretical Physics, National Academy of Sciences of Ukraine, Kiev, Ukraine",
                                "organization": "Bogolyubov Institute for Theoretical Physics",
                                "country": "Ukraine",
                            }
                        ],
                    },
                    {
                        "surname": "Zurlo",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Università di Brescia, Brescia, Italy",
                                "organization": "Università di Brescia",
                                "country": "Italy",
                            },
                            {
                                "value": "INFN, Sezione di Pavia, Pavia, Italy",
                                "organization": "INFN, Sezione di Pavia",
                                "country": "Italy",
                            },
                        ],
                        "orcid": "0000-0002-7478-2493",
                    },
                ],
                [
                    {
                        "surname": "Gialamas",
                        "given_names": "Ioannis D.",
                        "affiliations": [
                            {
                                "value": "Laboratory of High Energy and Computational Physics, National Institute of Chemical Physics and Biophysics, Rävala pst. 10, 10143, Tallinn, Estonia",
                                "organization": "Laboratory of High Energy and Computational Physics",
                                "country": "Estonia",
                            }
                        ],
                        "email": "ioannis.gialamas@kbfi.ee",
                        "orcid": "0000-0002-2957-5276",
                    },
                    {
                        "surname": "Veermäe",
                        "given_names": "Hardi",
                        "affiliations": [
                            {
                                "value": "Laboratory of High Energy and Computational Physics, National Institute of Chemical Physics and Biophysics, Rävala pst. 10, 10143, Tallinn, Estonia",
                                "organization": "Laboratory of High Energy and Computational Physics",
                                "country": "Estonia",
                            }
                        ],
                        "email": "hardi.veermae@cern.ch",
                    },
                ],
                [
                    {
                        "surname": "Armesto",
                        "given_names": "Néstor",
                        "affiliations": [
                            {
                                "value": "Instituto Galego de Física de Altas Enerxías IGFAE, Universidade de Santiago de Compostela, Santiago de Compostela, 15782, Galicia, Spain",
                                "organization": "Instituto Galego de Física de Altas Enerxías IGFAE",
                                "country": "Spain",
                            }
                        ],
                        "email": "nestor.armesto@usc.es",
                    },
                    {
                        "surname": "Escobedo",
                        "given_names": "Miguel Ángel",
                        "affiliations": [
                            {
                                "value": "Departament de Física Quàntica i Astrofísica and Institut de Ciències del Cosmos, Universitat de Barcelona, Martí i Franquès 1, Barcelona, 08028, Catalonia, Spain",
                                "organization": "Departament de Física Quàntica i Astrofísica",
                                "country": "Spain",
                            }
                        ],
                        "email": "miguel.a.escobedo@fqa.ub.edu",
                        "orcid": "0000-0002-0123-3223",
                    },
                    {
                        "surname": "Ferreiro",
                        "given_names": "Elena G.",
                        "affiliations": [
                            {
                                "value": "Instituto Galego de Física de Altas Enerxías IGFAE, Universidade de Santiago de Compostela, Santiago de Compostela, 15782, Galicia, Spain",
                                "organization": "Instituto Galego de Física de Altas Enerxías IGFAE",
                                "country": "Spain",
                            }
                        ],
                        "email": "elena.gonzalez.ferreiro@usc.es",
                    },
                    {
                        "surname": "López-Pardo",
                        "given_names": "Víctor",
                        "affiliations": [
                            {
                                "value": "Instituto Galego de Física de Altas Enerxías IGFAE, Universidade de Santiago de Compostela, Santiago de Compostela, 15782, Galicia, Spain",
                                "organization": "Instituto Galego de Física de Altas Enerxías IGFAE",
                                "country": "Spain",
                            }
                        ],
                        "email": "victorlopez.pardo@usc.es",
                        "orcid": "0009-0001-8965-382X",
                    },
                ],
            ],
            "authors",
            id="test_authors",
        ),
        param(
            [
                "European Center of Nuclear Research, ALICE experiment",
                "The Author(s)",
                "The Author(s)",
                "The Author(s)",
                "The Author(s)",
            ],
            "copyright_holder",
            id="test_copyright_holder",
        ),
        param(
            ["2023", "2023", "2023", "2023", "2025"],
            "copyright_year",
            id="test_copyright_year",
        ),
        param(
            [
                "European Center of Nuclear Research, ALICE experiment",
                "The Author(s)",
                "The Author(s)",
                "The Author(s)",
                "The Author(s)",
            ],
            "copyright_statement",
            id="test_copyright_statement",
        ),
        param(
            [
                "article",
                "article",
                "article",
                "article",
                "erratum",
            ],
            "journal_doctype",
            id="test_journal_doctype",
        ),
    ],
)
def test_elsevier_parsing(parsed_articles, expected, key):
    for (expected_value, article) in zip(expected, parsed_articles):
        assert article[key] == expected_value

        SKIP_ENHANCE_FOR = [
            "abstract",
            "title",
            "copyright_holder",
            "copyright_year",
            "copyright_statement",
        ]

        if key not in SKIP_ENHANCE_FOR:
            if key == "authors":
                for author in expected_value:
                    for aff in author.get("affiliations", []):
                        if aff.get("country") == "Republic of Korea":
                            aff["country"] = "South Korea"
                        if aff.get("country") == "Slovak Republic":
                            aff["country"] = "Slovakia"
                        if aff.get("country") == "United States":
                            aff["country"] = "USA"
                        if aff.get("country") == "United Kingdom":
                            aff["country"] = "UK"

            assert Enhancer()("Elsevier", article)[key] == expected_value


def test_multiple_author_groups(shared_datadir, parser):
    with open(shared_datadir / "multiple_author_groups.xml", "rb") as file:
        xml_content_bytes = BytesIO(file.read())
        article = parse_without_names_spaces(xml_content_bytes)

    parsed_multiple_author_groups_articles = parser._publisher_specific_parsing(article)

    with open(shared_datadir / "expected_authors.json") as file:
        expected_authors = json.loads(file.read())
    assert parsed_multiple_author_groups_articles.get("authors") == expected_authors


def test_wrong_namespaces(shared_datadir, parser):
    with open(shared_datadir / "wrong_namespaces.xml", "rb") as file:
        xml_content_bytes = BytesIO(file.read())
        article = parse_without_names_spaces(xml_content_bytes)

        parsed_article = parser._publisher_specific_parsing(article)

    with open(shared_datadir / "no_namespaces_expected.json") as file:
        expected_article = json.loads(file.read())
    assert parsed_article == expected_article
