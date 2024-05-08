from __future__ import annotations

from construct import (
    Bytes,
    Const,
    Struct,
    Switch,
)

from itksn.common import EnumStr

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
    "reserved" / Const(b"0"),
    "number" / Bytes(5),
)

module = Struct(
    "FE_chip_version" / fe_chip_version,
    "reserved" / Const(b"0"),
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
    FE_chip_wafer=b"FW",
    FE_chip=b"FC",
    Market_Survey_sensor_wafer=b"WM",
    L0_inner_pixel_3D_sensor_wafer=b"W0",
    L0_inner_pixel_planar_sensor_wafer=b"W1",
    L1_inner_pixel_sensor_wafer_thickness_100mum=b"W2",
    Outer_pixel_sensor_wafer_thickness_150mum=b"W3",
    Dummy_sensor_wafer=b"WD",
    Market_survey_sensor_tile=b"SM",
    L0_inner_pixel_3D_sensor_tile=b"S0",
    L0_inner_pixel_planar_sensor_tile=b"S1",
    L1_inner_pixel_quad_sensor_tile=b"S2",
    Outer_pixel_quad_sensor_tile=b"S3",
    Single_bare_module=b"B1",
    Dual_bare_module=b"B2",
    Quad_bare_module=b"B4",
    Digital_single_bare_module=b"BS",
    Digital_quad_bare_module=b"BQ",
    Dummy_single_bare_module=b"BT",
    Dummy_quad_bare_module=b"BR",
    Triplet_L0_Stave_PCB=b"PT",
    Triplet_L0_R0_PCB=b"P0",
    Triplet_L0_R0p5_PCB=b"P5",
    Quad_PCB=b"PQ",
    Dual_PCB=b"PD",
    PCB_test_coupon=b"PC",
    Triplet_L0_stave_module=b"MS",
    Triplet_L0_Ring0_module=b"M0",
    Triplet_L0_Ring0p5_module=b"M5",
    L1_quad_module=b"M1",
    Outer_system_quad_module=b"M2",
    Dual_chip_module=b"R2",
    Digital_triplet_module=b"R3",
    Digital_quad_module=b"R4",
    Dummy_triplet_module=b"R0",
    Dummy_quad_module=b"R1",
    Module_carrier=b"MC",
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
        "Triplet_L0_stave_module": module,
        "Triplet_L0_Ring0_module": module,
        "Triplet_L0_Ring0p5_module": module,
        "L1_quad_module": module,
        "Outer_system_quad_module": module,
        "Dual_chip_module": module,
        "Digital_triplet_module": module,
        "Digital_quad_module": module,
        "Dummy_triplet_module": module,
        "Dummy_quad_module": module,
        "Module_carrier": module_carrier,
    },
    default=Bytes(7),
)
