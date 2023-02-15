from __future__ import annotations

from itksn import core
from itksn._version import __version__

parse = core.SerialNumberStruct.parse

__all__ = ["__version__", "parse"]
del core
