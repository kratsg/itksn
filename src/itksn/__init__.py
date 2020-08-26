from .version import __version__
from .core import SerialNumberStruct

parse = SerialNumberStruct.parse

__all__ = ["__version__", "parse"]
del SerialNumberStruct
