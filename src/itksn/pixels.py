from __future__ import annotations

from construct import (
    Bytes,
    Computed,
    Const,
    Error,
    Pointer,
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

batch_number = EnumStr(
    Bytes(1),
    RD53A=b"0",
    ITkpix_v1=b"1",
    ITkpix_v2=b"2",
)

fe_chip = Struct(
    "number" / Bytes(7),
    "batch_number" / Computed(lambda ctx: (int(ctx.number) & 0xF0000) >> 16),  # type: ignore[arg-type,return-value]
    "batch" / Computed(lambda ctx: batch_number.parse(str(ctx.batch_number).encode())),  # type: ignore[arg-type,return-value]
    "wafer" / Computed(lambda ctx: (int(ctx.number) & 0x0FF00) >> 8),  # type: ignore[arg-type,return-value]
    "row" / Computed(lambda ctx: (int(ctx.number) & 0x000F0) >> 4),  # type: ignore[arg-type,return-value]
    "column" / Computed(lambda ctx: (int(ctx.number) & 0x0000F) >> 0),  # type: ignore[arg-type,return-value]
)

fe_chip_version = EnumStr(
    Bytes(1),
    RD53A=b"0",
    ITkpix_v1=b"1",
    ITkpix_v1p1=b"2",
    ITkpix_v2=b"3",
)

fe_chip_version_pcb = EnumStr(
    Bytes(1),
    RD53A=b"0",
    Prototype_ITkpix_v1=b"1",
    Pre_production_OS_ITkpix_v1=b"2",
    Pre_production_IS_ITkpix_v1=b"3",
    Production_OS_ITkpix_v2=b"4",
    Production_IS_ITkpix_v2=b"5",
    No_chip=b"9",
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
    "FE_chip_version" / fe_chip_version_pcb,
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

local_supports_production_type = EnumStr(
    Bytes(1),
    Pre_production=b"0",
    Production=b"1",
    Prototype=b"2",
    All_types=b"3",
)

local_supports_flavor = EnumStr(
    Bytes(1),
    L0=b"0",
    L1=b"1",
    R01=b"2",
    R0p5=b"3",
    R1=b"4",
)

local_supports_longeron_flavor = EnumStr(
    Bytes(1),
    L0=b"0",
    L1=b"1",
    R01=b"2",
    R0p5=b"3",
    R1=b"4",
    A_side=b"5",
    C_side=b"6",
)

local_supports = Struct(
    "layer" / Bytes(1),
    "production_type" / local_supports_production_type,
    "number" / Bytes(5),
)

local_supports_is = Struct(
    "production_type" / local_supports_production_type,
    "type" / local_supports_flavor,
    "number" / Bytes(5),
)

local_supports_longeron = Struct(
    "production_type" / local_supports_production_type,
    "type" / local_supports_longeron_flavor,
    "number" / Bytes(5),
)

local_supports_ihr = Struct(
    "production_type" / local_supports_production_type,
    "type" / local_supports_flavor,
    "position"
    / EnumStr(
        Bytes(1),
        Standard=b"1",
        Last=b"2",
    ),
    "number" / Bytes(4),
)

loaded_local_supports_ob_module = Struct(
    "production_type" / local_supports_production_type,
    "PCB_manufacturer" / pcb_manufacturer,
    "number" / Bytes(5),
)

local_supports_frame_box = Struct("type" / EnumStr(Bytes(1), Longeron=b"1", HR=b"2"))

orientation = EnumStr(
    Bytes(1),
    normal=b"0",
    mirror=b"1",
)

optoboard = Struct(
    "production_version"
    / EnumStr(
        Bytes(1),
        four=b"4",
    ),
    "LpGBT_count"
    / EnumStr(
        Bytes(1),
        one=b"1",
        two=b"2",
        four=b"4",
    ),
    "number" / Bytes(5),
)

optoboard_termination = Struct(
    "production_version" / Const(b"0"),
    "flavor"
    / EnumStr(
        Bytes(1),
        Normal_L_long=b"0",
        Normal_L_short=b"1",
        Mirror_L_long=b"2",
        Mirror_L_short=b"3",
        Normal_slim=b"4",
        Mirror_slim=b"5",
        Normal_extended_slim=b"6",
    ),
    "number" / Bytes(5),
)

optobox_powerboard_connector = Struct(
    "production_version" / Const(b"2"), "orientation" / orientation, "number" / Bytes(5)
)

optobox = Struct(
    "production_version" / Const(b"0"),
    "orientation" / orientation,
    "number" / Bytes(5),
)

canbus = Struct(
    "production_version" / Const(b"0"),
    "connector_type"
    / EnumStr(
        Bytes(1),
        six=b"6",
        eight=b"8",
    ),
    "number" / Bytes(5),
)

is_type = Struct(
    "production_version"
    / EnumStr(
        Bytes(1),
        Pre_production=b"0",
        Production=b"1",
    ),
    "flavor"
    / EnumStr(
        Bytes(1),
        Barrel_Triplet=b"0",
        Barrel_Quad=b"1",
        Ring_Triplet=b"2",
        Ring_Quad=b"3",
        Ring_Both=b"4",
    ),
    "subflavor"
    / EnumStr(
        Bytes(1),
        NA=b"0",
        F1=b"1",
        F2=b"2",
        F3=b"3",
        F4=b"4",
    ),
    "number" / Bytes(5),
)

pp0 = Struct(
    "production_version"
    / EnumStr(
        Bytes(1),
        Prototype=b"0",
        Pre_production=b"1",
        Production=b"2",
        Dummy=b"9",
    ),
    "flavor"
    / EnumStr(
        Bytes(1),
        Zp_3Stave=b"0",
        Zm_3Stave=b"1",
        Zp_2Stave=b"2",
        Zm_2Stave=b"3",
        Coupled_Ring=b"4",
        Intermediate_Ring=b"5",
        Quad_Ring=b"6",
    ),
    "number" / Bytes(5),
)

ob_type0_nonpp0 = Struct(
    "type" / EnumStr(Bytes(1), Flat=b"0", Inclined=b"1", Inclined_test_coupon=b"2"),
    "flavor"
    / Switch(
        lambda ctx: ctx.type,
        {
            "Flat": EnumStr(Bytes(1), Bottom=b"0", Top=b"1"),
            "Inclined": EnumStr(
                Bytes(1),
                Front=b"0",
                Back=b"1",
                Front_Last_ring=b"2",
                Back_Last_ring=b"3",
            ),
        },
    ),
    "version"
    / EnumStr(
        Bytes(1),
        Pre_production=b"0",
        Production=b"1",
        Prototype=b"9",
    ),
    "number" / Bytes(4),
)

ob_type0_pp0 = Struct(
    "type" / EnumStr(Bytes(1), Flat=b"0", Inclined=b"1", Inclined_test_coupon=b"2"),
    "flavor"
    / Switch(
        lambda ctx: ctx.type,
        {
            "Flat": EnumStr(
                Bytes(1), Short_L2=b"0", Long_L2=b"1", Short_L3_L4=b"2", Long_L3_L4=b"3"
            ),
            "Inclined": EnumStr(
                Bytes(1),
                L2_SP1=b"0",
                L2_SP2=b"1",
                L3_SP1=b"2",
                L3_SP2=b"3",
                L4_SP1=b"4",
                L4_SP2=b"5",
                Dummy=b"9",
            ),
        },
    ),
    "version"
    / EnumStr(
        Bytes(1),
        Pre_production=b"0",
        Production=b"1",
        Prototype=b"9",
    ),
    "number" / Bytes(4),
)

ob_type0 = Switch(
    lambda ctx: ctx.component_code,
    {"PP0": ob_type0_pp0, "Pigtail_panel": ob_type0_nonpp0, "Pigtail": ob_type0_nonpp0},
)

ob_type1_power = Struct(
    "type"
    / EnumStr(
        Bytes(1),
        Flat=b"0",
        Inclined=b"1",
    ),
    "serial_power_chains"
    / EnumStr(
        Bytes(1),
        F1=b"4",
        F2=b"2",
    ),
    "number" / Bytes(5),
)

ob_type1_data_bundle = Struct(
    "flavor"
    / EnumStr(
        Bytes(2),
        Flat_L2_Normal_Slim=b"00",
        Flat_L2_Mirror_Slim=b"01",
        Flat_L3_L4_Mirror_Slim=b"02",
        Flat_L3_L4_Normal_Slim=b"03",
        Inclined_L2_Normal_L_short=b"04",
        Inclined_L2_Normal_L_long=b"05",
        Inclined_L2_Mirror_L_short=b"06",
        Inclined_L2_Mirror_L_long=b"07",
        Inclined_L3_Normal_Slim10=b"08",
        Inclined_L3_Mirror_Slim10=b"09",
        Inclined_L4_Mirror_Slim16=b"10",
        Inclined_L4_Normal_Slim=b"11",
        Inclined_L3_L4_Mirror_Slim12=b"12",
        Inclined_L3_L4_Normal_Slim12=b"13",
    ),
)

ob_type1_data_termination = Struct(
    "version" / Bytes(1),
    "flavor"
    / EnumStr(
        Bytes(1),
        Normal_L_long=b"0",
        Normal_L_short=b"1",
        Mirror_L_long=b"2",
        Mirror_L_short=b"3",
        Normal_slim=b"4",
        Mirror_slim=b"5",
    ),
)

# FIXME: unused right now (see ob_type1_data)
ob_type1_data_inclined = Struct(
    "version" / Bytes(1),
    "manufacturer" / Bytes(1),
)

ob_type1_data = Struct(
    "_reserved" / Pointer(2, Bytes(2)),
    "data"
    / Switch(
        lambda ctx: ctx._reserved,
        {
            b"00": ob_type1_data_termination,
        },
        default=ob_type1_data_bundle,
    ),
    "length" / Bytes(2),
    "number" / Bytes(3),
)

ob_type1 = Switch(
    lambda ctx: ctx.component_code,
    {
        "Type_1_Power_DCS_line": ob_type1_power,
        "Type_1_Data_link": ob_type1_data,
    },
)

oe_type0_data_mapping = Switch(
    lambda ctx: ctx.layer,
    {
        "L2": EnumStr(
            Bytes(1),
            ring15_Front=b"0",
            ring15_Back=b"1",
            ring611_Front=b"2",
            ring611_Back=b"3",
        ),
        "L3": EnumStr(
            Bytes(1),
            Front_5downlinks=b"0",
            Back_5downlinks=b"1",
            Front_6downlinks=b"2",
            Back_6downlinks=b"3",
        ),
        "L4": EnumStr(
            Bytes(1),
            ring17_Front_4downlinks=b"0",
            ring17_Back_4downlinks=b"1",
            ring17_Front_5downlinks=b"2",
            ring17_Back_5downlinks=b"3",
            ring89_Front_4downlinks=b"4",
            ring89_Back_4downlinks=b"5",
            ring89_Front_5downlinks=b"6",
            ring89_Back_5downlinks=b"7",
        ),
    },
)

oe_type0 = Struct(
    "layer" / EnumStr(Bytes(1), L2=b"2", L3=b"3", L4=b"4", All=b"9"),
    "flavor"
    / Switch(
        lambda ctx: ctx._.component_code,
        {
            "Data_PP0": oe_type0_data_mapping,
        },
        default=Bytes(1),
    ),
    "reserved" / Const(b"0"),
    "number" / Bytes(4),
)

type0 = Switch(
    lambda ctx: ctx.subproject_code,
    {
        "inner_pixel": is_type,
        "outer_pixel_barrel": ob_type0,
        "pixel_general": Error,
        "pixel_endcaps": oe_type0,
    },
)

type1 = Switch(
    lambda ctx: ctx.subproject_code,
    {
        "inner_pixel": is_type,
        "outer_pixel_barrel": ob_type1,
        "pixel_general": Error,
        "pixel_endcaps": Error,
    },
)

yy_identifiers = {
    # pixel modules and subcomponents
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
    # local supports
    "IS_capillary": ("CP", "PI"),
    "IS_end_tube": ("ET", "PI"),
    "IS_cooling_tube": ("CA", "PI"),
    "IS_bare_local_support_stave": ("SS", "PI"),
    "IS_bare_local_support_ring": ("RS", "PI"),
    "IS_ring_local_support_assembly_loaded_ring": ("RL", "PI"),
    "IS_barrel_stave_assembly_loaded_stave": ("SL", "PI"),
    "OB_Base_Block": ("BB", "PB"),
    "OB_Cooling_Block": ("CB", "PB"),
    "OB_TPG_Tile": ("GT", "PB"),
    "OB_Local_Support_Inserts": ("IN", "PB"),
    "OB_Gusset": ("RG", "PB"),
    "OB_Truss": ("LT", "PB"),
    "OB_Half_Ring_Shell": ("RS", "PB"),
    "OB_End_of_longeron_Bracket_End_Gusset": ("EG", "PB"),
    "OB_Pipe_Support": ("PS", "PB"),
    "OB_Evaporator_Sleeves": ("ES", "PB"),
    "OB_Cooling_Pipe_IHR": ("RP", "PB"),
    "OB_Cooling_Pipe_Longeron": ("LP", "PB"),
    "OB_Functional_Pipe_for_IHR": ("RE", "PB"),
    "OB_Functional_Pipe_for_Longeron": ("LE", "PB"),
    "OB_End_of_longeron_Support": ("EL", "PB"),
    "OB_Bare_Module_Cell": ("BC", "PB"),
    "OB_Functional_IHR": ("FR", "PB"),
    "OB_Functional_Longeron": ("FL", "PB"),
    "OB_Loaded_Module_Cell": ("LC", "PB"),
    "OB_Loaded_IHR": ("LR", "PB"),
    "OB_Loaded_Longeron": ("LL", "PB"),
    "OB_IHR_Handling_Frame": ("HR", "PB"),
    "OB_Longeron_Handling_Frame": ("HL", "PB"),
    "OB_Bare_Cell_Transport_Box": ("TB", "PB"),
    "OEC_Trapezoids": ("TZ", "PE"),
    "OEC_Electrical break": ("EB", "PE"),
    "OEC_Inner_Rim_Insert": ("II", "PE"),
    "OEC_Outer_Rim_mounting_lugs": ("ML", "PE"),
    "OEC_Inner_Rim_Closeout": ("IC", "PE"),
    "OEC_Outer_Rim_Closeout": ("OC", "PE"),
    "OEC_Pipe_Closeout_support_closeout": ("SC", "PE"),
    "OEC_Half_Sandwich": ("HS", "PE"),
    "OEC_Evaporator": ("EV", "PE"),
    "OEC_Bare_half_ring_assembly_Bare_support": ("BH", "PE"),
    "OEC_Loaded_local_support_loaded_support": ("LS", "PE"),
    "OEC_Handling_frame_support_frame": ("SF", "PE"),
    "OEC_Transport/storage_box_support_box": ("SB", "PE"),
    "Local_support_handling_frame_box": ("LB", "PE", "PI", "PB"),
    "High_voltage_group": ("VG", "PE", "PI", "PB"),
    "Serial_powering_scheme": ("SP", "PE", "PI", "PB"),
    # services
    "Optoboard": ("OB", "PG"),
    "Optoboard_termination_board": ("OT", "PG"),  # codespell:ignore
    "Optobox": ("OX", "PG"),
    "Optobox_powerbox": ("OW", "PG"),
    "Optobox_connector_board": ("OC", "PG"),
    "Optobox_optical_fan_out": ("OF", "PG"),
    "Optopanel": ("OS", "PG"),
    "Optopanel_cooling_plate": ("OO", "PG"),
    "Optobox_powerboard": ("OP", "PG"),
    "GBCR_chip": ("OG", "PG"),
    "Vtrx_module": ("OV", "PG"),
    "Bpol2V5_chip": ("O5", "PG"),
    "Bpol12V_chip": ("O2", "PG"),
    "MOPS_chip": ("MP", "PG"),
    "Power_cables": ("OI", "PG"),
    "CAN_bus_cable": ("OD", "PG"),
    "Pigtail": ("PG", "PB"),
    "Rigid_flex": ("RF", "PI", "PB"),
    "Data_PP0": ("DP", "PI", "PE"),
    "Power_pigtail": ("PP", "PI", "PE"),
    "Power_bustape": ("PB", "PI", "PB", "PE"),
    "Bare_bustape": ("NB", "PE"),
    "Pigtail_panel": ("PL", "PB"),
    "PP0": ("P0", "PI"),
    "Finger": ("FI", "PI"),
    "Type_1_Data_link ": ("D1", "PI", "PB", "PE"),
    "Type_1_Power_DCS_line": ("P1", "PI", "PB", "PE"),
    "Type_1_Environmental_link": ("E1", "PI", "PB", "PE"),
    "PP1_connector": ("1P", "PI", "PB", "PE"),
    "PP1_connector_pieces_segments": ("CS", "PI", "PB", "PE"),
    "Type_1_strain_relief": ("SR", "PB"),
    "Type_2_power_cable": ("P2", "PI", "PB", "PE"),
    "Type_2_optobox_cable": ("20", "PI", "PB", "PE"),
    "PP2_box": ("2P", "PG"),
    "Type_3_HV_cable": ("P3", "PI", "PB", "PE"),
    "Type_3_LV_cable": ("L3", "PI", "PB", "PE"),
    "MOPS_cable": ("M3", "PG"),
    "TiLoc": ("TL", "PG"),
    "OPTO_MOP": ("OM", "PG"),
    "PP3_power": ("3P", "PG"),
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
    for subproject_code in ["PI", "PG", "PB", "PE"]
}

identifiers = Switch(
    lambda ctx: ctx.component_code,
    {
        "FE_chip_wafer": fe_chip,
        "FE_chip": fe_chip,
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
        # local supports
        "IS_capillary": local_supports_is,
        "IS_end_tube": local_supports_is,
        "IS_cooling_tube": local_supports_is,
        "IS_bare_local_support_stave": local_supports_is,
        "IS_bare_local_support_ring": local_supports_is,
        "IS_ring_local_support_assembly_loaded_ring": local_supports,
        "IS_barrel_stave_assembly_loaded_stave": local_supports,
        "OB_Base_Block": local_supports,
        "OB_Cooling_Block": local_supports,
        "OB_TPG_Tile": local_supports,
        "OB_Local_Support_Inserts": local_supports,
        "OB_Gusset": local_supports,
        "OB_Truss": local_supports,
        "OB_Half_Ring_Shell": local_supports,
        "OB_End_of_longeron_Bracket_End_Gusset": local_supports,
        "OB_Pipe_Support": local_supports,
        "OB_Evaporator_Sleeves": local_supports,
        "OB_Cooling_Pipe_IHR": local_supports,
        "OB_Cooling_Pipe_Longeron": local_supports,
        "OB_Functional_Pipe_for_IHR": local_supports,
        "OB_Functional_Pipe_for_Longeron": local_supports,
        "OB_End_of_longeron_Support": local_supports,
        "OB_Bare_Module_Cell": local_supports,
        "OB_Functional_IHR": local_supports_ihr,
        "OB_Functional_Longeron": local_supports_longeron,
        "OB_Loaded_Module_Cell": loaded_local_supports_ob_module,
        "OB_Loaded_IHR": local_supports,
        "OB_Loaded_Longeron": local_supports,
        "OB_IHR_Handling_Frame": local_supports,
        "OB_Longeron_Handling_Frame": local_supports,
        "OB_Bare_Cell_Transport_Box": local_supports,
        "OEC_Trapezoids": local_supports,
        "OEC_Electrical break": local_supports,
        "OEC_Inner_Rim_Insert": local_supports,
        "OEC_Outer_Rim_mounting_lugs": local_supports,
        "OEC_Inner_Rim_Closeout": local_supports,
        "OEC_Outer_Rim_Closeout": local_supports,
        "OEC_Pipe_Closeout_support_closeout": local_supports,
        "OEC_Half_Sandwich": local_supports,
        "OEC_Evaporator": local_supports,
        "OEC_Bare_half_ring_assembly_Bare_support": local_supports,
        "OEC_Loaded_local_support_loaded_support": local_supports,
        "OEC_Handling_frame_support_frame": local_supports,
        "OEC_Transport/storage_box_support_box": local_supports,
        "Local_support_handling_frame_box": local_supports_frame_box,
        "High_voltage_group": local_supports,
        "Serial_powering_scheme": local_supports,
        # services
        "Optoboard": optoboard,
        "Optoboard_termination_board": optoboard_termination,
        "Optobox": optobox,
        "Optobox_powerbox": optobox,
        "Optobox_connector_board": optobox_powerboard_connector,
        "Optobox_optical_fan_out": optobox,
        "Optopanel": Error,
        "Optopanel_cooling_plate": Error,
        "Optobox_powerboard": optobox_powerboard_connector,
        "GBCR_chip": Error,
        "Vtrx_module": Error,
        "Bpol2V5_chip": Error,
        "Bpol12V_chip": Error,
        "MOPS_chip": Error,
        "Power_cables": Error,
        "CAN_bus_cable": canbus,
        "Pigtail": type0,
        "Rigid_flex": Error,
        "Data_PP0": type0,
        "Power_pigtail": Error,
        "Power_bustape": Error,
        "Bare_bustape": Error,
        "Pigtail_panel": type0,
        "PP0": pp0,
        "Finger": Error,
        "Type_1_Data_link ": type1,
        "Type_1_Power_DCS_line": type1,
        "Type_1_Environmental_link": Error,
        "PP1_connector": Error,
        "PP1_connector_pieces_segments": Error,
        "Type_1_strain_relief": Error,
        "Type_2_power_cable": Error,
        "Type_2_optobox_cable": Error,
        "PP2_box": Error,
        "Type_3_HV_cable": Error,
        "Type_3_LV_cable": Error,
        "MOPS_cable": Error,
        "TiLoc": Error,
        "OPTO_MOP": Error,
        "PP3_power": Error,
    },
    # default=Bytes(7),
)
