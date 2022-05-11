from common.parsing.generic_parsing import take_first
from pytest import mark, param

take_first_expected = "TestValue"


@mark.parametrize(
    "test_input, expected",
    [
        param([None, "TestValue"], take_first_expected, id="Array contains None"),
        param(
            ["", "TestValue"], take_first_expected, id="Array contains empty string."
        ),
        param(["TestValue"], take_first_expected, id="Array correct value"),
        param([None, ""], None, id="Array is incorrect"),
    ],
)
def test_take_first(test_input, expected):
    assert expected == take_first(test_input)
