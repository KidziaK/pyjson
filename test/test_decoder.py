import pytest

from pyjson import JSONDecoder


def test_decode():
    json_str = "null"
    decoder = JSONDecoder()
    decoded = decoder.decode(json_str)

    assert(decoded is None)

@pytest.mark.parametrize(
        "test_input,expected", 
        [
            ("null", None), 
            ("false", False), 
            ("true", True),
            ("[1, 2, 3]", [1, 2, 3]),
            ('"foo"', "foo"),
            ('{"foo": 3}', {"foo": 3})
        ]
)
def test_decode_simple_types(test_input: str, expected):
    decoder = JSONDecoder()
    decoded = decoder.decode(test_input)
    assert(decoded == expected)
