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
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "pixel_general"
    assert parsed.component_code == "FE_chip_wafer"
    assert parsed.identifier.batch == "RD53A"
    assert parsed.identifier.number == b"2123456"


def test_parse_fe_wafer_wrong_subproject():
    with pytest.raises(MappingError):
        itksn.parse(b"20UPIFW2123456")


def test_parse_sensor():
    parsed = itksn.parse(b"20UPGW34212345")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "pixel_general"
    assert parsed.component_code == "Outer_pixel_sensor_wafer_150um_thickness"
    assert parsed.identifier.manufacturer == "V5_LFoundry"
    assert parsed.identifier.sensor_type == "Halfmoon_preproduction_Double_MS"
    assert parsed.identifier.number == b"12345"


def test_parse_bare_module():
    parsed = itksn.parse(b"20UPGBS1112345")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "pixel_general"
    assert parsed.component_code == "Digital_single_bare_module"
    assert parsed.identifier.FE_chip_version == "ITkpix_v1"
    assert parsed.identifier.sensor_type == "Market_survey_sensor_tile"
    assert parsed.identifier.number == b"12345"


def test_parse_pcb():
    parsed = itksn.parse(b"20UPGPD0112345")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "pixel_general"
    assert parsed.component_code == "Dual_PCB"
    assert parsed.identifier.FE_chip_version == "RD53A"
    assert parsed.identifier.PCB_manufacturer == "EPEC"
    assert parsed.identifier.number == b"12345"


def test_parse_module():
    parsed = itksn.parse(b"20UPGR90112345")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "pixel_general"
    assert parsed.component_code == "Digital_quad_module"
    assert parsed.identifier.FE_chip_version == "RD53A"
    assert parsed.identifier.PCB_manufacturer == "EPEC"
    assert parsed.identifier.number == b"12345"


def test_parse_quad_module():
    parsed = itksn.parse(b"20UPIM12602173")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "inner_pixel"
    assert parsed.component_code == "L1_quad_module"
    assert parsed.identifier.FE_chip_version == "ITkpix_v1p1"
    assert parsed.identifier.PCB_manufacturer is None
    assert parsed.identifier.number == b"602173"


def test_parse_quad_module_rd53a():
    parsed = itksn.parse(b"20UPIM10602173")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "inner_pixel"
    assert parsed.component_code == "L1_quad_module"
    assert parsed.identifier.FE_chip_version == "RD53A"
    assert parsed.identifier.PCB_manufacturer == "Yamashita_Material"
    assert parsed.identifier.number == b"02173"


def test_parse_module_carrier():
    parsed = itksn.parse(b"20UPGMC2291234")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "pixel_general"
    assert parsed.component_code == "Module_carrier"
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
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "pixel_general"
    assert parsed.component_code == "Digital_quad_module"
    assert parsed.identifier.FE_chip_version == "ITkpix_v1p1"
    assert parsed.identifier.PCB_manufacturer is None
    assert parsed.identifier.number == b"101041"


def test_parse_digital_quad_module_rd53a():
    parsed = itksn.parse(b"20UPGR90101041")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "pixel_general"
    assert parsed.component_code == "Digital_quad_module"
    assert parsed.identifier.FE_chip_version == "RD53A"
    assert parsed.identifier.PCB_manufacturer == "EPEC"
    assert parsed.identifier.number == b"01041"


@pytest.mark.parametrize(
    ("serial_number", "component_code", "assembly_site", "number"),
    [
        ("20UPIMS2002140", "Triplet_L0_stave_module", "Genova", b"2140"),
        ("20UPIM52002140", "Triplet_L0_Ring0p5_module", "Genova", b"2140"),
        ("20UPIM02202123", "Triplet_L0_Ring0_module", "Oslo", b"2123"),
        ("20UPIMS2102148", "Triplet_L0_stave_module", "Barcelona", b"2148"),
    ],
    ids=["normal", "R05", "R0", "L0"],
)
def test_triplet_modules(serial_number, component_code, assembly_site, number):
    parsed = itksn.parse(serial_number.encode())
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "inner_pixel"
    assert parsed.component_code == component_code
    assert parsed.identifier.assembly_site == assembly_site
    assert parsed.identifier.not_used == b"0"
    assert parsed.identifier.number == number


def test_fe_chip():
    parsed = itksn.parse(b"20UPGFC1048575")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "pixel_general"
    assert parsed.component_code == "FE_chip"
    assert parsed.identifier.batch == "ITkpix_v2"
    assert parsed.identifier.wafer == 255
    assert parsed.identifier.row == 15
    assert parsed.identifier.column == 15


def test_is_capillary():
    parsed = itksn.parse(b"20UPICP1299999")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "inner_pixel"
    assert parsed.component_code == "IS_capillary"
    assert parsed.identifier.production_type == "Production"
    assert parsed.identifier.type == "R01"
    assert parsed.identifier.number == b"99999"


def test_outer_endcap_data_pp0():
    parsed = itksn.parse(b"20UPEDP2209999")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "pixel_endcaps"
    assert parsed.component_code == "Data_PP0"
    assert parsed.identifier.layer == "L2"
    assert parsed.identifier.flavor == "ring611_Front"
    assert parsed.identifier.number == b"9999"


def test_inner_system_pp1():
    parsed = itksn.parse(b"20UPI1P1000002")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "inner_pixel"
    assert parsed.component_code == "PP1_connector"
    assert parsed.identifier.production_version == "Pre_production"
    assert parsed.identifier.glenair_part == "Type_2_Header"
    assert parsed.identifier.number == b"0002"


def test_inner_system_type1_power_L02xL1():
    parsed = itksn.parse(b"20UPIP19100001")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "inner_pixel"
    assert parsed.component_code == "Type_1_Power_DCS_line"
    assert parsed.identifier.production_version == "Dummy"
    assert parsed.identifier.flavor == "L02xL1"
    assert parsed.identifier.number == b"00001"


def test_inner_system_type1_power_CR():
    parsed = itksn.parse(b"20UPIP10200001")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "inner_pixel"
    assert parsed.component_code == "Type_1_Power_DCS_line"
    assert parsed.identifier.production_version == "Prototype"
    assert parsed.identifier.flavor == "Coupled_Ring"
    assert parsed.identifier.number == b"00001"


def test_inner_system_type0_barrel_triplet_data_flex():
    parsed = itksn.parse(b"20UPIDP9000015")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "inner_pixel"
    assert parsed.component_code == "Data_PP0"
    assert parsed.identifier.production_version == "Dummy"
    assert parsed.identifier.flavor == "Barrel_Triplet"
    assert parsed.identifier.subflavor == "NA"
    assert parsed.identifier.number == b"0015"
    assert parsed.identifier.component == "L0 Barrel Data Flex"


def test_inner_system_type0_quad_module_z_ray_flex():
    parsed = itksn.parse(b"20UPIPG9300001")
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "inner_pixel"
    assert parsed.component_code == "Pigtail"
    assert parsed.identifier.production_version == "Dummy"
    assert parsed.identifier.flavor == "Ring_Quad"
    assert parsed.identifier.subflavor == "NA"
    assert parsed.identifier.number == b"0001"
    assert parsed.identifier.component == "Quad Module Z-Ray Flex"
