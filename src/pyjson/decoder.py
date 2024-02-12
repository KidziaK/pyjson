from typing import Tuple

class JSONDecoderError(Exception):
    """ """
    def __init__(self, json_str: str, pos: int):
        line: int = json_str.count('\n', 0, pos) + 1
        column: int = pos - json_str.rfind('\n', 0, pos)
        msg = f"failed to decode json: on line {line} and column {column}"
        super().__init__(self, msg)


class JSONDecoder:
    """
    Default JSON decoder for Python objects.

    Supports the following translations by default:

    +---------------+-------------------+
    | JSON          | Python            |
    +===============+===================+
    | object        | dict              |
    +---------------+-------------------+
    | array         | list              |
    +---------------+-------------------+
    | string        | str               |
    +---------------+-------------------+
    | number (int)  | int               |
    +---------------+-------------------+
    | number (real) | float             |
    +---------------+-------------------+
    | true          | True              |
    +---------------+-------------------+
    | false         | False             |
    +---------------+-------------------+
    | null          | None              |
    +---------------+-------------------+
    """

    def decode(self, json_str: str) -> object:
        ret, _ = self.inner_decode(json_str, 0)
        return ret

    def inner_decode(self, json_str: str, pos) -> Tuple[object, int]:
        i = pos

        while i < len(json_str):
            c = json_str[i]
            if c == " ":
                i += 1
                continue

            if c == "{":
                ret, inc = self.decode_object(json_str, i)
            elif c == "[":
                ret, inc = self.decode_array(json_str, i)
            else:
                ret, inc = self.decode_value(json_str, i)
            return ret, i + inc
        
        raise JSONDecoderError(json_str, i)
        
    def decode_value(self, json_str: str, pos: int):
        i = pos
        c = json_str[i]

        if c == "n":
            return self.decode_null(), i + 4
        if c == "t":
            return self.decode_true(), i + 4
        if c == "f":
            return self.decode_false(), i + 5
        if c.isnumeric():
            return self.decode_number(json_str, i)
        if c == '"':
            return self.decode_string(json_str, i)
        
        raise JSONDecoderError(json_str, i)          

    def decode_object(self, json_str: str, pos: int):
        ret = dict()
        i = pos + 1

        while i < len(json_str):
            c = json_str[i]
            
            if c == " " or c == ",":
                i += 1
                continue
            if c == "}":
                i += 1
                break
            if c == '"':
                key, i = self.decode_value(json_str, i)
                c = json_str[i]
                while c != ":" or c == " ": i += 1
                val, i = self.inner_decode(json_str, i + 1)
                ret[key] = val

        return ret, i
        
    def decode_array(self, json_str: str, pos: int):
        ret = []
        i = pos + 1

        while i < len(json_str):
            c = json_str[i]
            
            if c == " " or c == ",":
                i += 1
                continue
            if c == "]":
                i += 1
                break

            val, i = self.inner_decode(json_str, i)
            ret.append(val)

        return ret, i

    def decode_string(self, json_str: str, pos: int):
        i = pos + 1

        while i < len(json_str):
            c = json_str[i]
            if c == '"':
                return json_str[pos + 1: i], i + 1
            i += 1

        raise JSONDecoderError(json_str, i)  

    def decode_number(self, json_str: str, pos: int):
        inc = 0
        while json_str[pos + inc].isnumeric() or json_str[pos + inc] == ".":
            inc += 1

        val = json_str[pos: pos + inc]

        if "." in val:
            return self.decode_float(val), inc
        else:
            return self.decode_int(val), inc

    def decode_int(self, val: str):
        return int(val)

    def decode_float(self, val: str):
        return float(val)

    def decode_true(self):
        return True

    def decode_false(self):
        return False

    def decode_null(self):
        return None
        
