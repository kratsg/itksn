from __future__ import annotations

from itksn import core
from itksn._version import __version__

parse = core.SerialNumberStruct.parse
build = core.SerialNumberStruct.build

__all__ = ["__version__", "build", "parse"]
del core
