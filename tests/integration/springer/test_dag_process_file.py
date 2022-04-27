import base64
import datetime
import xml.etree.ElementTree as ET
from zipfile import ZipFile

from airflow import DAG
from airflow.models import DagBag
from airflow.utils.state import DagRunState
from busypie import SECOND, wait
from pytest import fixture, raises
from springer.dag_process_file import springer_parse_file

DAG_NAME = "springer_process_file"


@fixture
def dag():
    dagbag = DagBag(dag_folder="dags/", include_examples=False)
    assert dagbag.import_errors.get(f"dags/{DAG_NAME}.py") is None
    return dagbag.get_dag(dag_id=DAG_NAME)


@fixture
def article():
    data_dir = "./data/"
    test_file = "ftp_PUB_19-01-29_20-02-10_JHEP.zip"

    def extract_zip_to_article(zip_filename):
        with ZipFile(zip_filename, "r") as zip_file:
            return [
                zip_file.read(filename)
                for filename in map(lambda x: x.filename, zip_file.filelist)
                if ".Meta" in filename or ".scoap" in filename
            ][0]

    article = ET.fromstring(extract_zip_to_article(data_dir + test_file))

    return article


def test_dag_loaded(dag: DAG):
    assert dag is not None
    assert len(dag.tasks) == 1


def test_dag_run(dag: DAG, article):
    id = datetime.datetime.utcnow().strftime(
        "test_springer_dag_process_file_%Y-%m-%dT%H:%M:%S.%f"
    )
    dagrun = dag.create_dagrun(
        DagRunState.QUEUED,
        run_id=id,
        conf={"file": base64.b64encode(ET.tostring(article)).decode()},
    )
    wait().at_most(60, SECOND).until(lambda: __test_dagrun_state(dagrun))


def test_dag_run_no_input_file(dag: DAG):
    id = datetime.datetime.utcnow().strftime(
        "test_springer_dag_process_file_%Y-%m-%dT%H:%M:%S.%f"
    )
    dagrun = dag.create_dagrun(DagRunState.QUEUED, run_id=id)
    wait().at_most(60, SECOND).until(lambda: __test_dagrun_fails(dagrun))


def test_dag_process_file(article):
    springer_parse_file(
        params={"file": base64.b64encode(ET.tostring(article)).decode()}
    )


def test_dag_process_file_no_input_file(article):
    raises(Exception, springer_parse_file)


def __test_dagrun_fails(dagrun):
    dagrun.update_state()
    return not dagrun.get_state() == DagRunState.FAILED


def __test_dagrun_state(dagrun):
    dagrun.update_state()
    assert dagrun.get_state() != DagRunState.FAILED
    return (
        not dagrun.get_state() == DagRunState.QUEUED
        and not dagrun.get_state() == DagRunState.RUNNING
    )
