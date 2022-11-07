import xml.etree.ElementTree as ET

from common.parsing.xml_extractors import RequiredFieldNotFoundExtractionError
from iop.parser import IOPParser
from pytest import fixture, raises


@fixture(scope="module")
def iop_parser():
    yield IOPParser()


@fixture
def happy_path_article(shared_datadir):
    with open(shared_datadir / "example1.xml") as f:
        return ET.fromstring(f.read())


@fixture
def parsed_happy_path_article(iop_parser, happy_path_article):
    yield iop_parser._publisher_specific_parsing(happy_path_article)


def test_happy_path_article(parsed_happy_path_article):
    print(parsed_happy_path_article["title"])
    assert (
        'Solar, terrestrial, and supernova neutrino experiments are subject to muon-induced radioactive background. The China Jinping Underground Laboratory (CJPL), with its unique advantage of a 2400 m rock coverage and long distance from nuclear power plants, is ideal for MeV-scale neutrino experiments. Using a 1-ton prototype detector of the Jinping Neutrino Experiment (JNE), we detected 343 high-energy cosmic-ray muons and (7.86<inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_8_085001_M1.jpg" ns0:type="simple" /></inline-formula>3.97) muon-induced neutrons from an 820.28-day dataset at the first phase of CJPL (CJPL-I). Based on the muon-induced neutrons, we measured the corresponding muon-induced neutron yield in a liquid scintillator to be<inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_8_085001_M2.jpg" ns0:type="simple" /></inline-formula><inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_8_085001_M2-1.jpg" ns0:type="simple" /></inline-formula>&#956;<sup>&#8722;1</sup>g<sup>&#8722;1</sup>cm<sup>2</sup>at an average muon energy of 340 GeV. We provided the first study for such neutron background at CJPL. A global fit including this measurement shows a power-law coefficient of (0.75<inline-formula xmlns:ns0="http://www.w3.org/1999/xlink"><tex-math></tex-math><inline-graphic ns0:href="cpc_46_8_085001_M3.jpg" ns0:type="simple" /></inline-formula>0.02) for the dependence of the neutron yield at the liquid scintillator on muon energy.'
        == parsed_happy_path_article["abstract"]
    )
    assert (
        'Measurement of muon-induced neutron yield at the China Jinping Underground Laboratory<xref ref-type="fn" rid="cpc_46_8_085001_fn1">*</xref><fn id="cpc_46_8_085001_fn1"><label>*</label><p>Supported in part by the National Natural Science Foundation of China (11620101004, 11475093, 12127808), the Key Laboratory of Particle &amp; Radiation Imaging (TsinghuaUniversity), the CAS Center for Excellence in Particle Physics (CCEPP), and Guangdong Basic and Applied Basic Research Foundation (2019A1515012216). Portion of this work performed at Brookhaven National Laboratory is supported in part by the United States Department of Energy (DE-SC0012704)</p></fn>'
        == parsed_happy_path_article["title"]
    )


@fixture
def article_without_abstract(shared_datadir):
    with open(shared_datadir / "without_abstract.xml") as f:
        return ET.fromstring(f.read())


def test_parsed_article_without_abstract(iop_parser, article_without_abstract):
    with raises(RequiredFieldNotFoundExtractionError):
        assert iop_parser._publisher_specific_parsing(article_without_abstract)


@fixture
def article_without_title(shared_datadir):
    with open(shared_datadir / "without_title.xml") as f:
        return ET.fromstring(f.read())


def test_parsed_article_without_title(iop_parser, article_without_title):
    with raises(RequiredFieldNotFoundExtractionError):
        assert iop_parser._publisher_specific_parsing(article_without_title)


@fixture
def article_with_empty_title(shared_datadir):
    with open(shared_datadir / "with_empty_title.xml") as f:
        return ET.fromstring(f.read())


def test_parsed_article_with_empty_title(iop_parser, article_with_empty_title):
    with raises(RequiredFieldNotFoundExtractionError):
        assert iop_parser._publisher_specific_parsing(article_with_empty_title)
