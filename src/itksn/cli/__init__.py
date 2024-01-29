"""The itksn command line interface."""

from __future__ import annotations

import logging

from itksn.cli.main import app

logging.basicConfig()

__all__ = ("app",)
