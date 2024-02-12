class JSONEncoder:
    """
    Default JSON encoder for Python objects.

    Supports the following objects and types by default:

    +-------------------+---------------+
    | Python            | JSON          |
    +===================+===============+
    | dict              | object        |
    +-------------------+---------------+
    | list, tuple       | array         |
    +-------------------+---------------+
    | str               | string        |
    +-------------------+---------------+
    | int, float        | number        |
    +-------------------+---------------+
    | True              | true          |
    +-------------------+---------------+
    | False             | false         |
    +-------------------+---------------+
    | None              | null          |
    +-------------------+---------------+

    To change add encoding for custom types,
    create a subclass and overload the encode_default() method.

    Example:

    class Complex:
        def __init__(self, x: float, y: float):
            self.re = x
            self.im = y

    class CustomJSONEncoder(JSONEncoder):
        def encode_default(self, obj) -> str:
            if isinstance(obj, Complex):
                return f'"{self.re} + {self.im}i"'
            else:
                raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')
    """

    def encode(self, obj) -> str:
        if isinstance(obj, dict):
            return self.encode_dict(obj)
        elif isinstance(obj, list):
            return self.encode_list(obj)
        elif isinstance(obj, tuple):
            return self.encode_tuple(obj)
        elif isinstance(obj, str):
            return self.encode_str(obj)
        elif isinstance(obj, bool):
            return self.encode_bool(obj)
        elif isinstance(obj, int):
            return self.encode_int(obj)
        elif isinstance(obj, float):
            return self.encode_float(obj)
        elif obj is None:
            return self.encode_none()
        else:
            return self.encode_default(obj)
        
    def __encode_list_tuple(self, obj: list|tuple) -> str:
        return "[" + ", ".join([self.encode(v) for v in obj]) + "]"

    def encode_dict(self, obj: dict) -> str:
        str_dict = ", ".join([f'"{k}": {self.encode(v)}' for k, v in obj.items()])
        return "{" + str_dict + "}"
    
    def encode_list(self, obj: list) -> str:
        return self.__encode_list_tuple(obj)
    
    def encode_tuple(self, obj: tuple) -> str:
        return self.__encode_list_tuple(obj)
    
    def encode_str(self, obj: str) -> str:
        return f'"{obj}"'
    
    def encode_bool(self, obj: bool) -> str:
        return str(obj).lower()
    
    def encode_int(self, obj: int) -> str:
        return str(obj)
    
    def encode_float(self, obj: float) -> str:
        return str(obj)
    
    def encode_none(self) -> str:
        return "null"
        
    def encode_default(self, obj) -> str:
        raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')