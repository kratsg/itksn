from __future__ import annotations

from construct import (
    Bytes,
    Const,
    Struct,
    Switch,
)

from itksn.common import EnumStr

pcb_manufacturer = EnumStr(
    Bytes(1),
    EPEC=b"1",
    NCAB_100um=b"2",
    ATLAFLEX=b"3",
    SFCircuits=b"4",
    PHOENIX=b"5",
    Yamashita_Material=b"6",
    NCAB_75um=b"7",
    Tecnomec=b"8",
)

fe_chip_version = EnumStr(
    Bytes(1),
    RD53A=b"0",
    ITkpix_v1=b"1",
    ITkpix_v1p1=b"2",
    ITkpix_v2=b"3",
)

fe_chip_wafer = Struct(
    "batch_number"
    / EnumStr(
        Bytes(1),
        RD53A=b"0",
        ITkpix_v1=b"1",
        ITkpix_v2=b"2",
    ),
    "number" / Bytes(6),
)

sensor = Struct(
    "manufacturer"
    / EnumStr(Bytes(1), V1=b"0", V2=b"1", V3=b"2", V4=b"3", V5=b"4", V6=b"5"),
    "sensor_type"
    / EnumStr(
        Bytes(1),
        Single_RD53A=b"0",
        Single_ITkpix_v1_2=b"1",
        Double=b"2",
        Quad=b"3",
        Test_Structure_1=b"4",
        Test_Structure_2=b"5",
        Test_Structure_3=b"6",
        Test_Structure_4=b"7",
        Test_Structure_5=b"8",
        Test_Structure_6=b"9",
    ),
    "number" / Bytes(5),
)

bare_module = Struct(
    "FE_chip_version" / fe_chip_version,
    "sensor_type"
    / EnumStr(
        Bytes(1),
        No_sensor=b"0",
        Market_survey_sensor_tile=b"1",
        L0_inner_pixel_3D_sensor_tile=b"2",
        L0_inner_pixel_planar_sensor_tile=b"3",
        L1_inner_pixel_quad_sensor_tile=b"4",
        Outer_pixel_quad_sensor_tile=b"5",
    ),
    "number" / Bytes(5),
)

pcb = Struct(
    "FE_chip_version" / fe_chip_version,
    "PCB_manufacturer" / pcb_manufacturer,
    "number" / Bytes(5),
)

module_rd53a = Struct(
    "FE_chip_version" / fe_chip_version,
    "reserved" / Const(b"0"),
    "number" / Bytes(5),
)

module = Struct(
    "FE_chip_version" / fe_chip_version,
    "PCB_manufacturer" / pcb_manufacturer,
    "number" / Bytes(5),
)

module_carrier = Struct(
    "module_type"
    / EnumStr(
        Bytes(1),
        Quad_module_carrier=b"0",
        Cell_loaded_quad_module_bottom_cover=b"1",
        Linear_triplet_module_carrier=b"2",
        Ring_triplet_module_carrier=b"3",
    ),
    "module_version"
    / EnumStr(
        Bytes(1),
        Triplet_v1p0=b"1",
        Quad_v2p1=b"2",
    ),
    "manufacturer" / Bytes(1),
    "number" / Bytes(4),
)

subproject_codes = EnumStr(
    Bytes(2),
    FE_chip_wafer=b"FW",  # PG
    FE_chip=b"FC",  # PG
    Planar_sensor_wafer_100um_thickness=b"W6",  # PI, PG
    Planar_sensor_wafer_150um_thickness=b"W7",  # PG
    ThreeD_sensor_wafer=b"W8",  # PI, PG
    L0_inner_pixel_3D_sensor_wafer_25x100um=b"W0",  # PI
    L0_inner_pixel_3D_sensor_wafer_50x50um=b"W1",  # PI
    L1_inner_pixel_sensor_wafer_100um_thickness=b"W2",  # PI
    Outer_pixel_sensor_wafer_150um_thickness=b"W3",  # PG
    Half_size_planar_sensor_tile_100um_thickness=b"S6",  # PG
    Half_size_planar_sensor_tile_150um_thickness=b"S7",  # PG
    Full_size_planar_sensor_tile_100um_thickness=b"S8",  # PI
    Full_size_planar_sensor_tile_150um_thickness=b"S9",  # PG
    Half_size_3D_sensor_tile_25x100um=b"SG",  # PG
    Full_size_3D_sensor_tile_25x100um=b"SH",  # PG
    Half_size_3D_sensor_tile_50x50um=b"SI",  # PG
    Full_size_3D_sensor_tile_50x50um=b"SJ",  # PG
    L0_inner_pixel_3D_sensor_tile_25x100um=b"S0",  # PI
    L0_inner_pixel_3D_sensor_tile_50x50um=b"S1",  # PI
    L1_inner_pixel_quad_sensor_tile=b"S2",  # PI
    Outer_pixel_quad_sensor_tile=b"S3",  # PG
    Planar_Sensor_test_structure_100um_thickness=b"ST",  # PI
    Planar_Sensor_test_structure_150um_thickness=b"SU",  # PG
    ThreeD_Sensor_test_structure_25x100um=b"SV",  # PI, PG
    ThreeD_Sensor_test_structure_50x50um=b"SW",  # PI, PG
    Planar_Sensor_half_moon_100um_thickness=b"HT",  # PI
    Planar_Sensor_half_moon_150um_thickness=b"HU",  # PG
    ThreeD_Sensor_half_moon_25x100um=b"HV",  # PI, PG
    ThreeD_Sensor_half_moon_50x50um=b"HW",  # PI, PG
    Single_bare_module=b"B1",  # PG
    Dual_bare_module=b"B2",  # PG
    Quad_bare_module=b"B4",  # PG
    Digital_single_bare_module=b"BS",  # PG
    Digital_quad_bare_module=b"BQ",  # PG
    Dummy_quad_bare_module=b"BR",  # PG
    Dummy_single_bare_module=b"BT",  # PG
    FourInch_bare_module_gel_pack=b"G4",  # PG
    SixInch_bare_module_gel_pack=b"G6",  # PG
    Triplet_L0_Stave_PCB=b"PT",  # PI
    Triplet_L0_R0_PCB=b"P0",  # PI
    Triplet_L0_R05_PCB=b"P5",  # PI
    Quad_PCB=b"PQ",  # PG
    Dual_PCB=b"PD",  # PG
    PCB_test_coupon=b"PC",  # PG
    OB_wirebond_protection_roof=b"WP",  # PB
    Triplet_L0_stave_module=b"MS",  # PI
    Triplet_L0_Ring0_module=b"M0",  # PI
    Triplet_L0_Ring05_module=b"M5",  # PI
    L1_quad_module=b"M1",  # PI
    Outer_system_quad_module=b"M2",  # PG
    Dual_chip_module=b"R2",  # PG
    Single_chip_module=b"R0",  # PG
    Digital_triplet_L0_stave_module=b"R6",  # PI
    Digital_triplet_L0_ring0_module=b"R7",  # PI
    Digital_triplet_L0_ring05_module=b"R8",  # PI
    Digital_quad_module=b"R9",  # PG
    Digital_L1_quad_module=b"RB",  # PI
    Dummy_triplet_L0_stave_module=b"RT",  # PI
    Dummy_triplet_L0_ring0_module=b"RU",  # PI
    Dummy_triplet_L0_ring05_module=b"RV",  # PI
    Dummy_quad_module=b"RQ",  # PG
    Dummy_L1_quad_module=b"RR",  # PG
    Module_carrier=b"MC",  # PG
)

identifiers = Switch(
    lambda ctx: ctx.subproject_code,
    {
        "FE_chip_wafer": fe_chip_wafer,
        "Market_Survey_sensor_wafer": sensor,
        "L0_inner_pixel_3D_sensor_wafer": sensor,
        "L0_inner_pixel_planar_sensor_wafer": sensor,
        "L1_inner_pixel_sensor_wafer_thickness_100mum": sensor,
        "Outer_pixel_sensor_wafer_thickness_150mum": sensor,
        "Dummy_sensor_wafer": sensor,
        "Market_survey_sensor_tile": sensor,
        "L0_inner_pixel_3D_sensor_tile": sensor,
        "L0_inner_pixel_planar_sensor_tile": sensor,
        "L1_inner_pixel_quad_sensor_tile": sensor,
        "Outer_pixel_quad_sensor_tile": sensor,
        "Single_bare_module": bare_module,
        "Dual_bare_module": bare_module,
        "Quad_bare_module": bare_module,
        "Digital_single_bare_module": bare_module,
        "Digital_quad_bare_module": bare_module,
        "Dummy_single_bare_module": bare_module,
        "Dummy_quad_bare_module": bare_module,
        "Triplet_L0_Stave_PCB": pcb,
        "Triplet_L0_R0_PCB": pcb,
        "Triplet_L0_R0p5_PCB": pcb,
        "Quad_PCB": pcb,
        "Dual_PCB": pcb,
        "PCB_test_coupon": pcb,
        "Triplet_L0_stave_module": module_rd53a,
        "Triplet_L0_Ring0_module": module_rd53a,
        "Triplet_L0_Ring0p5_module": module_rd53a,
        "L1_quad_module": module,
        "Outer_system_quad_module": module,
        "Dual_chip_module": module_rd53a,
        "Digital_triplet_module": module_rd53a,
        "Digital_quad_module": module_rd53a,
        "Dummy_triplet_module": module_rd53a,
        "Dummy_quad_module": module_rd53a,
        "Module_carrier": module_carrier,
    },
    default=Bytes(7),
)
