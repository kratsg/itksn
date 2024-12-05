from __future__ import annotations

import json
import pathlib

import pytest

import itksn

valid_sns = json.loads(
    (pathlib.Path(__file__).with_suffix("") / "valid_sns.json").read_text()
)


@pytest.mark.parametrize(
    "serial_number",
    valid_sns,
)
def test_sn(serial_number):
    itksn.parse(serial_number.encode("utf-8"))
