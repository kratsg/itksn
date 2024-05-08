from __future__ import annotations

import pytest
from construct import Bytes
from construct.core import TerminatedError

import itksn
from itksn.core import EnumStr


def test_enumstr():
    myenum = EnumStr(Bytes(2), itsaa=b"aa", itsbb=b"bb", itsyy=b"yy")
    assert myenum.parse(b"yy").bytevalue == b"yy"
    assert myenum.parse(b"yy") == "itsyy"
    assert myenum.parse(b"xx").bytevalue == b"xx"
    assert not myenum.parse(b"xx")


def test_parse_example1():
    parsed = itksn.parse(b"20Uxxyynnnnnnn")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert not parsed.project_code
    assert parsed.subproject_code == "yy"
    assert parsed.identifier == b"nnnnnnn"


def test_parse_example2():
    parsed = itksn.parse(b"20UPIyynnnnnnn")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "inner_pixel"
    assert not parsed.subproject_code
    assert parsed.identifier == b"nnnnnnn"


def test_parse_fe_wafer():
    parsed = itksn.parse(b"20UPGFW2123456")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel_general"
    assert parsed.subproject_code == "FE_chip_wafer"
    assert parsed.identifier.batch_number == "ITkpix_v2"
    assert parsed.identifier.number == b"123456"


def test_parse_sensor():
    parsed = itksn.parse(b"20UPGW34212345")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel_general"
    assert parsed.subproject_code == "Outer_pixel_sensor_wafer_thickness_150mum"
    assert parsed.identifier.manufacturer == "V5"
    assert parsed.identifier.sensor_type == "Double"
    assert parsed.identifier.number == b"12345"


def test_parse_bare_module():
    parsed = itksn.parse(b"20UPGBS1112345")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel_general"
    assert parsed.subproject_code == "Digital_single_bare_module"
    assert parsed.identifier.FE_chip_version == "ITkpix_v1"
    assert parsed.identifier.sensor_type == "Market_survey_sensor_tile"
    assert parsed.identifier.number == b"12345"


def test_parse_pcb():
    parsed = itksn.parse(b"20UPGPD0012345")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel_general"
    assert parsed.subproject_code == "Dual_PCB"
    assert parsed.identifier.FE_chip_version == "RD53A"
    assert parsed.identifier.reserved == b"0"
    assert parsed.identifier.number == b"12345"


def test_parse_module():
    parsed = itksn.parse(b"20UPGR40012345")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel_general"
    assert parsed.subproject_code == "Digital_quad_module"
    assert parsed.identifier.FE_chip_version == "RD53A"
    assert parsed.identifier.reserved == b"0"
    assert parsed.identifier.number == b"12345"


def test_parse_module_carrier():
    parsed = itksn.parse(b"20UPGMC2291234")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel_general"
    assert parsed.subproject_code == "Module_carrier"
    assert parsed.identifier.module_type == "Linear_triplet_module_carrier"
    assert parsed.identifier.module_version == "Quad_v2p1"
    assert parsed.identifier.manufacturer == b"9"
    assert parsed.identifier.number == b"1234"


def test_parse_toomany():
    with pytest.raises(TerminatedError):
        itksn.parse(b"20Uxxyynnnnnnnmmmm")
