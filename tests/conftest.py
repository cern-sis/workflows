import unittest

import airflow
import pytest

print("Initilized environment with", airflow.__name__)


@pytest.fixture(scope="session")
def test_case_instance():
    return unittest.TestCase()


@pytest.fixture(scope="session")
def assertListEqual(test_case_instance):
    return lambda first, second: test_case_instance.assertCountEqual(first, second)
