from .version import __version__
from . import core

parse = core.SerialNumberStruct.parse

__all__ = ["__version__", "parse"]
del core
