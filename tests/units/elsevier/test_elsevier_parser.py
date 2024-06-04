from common.utils import parse_without_names_spaces
from elsevier.parser import ElsevierParser
from pytest import fixture, mark, param
from common.enhancer import Enhancer


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
    ]
    for filename in file_names:
        with open(shared_datadir / filename) as file:
            articles.append(parse_without_names_spaces(file.read()))
    return articles


@fixture()
def parsed_articles(parser, articles):
    return [parser._publisher_specific_parsing(article) for article in articles]

@fixture()
def enhanced_articles(parser, parsed_articles):
    return [Enhancer()("Elsevier", parser._publisher_specific_parsing(article)) for article in parsed_articles]


@mark.parametrize(
    "expected, key",
    [
        param(
            [
                ["10.1016/j.physletb.2023.137730"],
                ["10.1016/j.physletb.2023.138173"],
                ["10.1016/j.physletb.2022.137649"],
                ["10.1016/j.physletb.2023.138109"],
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
                    },
                    {
                        "surname": "Akindinov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Aleksandrov",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Altsybeev",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Batyunya",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN",
                                # "country": "CERN"
                            }
                        ],
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
                    },
                    {
                        "surname": "Belokurova",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
                    },
                    {
                        "surname": "Belyaev",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Berdnikov",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Blau",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Bogdanov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
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
                    },
                    {
                        "surname": "Bolozdynya",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Borissov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Budnikov",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Ceballos Sanchez",
                        "given_names": "C.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN",
                                # "country": "CERN"
                            }
                        ],
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
                    },
                    {
                        "surname": "Diaz",
                        "given_names": "R.A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN",
                                # "country": "CERN"
                            },
                            {
                                "value": "Centro de Aplicaciones Tecnológicas y Desarrollo Nuclear (CEADEN), Havana, Cuba",
                                "organization": "Centro de Aplicaciones Tecnológicas y Desarrollo Nuclear (CEADEN)",
                                "country": "Cuba",
                            },
                        ],
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
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Evdokimov",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Feofilov",
                        "given_names": "G.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Finogeev",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Fokin",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Furs",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Grigoriev",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
                    },
                    {
                        "surname": "Grigoryan",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN",
                                # "country": "CERN"
                            },
                            {
                                "value": "A.I. Alikhanyan National Science Laboratory (Yerevan Physics Institute) Foundation, Yerevan, Armenia",
                                "organization": "A.I. Alikhanyan National Science Laboratory (Yerevan Physics Institute) Foundation",
                                "country": "Armenia",
                            },
                        ],
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
                    },
                    {
                        "surname": "Ilkaev",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
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
                    },
                    {
                        "surname": "Ippolitov",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Ivanov",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
                    },
                    {
                        "surname": "Izucheev",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
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
                    },
                    {
                        "surname": "Kaplin",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Karavichev",
                        "given_names": "O.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
                    },
                    {
                        "surname": "Karavicheva",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Karpechev",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
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
                    },
                    {
                        "surname": "Khanzadeev",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
                    },
                    {
                        "surname": "Kharlov",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Kiselev",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN",
                                # "country": "CERN"
                            }
                        ],
                    },
                    {
                        "surname": "Kondratyeva",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
                    },
                    {
                        "surname": "Kondratyuk",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Kovalenko",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Kryshen",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Kurepin",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
                    },
                    {
                        "surname": "Kurepin",
                        "given_names": "A.B.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Lazareva",
                        "given_names": "T.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Loginov",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
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
                    },
                    {
                        "surname": "Maevskaya",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
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
                    },
                    {
                        "surname": "Malaev",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Malinina",
                        "given_names": "L.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN",
                                # "country": "CERN"
                            }
                        ],
                    },
                    {
                        "surname": "Mal'Kevich",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Manko",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Mikhaylov",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN",
                                # "country": "CERN"
                            },
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            },
                        ],
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
                    },
                    {
                        "surname": "Morozov",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Nesterov",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Nikolaev",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
                    },
                    {
                        "surname": "Nikulin",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
                    },
                    {
                        "surname": "Nikulin",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Nomokonov",
                        "given_names": "P.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN",
                                # "country": "CERN"
                            }
                        ],
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
                    },
                    {
                        "surname": "Nyanin",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Okorokov",
                        "given_names": "V.A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Peresunko",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Pestov",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
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
                    },
                    {
                        "surname": "Petrov",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Pozdniakov",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN",
                                # "country": "CERN"
                            }
                        ],
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
                    },
                    {
                        "surname": "Pshenichnov",
                        "given_names": "I.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Riabov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
                    },
                    {
                        "surname": "Riabov",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Rogalev",
                        "given_names": "R.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
                    },
                    {
                        "surname": "Rogochaya",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN",
                                # "country": "CERN"
                            }
                        ],
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
                    },
                    {
                        "surname": "Rumyantsev",
                        "given_names": "B.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN",
                                # "country": "CERN"
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
                    },
                    {
                        "surname": "Ryabinkin",
                        "given_names": "E.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
                    },
                    {
                        "surname": "Ryabov",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Sadovsky",
                        "given_names": "S.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            },
                        ],
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
                    },
                    {
                        "surname": "Serebryakov",
                        "given_names": "D.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Shabanov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
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
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Sibiriak",
                        "given_names": "Y.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Sukhanov",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Tikhonov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Topilskaya",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Vasiliev",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Vechernin",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Vinogradov",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                                "value": "Affiliated with an international laboratory covered by a cooperation agreement with CERN",
                                # "country": "CERN"
                            }
                        ],
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
                    },
                    {
                        "surname": "Voloshin",
                        "given_names": "K.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
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
                    },
                    {
                        "surname": "Vozniuk",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Zarochentsev",
                        "given_names": "A.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Zaviyalov",
                        "given_names": "N.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
                    },
                    {
                        "surname": "Zhalov",
                        "given_names": "M.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                    },
                    {
                        "surname": "Zherebchevskii",
                        "given_names": "V.",
                        "affiliations": [
                            {
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
                            }
                        ],
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
                                "value": "Affiliated with an institute covered by a cooperation agreement with CERN",
                                # "country": "CERN",
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
            ],
            "copyright_holder",
            id="test_copyright_holder",
        ),
        param(
            ["2023", "2023", "2023", "2023"],
            "copyright_year",
            id="test_copyright_year",
        ),
        param(
            [
                "European Center of Nuclear Research, ALICE experiment",
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
            if key =="authors":
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
