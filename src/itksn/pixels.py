from __future__ import annotations

from construct import (
    Bytes,
    Error,
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

triplet_assembly_site = EnumStr(
    Bytes(1),
    Genova=b"0",
    Barcelona=b"1",
    Oslo=b"2",
    Milano=b"3",
    LBNL=b"4",
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
    / EnumStr(
        Bytes(1),
        V1_ADVACAM=b"0",
        V2_HLL=b"1",
        V3_FBK_planar=b"2",
        V4_HPK=b"3",
        V5_LFoundry=b"4",
        V6_MICRON=b"5",
        V7_CNM=b"6",
        V8_FBK_3D=b"7",
        V9_SINTEF=b"8",
        Dummy=b"9",
    ),
    "sensor_type"
    / EnumStr(
        Bytes(1),
        RD53A_test_structure=b"0",
        Single=b"1",
        Halfmoon_preproduction_Double_MS=b"2",
        Quad=b"3",
        Planar_diode_test_structure_1=b"4",
        Strip_test_structure_2=b"5",
        Mini_sensor_test_structure_3=b"6",
        Interpixel_capacitance_test_structure_4=b"7",
        Biasing_test_structure_5=b"8",
        ThreeD_diode_test_structure_6=b"9",
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

module = Struct(
    "FE_chip_version" / fe_chip_version,
    "PCB_manufacturer" / pcb_manufacturer,
    "number" / Bytes(5),
)
triplet_module = Struct(
    "FE_chip_version" / fe_chip_version,
    "assembly_site" / triplet_assembly_site,
    "not_used" / Bytes(1),
    "number" / Bytes(4),
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

yy_identifiers = {
    "FE_chip_wafer": ("FW", "PG"),
    "FE_chip": ("FC", "PG"),
    "Planar_sensor_wafer_100um_thickness": ("W6", "PI", "PG"),
    "Planar_sensor_wafer_150um_thickness": ("W7", "PG"),
    "ThreeD_sensor_wafer": ("W8", "PI", "PG"),
    "L0_inner_pixel_3D_sensor_wafer_25x100um": ("W0", "PI"),
    "L0_inner_pixel_3D_sensor_wafer_50x50um": ("W1", "PI"),
    "L1_inner_pixel_sensor_wafer_100um_thickness": ("W2", "PI"),
    "Outer_pixel_sensor_wafer_150um_thickness": ("W3", "PG"),
    "Half_size_planar_sensor_tile_100um_thickness": ("S6", "PG"),
    "Half_size_planar_sensor_tile_150um_thickness": ("S7", "PG"),
    "Full_size_planar_sensor_tile_100um_thickness": ("S8", "PI"),
    "Full_size_planar_sensor_tile_150um_thickness": ("S9", "PG"),
    "Half_size_3D_sensor_tile_25x100um": ("SG", "PG"),
    "Full_size_3D_sensor_tile_25x100um": ("SH", "PG"),
    "Half_size_3D_sensor_tile_50x50um": ("SI", "PG"),
    "Full_size_3D_sensor_tile_50x50um": ("SJ", "PG"),
    "L0_inner_pixel_3D_sensor_tile_25x100um": ("S0", "PI"),
    "L0_inner_pixel_3D_sensor_tile_50x50um": ("S1", "PI"),
    "L1_inner_pixel_quad_sensor_tile": ("S2", "PI"),
    "Outer_pixel_quad_sensor_tile": ("S3", "PG"),
    "Planar_Sensor_test_structure_100um_thickness": ("ST", "PI"),
    "Planar_Sensor_test_structure_150um_thickness": ("SU", "PG"),
    "ThreeD_Sensor_test_structure_25x100um": ("SV", "PI", "PG"),
    "ThreeD_Sensor_test_structure_50x50um": ("SW", "PI", "PG"),
    "Planar_Sensor_half_moon_100um_thickness": ("HT", "PI"),
    "Planar_Sensor_half_moon_150um_thickness": ("HU", "PG"),
    "ThreeD_Sensor_half_moon_25x100um": ("HV", "PI", "PG"),
    "ThreeD_Sensor_half_moon_50x50um": ("HW", "PI", "PG"),
    "Single_bare_module": ("B1", "PG"),
    "Dual_bare_module": ("B2", "PG"),
    "Quad_bare_module": ("B4", "PG"),
    "Digital_single_bare_module": ("BS", "PG"),
    "Digital_quad_bare_module": ("BQ", "PG"),
    "Dummy_quad_bare_module": ("BR", "PG"),
    "Dummy_single_bare_module": ("BT", "PG"),
    "FourInch_bare_module_gel_pack": ("G4", "PG"),
    "SixInch_bare_module_gel_pack": ("G6", "PG"),
    "Triplet_L0_Stave_PC": ("PT", "PI"),
    "Triplet_L0_R0_PC": ("P0", "PI"),
    "Triplet_L0_R0p5_PC": ("P5", "PI"),
    "Quad_PCB": ("PQ", "PG"),
    "Dual_PCB": ("PD", "PG"),
    "PCB_test_coupon": ("PC", "PG"),
    "OB_wirebond_protection_roof": ("WP", "P"),
    "Triplet_L0_stave_module": ("MS", "PI"),
    "Triplet_L0_Ring0_module": ("M0", "PI"),
    "Triplet_L0_Ring0p5_module": ("M5", "PI"),
    "L1_quad_module": ("M1", "PI"),
    "Outer_system_quad_module": ("M2", "PG"),
    "Dual_chip_module": ("R2", "PG"),
    "Single_chip_module": ("R0", "PG"),
    "Digital_triplet_L0_stave_module": ("R6", "PI"),
    "Digital_triplet_L0_ring0_module": ("R7", "PI"),
    "Digital_triplet_L0_ring0p5_module": ("R8", "PI"),
    "Digital_quad_module": ("R9", "PG"),
    "Digital_L1_quad_module": ("R", "PI"),
    "Dummy_triplet_L0_stave_module": ("RT", "PI"),
    "Dummy_triplet_L0_ring0_module": ("RU", "PI"),
    "Dummy_triplet_L0_ring0p5_module": ("RV", "PI"),
    "Dummy_quad_module": ("RQ", "PG"),
    "Dummy_L1_quad_module": ("RR", "PG"),
    "Module_carrier": ("MC", "PG"),
}

subproject_codes = {
    subproject_code: EnumStr(
        Bytes(2),
        **{
            k: v.encode("utf-8")
            for k, (v, *allowed_subprojects) in yy_identifiers.items()
            if subproject_code in allowed_subprojects
        },
    )
    for subproject_code in ["PI", "PG", "PB"]
}

identifiers = Switch(
    lambda ctx: ctx.subproject_code,
    {
        "FE_chip_wafer": fe_chip_wafer,
        "FE_chip": Error,
        "Planar_sensor_wafer_100um_thickness": sensor,
        "Planar_sensor_wafer_150um_thickness": sensor,
        "ThreeD_sensor_wafer": sensor,
        "L0_inner_pixel_3D_sensor_wafer_25x100um": sensor,
        "L0_inner_pixel_3D_sensor_wafer_50x50um": sensor,
        "L1_inner_pixel_sensor_wafer_100um_thickness": sensor,
        "Outer_pixel_sensor_wafer_150um_thickness": sensor,
        "Half_size_planar_sensor_tile_100um_thickness": sensor,
        "Half_size_planar_sensor_tile_150um_thickness": sensor,
        "Full_size_planar_sensor_tile_100um_thickness": sensor,
        "Full_size_planar_sensor_tile_150um_thickness": sensor,
        "Half_size_3D_sensor_tile_25x100um": sensor,
        "Full_size_3D_sensor_tile_25x100um": sensor,
        "Half_size_3D_sensor_tile_50x50um": sensor,
        "Full_size_3D_sensor_tile_50x50um": sensor,
        "L0_inner_pixel_3D_sensor_tile_25x100um": sensor,
        "L0_inner_pixel_3D_sensor_tile_50x50um": sensor,
        "L1_inner_pixel_quad_sensor_tile": sensor,
        "Outer_pixel_quad_sensor_tile": sensor,
        "Planar_Sensor_test_structure_100um_thickness": sensor,
        "Planar_Sensor_test_structure_150um_thickness": sensor,
        "ThreeD_Sensor_test_structure_25x100um": sensor,
        "ThreeD_Sensor_test_structure_50x50um": sensor,
        "Planar_Sensor_half_moon_100um_thickness": sensor,
        "Planar_Sensor_half_moon_150um_thickness": sensor,
        "ThreeD_Sensor_half_moon_25x100um": sensor,
        "ThreeD_Sensor_half_moon_50x50um": sensor,
        "Single_bare_module": bare_module,
        "Dual_bare_module": bare_module,
        "Quad_bare_module": bare_module,
        "Digital_single_bare_module": bare_module,
        "Digital_quad_bare_module": bare_module,
        "Dummy_quad_bare_module": bare_module,
        "Dummy_single_bare_module": bare_module,
        "FourInch_bare_module_gel_pack": Error,
        "SixInch_bare_module_gel_pack": Error,
        "Triplet_L0_Stave_PCB": pcb,
        "Triplet_L0_R0_PCB": pcb,
        "Triplet_L0_R0p5_PCB": pcb,
        "Quad_PCB": pcb,
        "Dual_PCB": pcb,
        "PCB_test_coupon": pcb,
        "OB_wirebond_protection_roof": Error,
        "Triplet_L0_stave_module": triplet_module,
        "Triplet_L0_Ring0_module": triplet_module,
        "Triplet_L0_Ring0p5_module": triplet_module,
        "L1_quad_module": module,
        "Outer_system_quad_module": module,
        "Dual_chip_module": module,
        "Single_chip_module": module,
        "Digital_triplet_L0_stave_module": triplet_module,
        "Digital_triplet_L0_ring0_module": triplet_module,
        "Digital_triplet_L0_ring0p5_module": triplet_module,
        "Digital_quad_module": module,
        "Digital_L1_quad_module": module,
        "Dummy_triplet_L0_stave_module": triplet_module,
        "Dummy_triplet_L0_ring0_module": triplet_module,
        "Dummy_triplet_L0_ring0p5_module": triplet_module,
        "Dummy_quad_module": module,
        "Dummy_L1_quad_module": module,
        "Module_carrier": module_carrier,
    },
    default=Bytes(7),
)
