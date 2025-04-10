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
    assert parsed.identifier.Vendor_or_Thickness == "Leonardo"
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


@pytest.mark.parametrize(
    ("serial_number", "region", "component_code", "component"),
    [
        ("20UPIPG0000000", "Barrel_Triplet", "Pigtail", "L0 Barrel Data Flex"),
        ("20UPIPP0000000", "Barrel_Triplet", "Power_pigtail", "L0 Barrel Power Flex"),
        ("20UPIPG0110000", "Barrel_Quad", "Pigtail", "L1 Barrel Data Flex F1"),
        ("20UPIPG0120000", "Barrel_Quad", "Pigtail", "L1 Barrel Data Flex F2"),
        ("20UPIPG0130000", "Barrel_Quad", "Pigtail", "L1 Barrel Data Flex F3"),
        ("20UPIPG0140000", "Barrel_Quad", "Pigtail", "L1 Barrel Data Flex F4"),
        ("20UPIPP0110000", "Barrel_Quad", "Power_pigtail", "L1 Barrel Power Flex F1"),
        ("20UPIPP0120000", "Barrel_Quad", "Power_pigtail", "L1 Barrel Power Flex F2"),
        ("20UPIRF0500000", "Endcap_Mixed", "Rigid_flex", "Coupled Ring"),
        ("20UPIRF0400000", "Endcap_Quad", "Rigid_flex", "Quad Ring"),
        ("20UPIRF0300000", "Endcap_Ring05_Triplet", "Rigid_flex", "Intermediate Ring"),
        ("20UPIPG0400000", "Endcap_Quad", "Pigtail", "Quad Module Z-Ray"),
        ("20UPIPG0210000", "Endcap_Ring0_Triplet", "Pigtail", "R0 Data Flex F1"),
        ("20UPIPG0220000", "Endcap_Ring0_Triplet", "Pigtail", "R0 Data Flex F2"),
        ("20UPIPG0230000", "Endcap_Ring0_Triplet", "Pigtail", "R0 Data Flex F3"),
        ("20UPIPP0510000", "Endcap_Mixed", "Power_pigtail", "Triplet Power T-Rex"),
        ("20UPIPP0520000", "Endcap_Mixed", "Power_pigtail", "Triplet Power Jumper"),
        ("20UPIPG0310000", "Endcap_Ring05_Triplet", "Pigtail", "R0.5 Data Flex F1"),
        ("20UPIPG0320000", "Endcap_Ring05_Triplet", "Pigtail", "R0.5 Data Flex F2"),
        ("20UPIPG0510000", "Endcap_Mixed", "Pigtail", "Type-0 to PP0 F1"),
        ("20UPIPG0520000", "Endcap_Mixed", "Pigtail", "Type-0 to PP0 F2"),
    ],
)
def test_inner_system_type0_services(serial_number, region, component_code, component):
    parsed = itksn.parse(serial_number.encode("utf-8"))
    assert parsed.atlas_project == "atlas_detector"
    assert parsed.system_code == "phaseII_upgrade"
    assert parsed.project_code == "pixel"
    assert parsed.subproject_code == "inner_pixel"
    assert parsed.component_code == component_code
    assert parsed.identifier.region == region
    assert parsed.identifier.number == b"0000"
    assert parsed.identifier.component == component
