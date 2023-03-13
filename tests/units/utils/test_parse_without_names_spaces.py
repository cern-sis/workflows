import os

from common.utils import parse_without_names_spaces


def test_parse_without_names_spaces(shared_datadir):
    file_names = os.listdir(shared_datadir)
    for file_name in file_names:
        with open(shared_datadir / file_name) as file:
            # TOD: RAISE ERROR!!
            raise parse_without_names_spaces(file.read()).tag.split("}")[0].strip("{")
            # assert parse_without_names_spaces(file.read()).tag.split('}')[0].strip('{') ==""
            # assert None
