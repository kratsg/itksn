import itksn
import pytest


def test_parse_fail():
    with pytest.raises(TypeError):
        itksn.parse("20Uxxyynnnnnnn")


def test_parse_example1():
    parsed = itksn.parse(b"20Uxxyynnnnnnn")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == b"xx"
    assert parsed.subproject_code == b"yy"
    assert parsed.identifier == b"nnnnnnn"


def test_parse_example2():
    parsed = itksn.parse(b"20UPIyynnnnnnn")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == b"PI"
    assert parsed.subproject_code == b"yy"
    assert parsed.identifier == b"nnnnnnn"
