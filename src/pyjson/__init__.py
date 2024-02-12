from .encoder import JSONEncoder
from .decoder import JSONDecoder, JSONDecoderError
from typing import TextIO, Optional
from pathlib import Path

__all__ = [
    "load",
    "loads",
    "dump", 
    "dumps", 
    "JSONEncoder", 
    "JSONDecoder", 
    "JSONDecoderError"
]

_default_decoder = JSONDecoder()
_default_encoder = JSONEncoder()

def load(f: TextIO, decoder: Optional[JSONDecoder] = None):
    decoder = decoder or _default_decoder
    return decoder.decode(f.read())

def loads(file_path: str|Path, decoder: Optional[JSONDecoder] = None):
    with Path(file_path).open("r") as f:
        return load(f, decoder=decoder)

def dump(d: dict[str, object], f: TextIO, encoder: Optional[JSONEncoder] = None):
    encoder = encoder or _default_encoder
    f.write(encoder.encode(d))

def dumps(d: dict[str, object], encoder: Optional[JSONEncoder] = None) -> str:
    encoder = encoder or _default_encoder
    return encoder.encode(d)