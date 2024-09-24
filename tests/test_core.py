from __future__ import annotations

import pytest
from construct import Bytes
from construct.core import MappingError, TerminatedError

import itksn
from itksn.core import EnumStr


def test_enumstr():
    myenum = EnumStr(Bytes(2), itsaa=b"aa", itsbb=b"bb", itsyy=b"yy")
    assert myenum.parse(b"yy").bytevalue == b"yy"
    assert myenum.parse(b"yy") == "itsyy"
    with pytest.raises(MappingError):
        myenum.parse(b"xx")


def test_parse_fe_wafer():
    parsed = itksn.parse(b"20UPGFW2123456")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel_general"
    assert parsed.subproject_code == "FE_chip_wafer"
    assert parsed.identifier.batch_number == "ITkpix_v2"
    assert parsed.identifier.number == b"123456"


def test_parse_fe_wafer_wrong_subproject():
    with pytest.raises(MappingError):
        itksn.parse(b"20UPIFW2123456")


def test_parse_sensor():
    parsed = itksn.parse(b"20UPGW34212345")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel_general"
    assert parsed.subproject_code == "Outer_pixel_sensor_wafer_150um_thickness"
    assert parsed.identifier.manufacturer == "V5_LFoundry"
    assert parsed.identifier.sensor_type == "Halfmoon_preproduction_Double_MS"
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
    parsed = itksn.parse(b"20UPGPD0112345")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel_general"
    assert parsed.subproject_code == "Dual_PCB"
    assert parsed.identifier.FE_chip_version == "RD53A"
    assert parsed.identifier.PCB_manufacturer == "EPEC"
    assert parsed.identifier.number == b"12345"


def test_parse_module():
    parsed = itksn.parse(b"20UPGR90112345")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel_general"
    assert parsed.subproject_code == "Digital_quad_module"
    assert parsed.identifier.FE_chip_version == "RD53A"
    assert parsed.identifier.PCB_manufacturer == "EPEC"
    assert parsed.identifier.number == b"12345"


def test_parse_quad_module():
    parsed = itksn.parse(b"20UPIM12602173")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "inner_pixel"
    assert parsed.subproject_code == "L1_quad_module"
    assert parsed.identifier.FE_chip_version == "ITkpix_v1p1"
    assert parsed.identifier.PCB_manufacturer == "Yamashita_Material"
    assert parsed.identifier.number == b"02173"


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
        itksn.parse(b"20UPGMC2291234999")


def test_parse_digital_quad_module():
    parsed = itksn.parse(b"20UPGR92101041")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel_general"
    assert parsed.subproject_code == "Digital_quad_module"
    assert parsed.identifier.FE_chip_version == "ITkpix_v1p1"
    assert parsed.identifier.PCB_manufacturer == "EPEC"
    assert parsed.identifier.number == b"01041"


@pytest.mark.parametrize(
    ("serial_number", "subproject_code", "assembly_site", "number"),
    [
        ("20UPIMS2002140", "Triplet_L0_stave_module", "Genova", b"2140"),
        ("20UPIM52002140", "Triplet_L0_Ring0p5_module", "Genova", b"2140"),
        ("20UPIM02202123", "Triplet_L0_Ring0_module", "Oslo", b"2123"),
        ("20UPIMS2102148", "Triplet_L0_stave_module", "Barcelona", b"2148"),
    ],
    ids=["normal", "R05", "R0", "L0"],
)
def test_triplet_modules(serial_number, subproject_code, assembly_site, number):
    parsed = itksn.parse(serial_number.encode())
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "inner_pixel"
    assert parsed.subproject_code == subproject_code
    assert parsed.identifier.assembly_site == assembly_site
    assert parsed.identifier.not_used == b"0"
    assert parsed.identifier.number == number
