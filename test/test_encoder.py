import pytest

from pyjson import JSONEncoder

@pytest.mark.parametrize(
        "test_input,expected", 
        [
            ({1: {"foo": "bar"}}, '{"1": {"foo": "bar"}}'), 
            ({"2": ["foo", "bar"]}, '{"2": ["foo", "bar"]}'), 
            ({3: 14}, '{"3": 14}'),
            ({4: 20.0}, '{"4": 20.0}'),
            ({5: True}, '{"5": true}'),
            ({6: False}, '{"6": false}'),
            ({7: None}, '{"7": null}'),
            ({8: (1, "2", 3.0)}, '{"8": [1, "2", 3.0]}')
        ]
)
def test_encode(test_input: dict, expected: str):
    json_enocder = JSONEncoder()
    json_str = json_enocder.encode(test_input)
    assert(json_str == expected)

def test_non_serializable():
    """ set() is not serializable by default. """
    to_serialize = {1, 2, 3}
    json_enocder = JSONEncoder()

    try: 
        json_enocder.encode(to_serialize)
        assert(False)
    except TypeError: 
        assert(True)

def test_custom_encoder():
    class Complex:
        def __init__(self, x: float, y: float):
            self.re = x
            self.im = y

    class CustomJSONEncoder(JSONEncoder):
        def encode_default(self, obj) -> str:
            if isinstance(obj, Complex):
                return f'"{obj.re} + {obj.im}i"'
            else:
                raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable') 
            
    to_serialize = {"1": Complex(1, 2)}
    json_enocder = CustomJSONEncoder()
    json_str = json_enocder.encode(to_serialize)
    assert(json_str == '{"1": "1 + 2i"}')