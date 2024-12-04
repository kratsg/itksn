from __future__ import annotations

from typing import TypeVar

from construct import (
    Bytes,
    Computed,
    Const,
    Construct,
    Error,
    GreedyBytes,
    Pass,
    Pointer,
    Select,
    Struct,
    Switch,
)

from itksn.common import EnumStr

pcb_manufacturer = EnumStr(
    Bytes(1),
    Dummy=b"0",
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

batch_number = {
    0: b"RD53A",
    1: b"ITkpix_v1",
    2: b"ITkpix_v2",
    3: b"ITkpix_v2",
    4: b"ITkpix_v2",
    5: b"ITkpix_v2",
    6: b"ITkpix_v2",
    7: b"ITkpix_v2",
    8: b"ITkpix_v2",
    9: b"ITkpix_v2",
    10: b"ITkpix_v2",
    11: b"ITkpix_v2",
    12: b"ITkpix_v2",
    13: b"ITkpix_v2",
    14: b"ITkpix_v2",
    15: b"ITkpix_v2",
}

fe_chip = Struct(
    "number" / Bytes(7),
    "batch_number" / Computed(lambda ctx: (int(ctx.number) & 0xF0000) >> 16),  # type: ignore[arg-type,return-value]
    "batch" / Computed(lambda ctx: batch_number[ctx.batch_number]),  # type: ignore[arg-type,return-value]
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
    No_chip=b"9",
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
        Dummy_sensor_tile=b"9",
    ),
    "number" / Bytes(5),
)

pcb_loading_site = EnumStr(
    Bytes(1), Oslo=b"2", TOPRO=b"5", NORBIT=b"6", CERN=b"7", unloaded=b"9"
)

pcb_reception_site = EnumStr(
    Bytes(1),
    Genova=b"0",
    Barcelona=b"1",
    Oslo=b"2",
    Milano=b"3",
    Bergen=b"4",
)

pcb = Struct(
    "FE_chip_version" / fe_chip_version_pcb,
    "PCB_manufacturer" / pcb_manufacturer,
    "number" / Bytes(5),
)

pcb_triplets = Struct(
    "FE_chip_version" / fe_chip_version_pcb,
    "PCB_manufacturer" / pcb_manufacturer,
    "loading"
    / Switch(
        lambda ctx: ctx.PCB_manufacturer, {"Dummy": Bytes(1)}, default=pcb_loading_site
    ),  # esdape hatch for some dummy/digitals
    "reception"
    / Switch(
        lambda ctx: ctx.PCB_manufacturer,
        {"Dummy": Bytes(1)},
        default=pcb_reception_site,
    ),  # esdape hatch for some dummy/digitals
    "number" / Bytes(3),
)


module = Struct(
    "FE_chip_version" / fe_chip_version,
    "PCB_manufacturer"
    / Switch(
        lambda ctx: ctx.FE_chip_version, {"RD53A": pcb_manufacturer}, default=Pass
    ),
    "number" / GreedyBytes,
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
        Not_used=b"0",
        Triplet_v1p0=b"1",
        Quad_v2p1=b"2",
        Quad_v4p1=b"3",
        Quad_v4p2=b"4",
        Quad_v4p3=b"5",
    ),
    "manufacturer" / Bytes(1),
    "number" / Bytes(4),
)

local_supports_production_type = EnumStr(
    Bytes(1),
    Pre_production=b"0",
    Production=b"1",
    Prototype=b"2",
    All_types=b"9",
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

# FIXME: is the rest not defined?
local_supports_frame_box = Struct(
    "type" / EnumStr(Bytes(1), Longeron=b"1", HR=b"2"), "number" / Bytes(6)
)

orientation = EnumStr(
    Bytes(1),
    normal=b"0",
    mirror=b"1",
)

optoboard = Struct(
    "production_version"
    / Select(
        Const(b"2"), Const(b"3"), Const(b"4"), Const(b"5")
    ),  # FIXME: "2", "3", "5" not defined in table 6
    "LpGBT_count"
    / EnumStr(
        Bytes(1),
        one=b"1",
        two=b"2",
        four=b"4",
    ),
    "number" / Bytes(5),
)

termination_board = Struct(
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
        Normal_extended_slim=b"6",  # FIXME: OB Type-1 Termination Board does not have this
    ),
    "number" / Bytes(5),
)

optobox_powerboard_connector = Struct(
    "production_version"
    / Select(
        Const(b"0"), Const(b"2"), Const(b"3")
    ),  # FIXME: "0" and "3" not in table 9
    "orientation" / orientation,
    "number" / Bytes(5),
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

is_cable = Struct(
    "production_version"
    / EnumStr(
        Bytes(1),
        Pre_production=b"0",
        Production=b"1",
        Dummy=b"9",
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
    "number" / Bytes(4),
)

pi_type0_pp0 = Struct(
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

# PB-PL, PB-PG
pb_type0_cable = Struct(
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

# PB-RF
pb_type0_pp0 = Struct(
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
            "Inclined_test_coupon": EnumStr(  # FIXME: not specified in Table 21
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

pb_type1_power = Struct(
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

pb_type1_data_bundle = Struct(
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

pb_type1_data_inclined = Struct(
    "version" / Bytes(1),
    "manufacturer" / Bytes(1),
)

pb_type1_data = Struct(
    "_reserved" / Pointer(2, Bytes(2)),
    "data"
    / Switch(
        lambda ctx: ctx._reserved,  # pylint: disable=protected-access
        {
            b"00": pb_type1_data_inclined,
        },
        default=pb_type1_data_bundle,
    ),
    "length" / Bytes(2),
    "number" / Bytes(3),
)

pe_type0_data_mapping = Switch(
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

pe_type0_data = Struct(
    "layer" / EnumStr(Bytes(1), L2=b"2", L3=b"3", L4=b"4", All=b"9"),
    "flavor" / pe_type0_data_mapping,
    "reserved" / Const(b"0"),
    "number" / Bytes(4),
)

pe_type0_power = Struct(
    "layer" / EnumStr(Bytes(1), L2=b"2", L3=b"3", L4=b"4", All=b"9"),
    "flavor" / Bytes(1),
    "reserved" / Const(b"0"),
    "number" / Bytes(4),
)

# FIXME: merge with pe_type0_power?
# 1P (PP1_connector) or PB (Power_bustape)
pe_type1 = Struct(
    "flavor" / Bytes(1),
    "reserved" / Const(b"0"),
    "length"
    / EnumStr(
        Bytes(1),
        _50cm=b"0",
        _250cm=b"9",
    ),
    "number" / Bytes(4),
)

type2 = Struct(
    "flavor"
    / Switch(
        lambda ctx: ctx._.component_code,
        {
            "Type_2_power_cable": EnumStr(Bytes(1), normal=b"1", abnormal=b"2"),
            "Type_2_optobox_cable": Const(b"0"),
            "PP2_box": EnumStr(
                Bytes(1),
                F1=b"1",
                F2=b"2",
                F3=b"3",
                F4=b"4",
                F5=b"5",
                F6=b"6",
                F7=b"7",
                F8=b"8",
            ),
        },
    ),
    "number" / Bytes(6),
)

type3 = Struct(
    "flavor" / Const(b"0"),
    "numbers" / Bytes(6),
)

type4 = Struct(
    "flavor"
    / EnumStr(
        Bytes(1),
        Pre_production_non_rad_hard=b"0",
        Pre_production_rad_hard=b"1",
        Production=b"2",
    )
)

mops_chip = Struct(
    "reserved" / Const(b"00"),
    "production_version"
    / EnumStr(
        Bytes(1),
        Pre_production=b"0",
        Production=b"3",
    ),
    "vendor" / Bytes(4),
)

# from construct-typing
ParsedType_co = TypeVar("ParsedType_co", covariant=True)
BuildTypes_contra = TypeVar("BuildTypes_contra", contravariant=True)


def subproject_switch(
    pg: Construct[ParsedType_co, BuildTypes_contra] | None = None,
    pi: Construct[ParsedType_co, BuildTypes_contra] | None = None,
    pe: Construct[ParsedType_co, BuildTypes_contra] | None = None,
    pb: Construct[ParsedType_co, BuildTypes_contra] | None = None,
) -> Construct[ParsedType_co, BuildTypes_contra]:
    return Switch(
        lambda ctx: ctx.subproject_code,
        {
            "inner_pixel": pi or Error,
            "outer_pixel_barrel": pb or Error,
            "pixel_general": pg or Error,
            "pixel_endcaps": pe or Error,
        },
    )


"""
TP: OEC Ti pipe for HR - TI_PIPE_L2 (20UPETP2000001, 20UPETP2000002, 20UPETP2000003, 20UPETP2000004, 20UPETP2000005, 20UPETP2000007, 20UPETP2000008, 20UPETP2000009, 20UPETP2000010, 20UPETP2000012, 20UPETP2000013, 20UPETP2000014, 20UPETP2000015, 20UPETP2000016, 20UPETP2000017, 20UPETP2000018, 20UPETP2000019, 20UPETP2100001, 20UPETP2100002, 20UPETP2100003, 20UPETP2100004, 20UPETP2100005, 20UPETP2100006, 20UPETP2100007, 20UPETP2100008, 20UPETP2100009, 20UPETP2100010, 20UPETP2100011, 20UPETP2100012, 20UPETP2100013, 20UPETP2100014, 20UPETP2100015, 20UPETP2100016, 20UPETP2100017, 20UPETP2100018, 20UPETP2100019, 20UPETP2100020, 20UPETP2100021, 20UPETP2100022, 20UPETP2100023, 20UPETP2100024, 20UPETP2100025, 20UPETP2100026, 20UPETP2100027, 20UPETP2100028, 20UPETP2100029, 20UPETP2100030, 20UPETP2100031, 20UPETP2100032, 20UPETP2100033, 20UPETP2100034, 20UPETP2100035, 20UPETP2100036, 20UPETP2100037, 20UPETP2100038, 20UPETP2100039, 20UPETP2100040, 20UPETP2200001, 20UPETP2200002, 20UPETP2200003, 20UPETP2200004, 20UPETP2900001, 20UPETP2900002, 20UPETP2900003, 20UPETP2900004, 20UPETP3000001, 20UPETP3000002, 20UPETP3000003, 20UPETP3000004, 20UPETP3200001, 20UPETP3200002, 20UPETP3200003, 20UPETP3200004, 20UPETP3200005, 20UPETP3900001, 20UPETP3900002, 20UPETP3900003, 20UPETP4000002, 20UPETP4000003, 20UPETP4000004, 20UPETP4000005, 20UPETP4000006, 20UPETP4000007, 20UPETP4000008, 20UPETP4000009, 20UPETP4200001, 20UPETP4200002, 20UPETP4200003)
LM: OB Loaded Module Cell - Dummy (20UPBLM0000015, 20UPBLM0000016, 20UPBLM0000017, 20UPBLM0000018, 20UPBLM0000019, 20UPBLM0000020, 20UPBLM0000021, 20UPBLM0000022, 20UPBLM0000023, 20UPBLM0000024, 20UPBLM0000025, 20UPBLM0000026, 20UPBLM0000027, 20UPBLM0000028, 20UPBLM0000029, 20UPBLM0000030, 20UPBLM0000031, 20UPBLM0000032, 20UPBLM0000033, 20UPBLM0000034, 20UPBLM0000035, 20UPBLM0000036, 20UPBLM0000037, 20UPBLM0000038, 20UPBLM0000039, 20UPBLM0000040, 20UPBLM0000041, 20UPBLM0000042, 20UPBLM0000043, 20UPBLM0000044, 20UPBLM0000045, 20UPBLM0000046, 20UPBLM0000047, 20UPBLM0000048, 20UPBLM0000049, 20UPBLM0000050, 20UPBLM0000089, 20UPBLM0000126, 20UPBLM0000127, 20UPBLM0000128, 20UPBLM0000129, 20UPBLM0000130, 20UPBLM0000131, 20UPBLM0000132, 20UPBLM0000133, 20UPBLM0000134, 20UPBLM0000135, 20UPBLM0000136, 20UPBLM0000137, 20UPBLM0000138, 20UPBLM0000139, 20UPBLM0000140, 20UPBLM0000141, 20UPBLM0000142, 20UPBLM0000143, 20UPBLM0000144, 20UPBLM0000145, 20UPBLM0000146, 20UPBLM0000147, 20UPBLM0000148, 20UPBLM0000149, 20UPBLM0000150, 20UPBLM0000151, 20UPBLM0000152, 20UPBLM0000153, 20UPBLM0000154, 20UPBLM0000155, 20UPBLM0000156, 20UPBLM0000157, 20UPBLM0000158, 20UPBLM0000159, 20UPBLM0000160, 20UPBLM0000161, 20UPBLM0000162, 20UPBLM0000163, 20UPBLM0000164, 20UPBLM0000197, 20UPBLM0000198)
YZ: test module monika - quad module (20UPGYZ0000001, 20UPGYZ0000003, 20UPGYZ0000004, 20UPGYZ0000005, 20UPGYZ1000001, 20UPGYZ1000002, 20UPGYZ1000003, 20UPGYZ1000007, 20UPGYZ2000001, 20UPGYZ2000002, 20UPGYZ2000004, 20UPGYZ3000001, 20UPGYZ3000002, 20UPGYZ3000003, 20UPGYZ3000004, 20UPGYZ3000005, 20UPGYZ3000006, 20UPGYZ3000007, 20UPGYZ3000008, 20UPGYZ3000009, 20UPGYZ3000010, 20UPGYZ3000011, 20UPGYZ3000012, 20UPGYZ3000013, 20UPGYZ3000014, 20UPGYZ3000015, 20UPGYZ3000016, 20UPGYZ3000017, 20UPGYZ3000018, 20UPGYZ3000019, 20UPGYZ3000020, 20UPGYZ3000021, 20UPGYZ3000022, 20UPGYZ3000023, 20UPGYZ3000024, 20UPGYZ3000025, 20UPGYZ3000026, 20UPGYZ3000027, 20UPGYZ3000028, 20UPGYZ3000029, 20UPGYZ3000030, 20UPGYZ3000031, 20UPGYZ3000032, 20UPGYZ3000033, 20UPGYZ3000034, 20UPGYZ3000035, 20UPGYZ3000036, 20UPGYZ3000037, 20UPGYZ3000038, 20UPGYZ3000039, 20UPGYZ3000040, 20UPGYZ3000041, 20UPGYZ3000042, 20UPGYZ3000043, 20UPGYZ3000044, 20UPGYZ3000045, 20UPGYZ3000046, 20UPGYZ3000047, 20UPGYZ3000048, 20UPGYZ3000049, 20UPGYZ3000050, 20UPGYZ3000051, 20UPGYZ3000052, 20UPGYZ3000053)
ZZ: test chip monika - test chip (20UPGZZ0000001, 20UPGZZ0000002, 20UPGZZ0000012, 20UPGZZ0000013, 20UPGZZ0000014, 20UPGZZ0000015, 20UPGZZ0000016, 20UPGZZ0001001, 20UPGZZ0001002, 20UPGZZ0001003, 20UPGZZ0001004, 20UPGZZ0001005, 20UPGZZ0001006, 20UPGZZ0001007, 20UPGZZ0001008, 20UPGZZ0001009, 20UPGZZ0001010, 20UPGZZ0001011, 20UPGZZ0001012, 20UPGZZ0001013, 20UPGZZ0100001, 20UPGZZ0100002, 20UPGZZ0100003, 20UPGZZ1000001, 20UPGZZ1000002, 20UPGZZ1000003, 20UPGZZ1000004, 20UPGZZ1100001, 20UPGZZ1100002, 20UPGZZ1100003, 20UPGZZ1100004, 20UPGZZt000001, 20UPGZZty00001)
X1: Module - Dummy quad module (20UPGX10000001, 20UPGX10099998, 20UPGX10268255, 20UPGX12110040, 20UPGX12110055, 20UPGX12110397, 20UPGX12901105, 20UPGX19110133, 20UPGX19110134, 20UPGX19110135, 20UPGX19110136, 20UPGX19110154, 20UPGX19110159, 20UPGX19110160, 20UPGX19110217, 20UPGX19110218, 20UPGX19110219, 20UPGX19110220, 20UPGX19110230, 20UPGX19110334, 20UPGX19110336, 20UPGX19110388, 20UPGX19110438, 20UPGX19110502, 20UPGX19110503, 20UPGX19110504, 20UPGX19110505, 20UPGX19110507, 20UPGX19110508, 20UPGX19110541, 20UPGX19110542, 20UPGX19110543, 20UPGX19110544, 20UPGX19210365, 20UPGX19210367, 20UPGX19910047, 20UPGX19910048, 20UPGX19910057, 20UPGX19910063, 20UPGX19910113, 20UPGX19910114, 20UPGX19910115, 20UPGX19910463, 20UPGX19910510, 20UPGX19910511, 20UPGX19910539, 20UPGX19910548)
MQ: ModuleSiteQualification - Module Site Qualification OBJECT (20UPGMQ0000001, 20UPGMQ0000002, 20UPGMQ0000003, 20UPGMQ0000005, 20UPGMQ0000006, 20UPGMQ0000007, 20UPGMQ0000008, 20UPGMQ0000009, 20UPGMQ0000010, 20UPGMQ0000011, 20UPGMQ0000013, 20UPGMQ0000014, 20UPGMQ0000015, 20UPGMQ0000016, 20UPGMQ0000017, 20UPGMQ0000018, 20UPGMQ0000019, 20UPGMQ0000020, 20UPGMQ0000021, 20UPGMQ0000022, 20UPGMQ0000023, 20UPGMQ0000024, 20UPGMQ0000026, 20UPGMQ0000027, 20UPGMQ0000028, 20UPGMQ0000029, 20UPGMQ0000030, 20UPGMQ0000031, 20UPGMQ0000032, 20UPGMQ0000035)
FX: Front-end Chip - Tutorial FE chip (20UPGFX0009233, 20UPGFX0009234, 20UPGFX0009249, 20UPGFX0009250, 20UPGFX0009251, 20UPGFX0009252, 20UPGFX0009265, 20UPGFX0009266, 20UPGFX0009267, 20UPGFX0009489, 20UPGFX0009490, 20UPGFX0009505, 20UPGFX0009506, 20UPGFX0009507, 20UPGFX0009508, 20UPGFX0009509, 20UPGFX0009510, 20UPGFX0009511, 20UPGFX0009512, 20UPGFX0009513, 20UPGFX2990001)
TT: test module - OB module (20UPGTT0000007, 20UPGTT0000008, 20UPGTT0000009, 20UPGTT1000001, 20UPGTT1012345, 20UPGTT2000002, 20UPGTT2010001, 20UPGTTA000002, 20UPGTTA0x1F23, 20UPGTTB000001, 20UPGTTB000002)
KW: Front-end Chip - ITkpix_V1 (20UPGKW0000001, 20UPGKW0000002, 20UPGKW0000003, 20UPGKW0000004, 20UPGKW0000005, 20UPGKW0000006, 20UPGKW0000007, 20UPGKW0000008, 20UPGKW0000101, 20UPGKW0000102, 20UPGKW0099999)
ZS: OB Loaded Module Cell - Dummy (20UPBZS0000001, 20UPBZS0000002, 20UPBZS0000003, 20UPBZS0000004, 20UPBZS0000005, 20UPBZS0000006, 20UPBZS0000007, 20UPBZS0000008, 20UPBZS0000009, 20UPBZS0000010, 20UPBZS0000011)
G9: Bare Module - Digital quad bare module (20UPGG92901054, 20UPGG92901055, 20UPGG92901056, 20UPGG92901057, 20UPGG92901058, 20UPGG92901059, 20UPGG92901060, 20UPGG92901105)
CC: Coffee club component - Common type (20UPGCC0000001, 20UPGCC0000002, 20UPGCC0000003, 20UPGCC0000004, 20UPGCC0000005)
RA: Front-end Chip - RD53A (20UPGRA0000730, 20UPGRA0000731)
MO: Module (20UPBMO0000007, 20UPBMO0000008, 20UPBMO0000009)
KG: Bare Module - Quad bare module (20UPGKGW999998, 20UPGKGW999999)
GS: Glue - SE4445 (20UPIGS270824B, 20UPIGS270824C)
TR: OB Truss - Dummy (20UPBTR0000001, 20UPBTR0000002)
R1: Module - Dummy quad module (20UPGR10021016, 20UPGR10099999)
30: OEC Evaporator - EV_L3 (20UPE300000001, 20UPE300000002)
3D: Module (20UPG3D0000010)
R4: Module - Dummy triplet L0 ring0 module (20UPIR40099999)
TC: Triplet Shipping Create (20UPGTC0000001)
40: OEC Evaporator - EV_L4 (20UPE400000001)
00: Sensor Tile (20UPI000000007, 20UPI000000008, 20UPI000000009, 20UPI000000010, 20UPI000000011, 20UPI000000034, 20UPI000000035, 20UPI000000036, 20UPI000000041, 20UPI000000042, 20UPI000000043, 20UPI000000044, 20UPI000000045, 20UPI000000046, 20UPI000000047, 20UPI000000048, 20UPI000000049, 20UPI000000050, 20UPI000000051, 20UPI000000052, 20UPI000000053, 20UPI000000057, 20UPI000000058, 20UPI000000059, 20UPI000000063, 20UPI000000066, 20UPI000000067, 20UPI000000071, 20UPI000000072, 20UPI000000074, 20UPI000000075, 20UPI000000076, 20UPI000000077, 20UPI000000082, 20UPI000000083, 20UPI000000084, 20UPI000000085, 20UPI000000086, 20UPI000000089, 20UPI000000090, 20UPI000000091, 20UPI000000092, 20UPI000000093, 20UPI000000094, 20UPI000000095, 20UPI000000096, 20UPI000000097, 20UPI000000098, 20UPI000000099)
QT: PP1 Connector - Dummy (20UPBQT1000001, 20UPBQT1080001, 20UPBQT1190001, 20UPBQT1200001, 20UPBQT1200002, 20UPBQT1400001, 20UPBQT1580001, 20UPBQT1580002, 20UPBQT9080001, 20UPBQT9280001, 20UPBQT9280002, 20UPBQT9380001, 20UPBQT9380002, 20UPBQT9380003, 20UPBQT9380004, 20UPBQT9400001, 20UPBQT9480001, 20UPBQT9480002, 20UPBQT9580001, 20UPBQT9590001)
XT: Sensor Tile - Dummy teststructure (20UPIXT5100001, 20UPIXT5100002, 20UPIXT5100003, 20UPIXT5100004, 20UPIXT5400001, 20UPIXT5400002, 20UPIXT5400003, 20UPIXT5400004, 20UPIXT5400005, 20UPIXT5400006, 20UPIXT5400007, 20UPIXT5400008, 20UPIXT5400009, 20UPIXT5400010, 20UPIXT5400011, 20UPIXT5400012, 20UPIXT5400013, 20UPIXT5400014, 20UPIXT5400015, 20UPIXT5400016, 20UPIXT5500001, 20UPIXT5500002, 20UPIXT5500003, 20UPIXT5500004, 20UPIXT5500005, 20UPIXT5500006, 20UPIXT5500007, 20UPIXT5500008, 20UPIXT5500009, 20UPIXT5500010, 20UPIXT5500011, 20UPIXT5500012, 20UPIXT5600001, 20UPIXT5600002, 20UPIXT5600003, 20UPIXT5600004, 20UPIXT5600005, 20UPIXT5600006, 20UPIXT5600007, 20UPIXT5600008, 20UPIXT5600009, 20UPIXT5600010, 20UPIXT5600011, 20UPIXT5600012)
XC: Module carrier - Tutorial Carrier (20UPGXC0000000, 20UPGXC0000001, 20UPGXC0000002, 20UPGXC0000010, 20UPGXC0000013, 20UPGXC0000014, 20UPGXC0000016, 20UPGXC0000017, 20UPGXC0000018, 20UPGXC0000020, 20UPGXC0000027, 20UPGXC0000030, 20UPGXC0000031, 20UPGXC0000032, 20UPGXC0000035, 20UPGXC0000038, 20UPGXC0000041, 20UPGXC0000042, 20UPGXC0000111, 20UPGXC0000200, 20UPGXC0000201, 20UPGXC0000202, 20UPGXC0000203, 20UPGXC0000210, 20UPGXC0999998, 20UPGXC0999999, 20UPGXC1000200, 20UPGXC1008795, 20UPGXC2990001, 20UPGXC5000004, 20UPGXC5000005, 20UPGXC5000006, 20UPGXC5000007, 20UPGXC5000008, 20UPGXC5000010, 20UPGXC9000001, 20UPGXC9000002)
SU: Sensor Tile - Planar Sensor Test Structure (150 µm thickness) (20UPBSU3400001, 20UPBSU3400002, 20UPBSU3400003, 20UPBSU3400004, 20UPBSU3400005, 20UPBSU3400006, 20UPBSU3400007, 20UPBSU3400008, 20UPBSU3400009, 20UPBSU3400010, 20UPBSU3400011, 20UPBSU3400012, 20UPBSU3400013, 20UPBSU3400014, 20UPBSU3400015, 20UPBSU3500001, 20UPBSU3500002, 20UPBSU3500003, 20UPBSU3500004, 20UPBSU3500005, 20UPBSU3600001, 20UPBSU3600002, 20UPBSU3600003, 20UPBSU3600004, 20UPBSU3600005, 20UPBSU3700001, 20UPBSU3700002, 20UPBSU3700003, 20UPBSU3700004, 20UPBSU3700005)

# exists, not defined well
S8: Sensor Tile - Full-size Planar Sensor Tile (100 µm thickness) (20UPGS81300003, 20UPGS81300004, 20UPGS81300005, 20UPGS81300006, 20UPGS81300007, 20UPGS82300001, 20UPGS82300002, 20UPGS82300003, 20UPGS82300004, 20UPGS82300005, 20UPGS82300006, 20UPGS82300007, 20UPGS82300008, 20UPGS82300009, 20UPGS82300010, 20UPGS82300011, 20UPGS82300012, 20UPGS82300013, 20UPGS82300014, 20UPGS82300015, 20UPGS82300016, 20UPGS82300017, 20UPGS82300018, 20UPGS82300019, 20UPGS82300020, 20UPGS82300021, 20UPGS83300001, 20UPGS83300003)
Ob: Optoboard (20UPGOb0000001, 20UPGOb0000002, 20UPGOb0000003, 20UPGOb0000004, 20UPGOb0000005, 20UPGOb0000006, 20UPGOb0000007, 20UPGOb0000008, 20UPGOb0000009, 20UPGOb0000010, 20UPGOb0000011, 20UPGOb0000012, 20UPGOb0000013, 20UPGOb0000014, 20UPGOb0000015, 20UPGOb0000016)
PB: OEC Bus Tape - BT_L2 (20UPEPB0200041, 20UPEPB0200042, 20UPEPB0200043, 20UPEPB0200044, 20UPEPB0200051, 20UPEPB0200052, 20UPEPB0200053, 20UPEPB0300041, 20UPEPB0300042, 20UPEPB0300051, 20UPEPB0300052, 20UPEPB0400041, 20UPEPB0400042, 20UPEPB0400051)
M1: Module - L1 Quad Module (20UPGM12101076, 20UPGM12101259, 20UPGM12110001, 20UPGM12110002, 20UPGM12110003, 20UPGM12110246, 20UPGM12110247, 20UPGM12110248, 20UPGM12110378, 20UPGM12110379)
S2: Sensor Tile - L1 Inner Pixel Quad Sensor Tile (20UPGS22300021, 20UPGS22300022, 20UPGS22300023, 20UPGS22300024, 20UPGS22300025, 20UPGS29900001, 20UPGS29900002)
SH: OB Carbon Ring - Dummy (20UPBSH0000001, 20UPBSH0000002, 20UPBSH0000003, 20UPBSH0000004, 20UPBSH0000005, 20UPBSH0000006, 20UPBSH0000007)
S3: Sensor Tile - Outer Pixel Quad Sensor Tile (20UPBS33300001, 20UPBS33300002, 20UPBS33300003, 20UPBS33300004, 20UPBS33300005, 20UPBS33300006, 20UPBS35100001)
XS: Dummy tutorial sensor tile (20UPIXS5300001, 20UPIXS5300002, 20UPIXS5300003, 20UPIXS5300004, 20UPIXS5300005, 20UPEXS2100001)
lp: lpGBT - lpGBT V0 (20UPGlp0000005, 20UPGlp0000006, 20UPGlp0000007, 20UPGlp0000008, 20UPGlp0000009, 20UPGlp0000010)
P5: Module PCB - Triplet L0 R0.5 PCB (20UPIP51202001, 20UPIP51202002, 20UPIP51202003, 20UPIP51202004, 20UPIP51202005)
LS: IS Bare Local Support - L0 Stave Structure (20UPILS9000001, 20UPILS9000002, 20UPILS9000003)
HT: Sensor Tile - Planar Sensor Halfmoon (100 µm thickness) (20UPGHT2200017, 20UPGHT2200018, 20UPGHT2200019, 20UPGHT2200020)
RS: Module (20UPGRS0000035, 20UPGRS0000036)
LB: OB Local Support HF Box - OB Longeron box (20UPBLBL000007, 20UPBLBL000008, 20UPBLBR000008)
XM: Module - Dummy triplet L0 ring0 module (20UPGXM0999999, 20UPGXMS999999)
XP: Module PCB - Tutorial PCB (20UPGXP2990001, 20UPGXPR999999, 20UPGXPS999999)
PQ: Module PCB - Quad PCB (20UPGPQ0900024, 20UPGPQ0900029, 20UPGPQ0900032)
BS: OEC Bare Half Ring Assembly - BHR_L2 (20UPEBS2200003, 20UPEBS2200004, 20UPEBS4200003)
XB: Bare Module - Tutorial bare module (20UPGXB100102)
P1: OB Type-1 Power Superbundle - Mixed (20UPBP12380001, 20UPBP12480001), IS Type-1 Power (20UPIP19000001, 20UPIP19100001)
MC: MOPS Chip (20UPGMC0000000)
HR: OB Inclined Half-Ring HF - L2 std (20UPBHR2S00001)
CP: OB Cooling Pipe for IHR - Dummy (20UPBCP0000003)
W0: Sensor Wafer - L0 Inner Pixel 3D Sensor Wafer (25x100) (20UPGW00000001)
Os: Optopanel (20UPGOs0000001)
W7: Sensor Wafer - Planar sensor wafer (150 μm thickness) (20UPBW72000001)
W3: Sensor Wafer - Outer Pixel Sensor Wafer (150 μm thickness) (20UPBW33000001)
W2: Sensor Wafer - L1 Inner Pixel Sensor Wafer (100 μm thickness) (20UPGW22000005)
W1: Sensor Wafer - L0 Inner Pixel 3D Sensor Wafer (50x50) (20UPGW18000001)
MP: MOPS Chip (1482 defined with 20UPGMP10 or 20UPGMP20, not defined in SN document)
QR: OEC Type-1 Power Bundle - Dummy ("20UPEQR2200001")

OK: Bpol2V5 carrier board (no SN definition)
OL: IpGBT chip (no SN definition)
OG: GBCR chip (no SN definition)
NB: Bare bustape (no SN definition)
QT: Dummy PP1 connector (no SN definition)
1P: PP1 connector (no SN definition)
DP: Data PP0 (no clear SN definition for PI)
G4: 4" bare module gel pack (no SN definition)
OI: Power cables (no SN definition)
PP: Power pigtail (no clear SN definition for PI)
OS: Optopanel (no clear SN definition)
XG: Dummy bare module gel pack (no clear SN definition)

"""

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
    "FourInch_bare_module_gel_pack": ("G4", "PG"),
    "SixInch_bare_module_gel_pack": ("G6", "PG"),
    "Triplet_L0_Stave_PCB": ("PT", "PI"),
    "Triplet_L0_R0_PCB": ("P0", "PI"),
    "Triplet_L0_R0p5_PCB": ("P5", "PI"),
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
    # dummy for testing of GUIs/tutorials
    "Dummy_FE_chip_wafer": ("XW", "PG"),
    "Dummy_tutorial_FE_chip": ("XF", "PG"),
    "Dummy_sensor_wafer (with dummy tiles/test structures": ("XH", "PG"),
    "Dummy_tutorial_sensor_tile": ("XS", "PG"),
    "Dummy_sensor_test_structure": ("XT", "PG"),
    "Dummy_sensor_half_moon": ("XH", "PG"),
    "Dummy_single_bare_module": ("BT", "PG"),
    "Dummy_quad_bare_module": ("BR", "PG"),
    "Dummy_tutorial_bare_module": ("XB", "PG"),
    "Dummy_bare_module_gel_pack": ("XG", "PG"),
    "Dummy_tutorial_PCB": ("XP", "PG"),
    "Dummy_PCB_test_coupon": ("XD", "PG"),
    "Dummy_OB_wirebond_protection_roof": ("XE", "PB"),
    "Dummy_tutorial_module": ("XM", "PG"),
    "Dummy_module_carrier": ("XC", "PG"),
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
    # dummy local supports
    "Dummy_IS_capillary": ("YA", "PI"),
    "Dummy_IS_end_tube": ("YB", "PI"),
    "Dummy_IS_cooling_tube": ("YD", "PI"),
    "Dummy_IS_bare_local_support_stave": ("YE", "PI"),
    "Dummy_IS_bare_local_support_ring": ("YF", "PI"),
    "Dummy_IS_ring_local_support_assembly_loaded_ring": ("YG", "PI"),
    "Dummy_IS_barrel_stave_assembly_loaded_stave": ("YH", "PI"),
    "Dummy_OB_Base_Block": ("ZA", "PB"),
    "Dummy_OB_Cooling_Block": ("ZB", "PB"),
    "Dummy_OB_TPG_Tile": ("ZC", "PB"),
    "Dummy_OB_Local_Support_Inserts": ("ZD", "PB"),
    "Dummy_OB_Gusset": ("ZE", "PB"),
    "Dummy_OB_Truss": ("ZF", "PB"),
    "Dummy_OB_Half_Ring_Shell": ("ZG", "PB"),
    "Dummy_OB_End_of_longeron_Bracket_End_Gusset": ("ZH", "PB"),
    "Dummy_OB_Pipe_Support": ("ZI", "PB"),
    "Dummy_OB_Evaporator_Sleeves": ("ZJ", "PB"),
    "Dummy_OB_Cooling_Pipe_IHR": ("ZK", "PB"),
    "Dummy_OB_Cooling_Pipe_Longeron": ("ZL", "PB"),
    "Dummy_OB_Functional_Pipe_for_IHR": ("ZM", "PB"),
    "Dummy_OB_Functional_Pipe_for_Longeron": ("ZN", "PB"),
    "Dummy_OB_End_of_longeron_Support": ("ZO", "PB"),
    "Dummy_OB_Bare_Module_Cell": ("ZP", "PB"),
    "Dummy_OB_Functional_IHR": ("ZQ", "PB"),
    "Dummy_OB_Functional_Longeron": ("ZR", "PB"),
    "Dummy_OB_Loaded_Module_Cell": ("ZS", "PB"),
    "Dummy_OB_Loaded_IHR": ("ZT", "PB"),
    "Dummy_OB_Loaded_Longeron": ("ZU", "PB"),
    "Dummy_OB_IHR_Handling_Frame": ("ZV", "PB"),
    "Dummy_OB_Longeron_Handling_Frame": ("ZW", "PB"),
    "Dummy_OB_Bare_Cell_Transport_Box": ("ZX", "PB"),
    "Dummy_OEC_Trapezoids": ("YI", "PE"),
    "Dummy_OEC_Electrical break": ("YJ", "PE"),
    "Dummy_OEC_Inner_Rim_Insert": ("YK", "PE"),
    "Dummy_OEC_Outer_Rim_mounting_lugs": ("YL", "PE"),
    "Dummy_OEC_Inner_Rim_Closeout": ("YM", "PE"),
    "Dummy_OEC_Outer_Rim_Closeout": ("YN", "PE"),
    "Dummy_OEC_Pipe_Closeout_support_closeout": ("YO", "PE"),
    "Dummy_OEC_Half_Sandwich": ("YP", "PE"),
    "Dummy_OEC_Evaporator": ("YQ", "PE"),
    "Dummy_OEC_Bare_half_ring_assembly_Bare_support": ("YR", "PE"),
    "Dummy_OEC_Loaded_local_support_loaded_support": ("YS", "PE"),
    "Dummy_OEC_Handling_frame_support_frame": ("YT", "PE"),
    "Dummy_OEC_Transport/storage_box_support_box": ("YU", "PE"),
    "Dummy_Local_support_handling_frame_box": ("YV", "PE", "PI", "PB"),
    "Dummy_High_voltage_group": ("YW", "PE", "PI", "PB"),
    "Dummy_Serial_powering_scheme": ("YX", "PE", "PI", "PB"),
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
    "LpGBT_chip": ("OL", "PG"),
    "GBCR_chip": ("OG", "PG"),
    "Vtrx_module": ("OV", "PG"),
    "Bpol2V5_chip": ("O5", "PG"),
    "Bpol2V5_carrier_board": ("OK", "PG"),
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
    "PP0": ("0P", "PI"),  # FIXME: conflict with Triplet_L0_R0_PC
    "Finger": ("FI", "PI"),
    "Data_link ": ("D1", "PI", "PB", "PE"),
    "Power_DCS_line": ("P1", "PI", "PB", "PE"),
    "Environmental_link": ("E1", "PI", "PB", "PE"),
    "PP1_connector": ("1P", "PI", "PB", "PE"),
    "PP1_connector_pieces_segments": ("CS", "PI", "PB", "PE"),
    "strain_relief": ("SR", "PB"),
    "Type_2_power_cable": ("P2", "PI", "PB", "PE"),
    "Type_2_optobox_cable": ("20", "PI", "PB", "PE"),
    "PP2_box": ("2P", "PG"),
    "Type_3_HV_cable": ("P3", "PI", "PB", "PE"),
    "Type_3_LV_cable": ("L3", "PI", "PB", "PE"),
    "MOPS_cable": ("M3", "PG"),
    "TiLock": ("TL", "PG"),
    "OPTO_MOPS": ("OM", "PG"),
    "PP3_power": ("3P", "PG"),
    # Dummy services
    "Dummy_Optoboard": ("Q1", "PG"),
    "Dummy_Optoboard_termination_board": ("Q2", "PG"),  # codespell:ignore
    "Dummy_Optobox": ("Q3", "PG"),
    "Dummy_Optobox_powerbox": ("Q4", "PG"),
    "Dummy_Optobox_connector_board": ("Q5", "PG"),
    "Dummy_Optobox_optical_fan_out": ("Q6", "PG"),
    "Dummy_Optopanel": ("Q7", "PG"),
    "Dummy_Optopanel_cooling_plate": ("Q8", "PG"),
    "Dummy_Optobox_powerboard": ("Q9", "PG"),
    # "Dummy_LpGBT_chip": ("", "PG"), # FIXME: missing dummy
    "Dummy_GBCR_chip": ("QA", "PG"),
    "Dummy_Vtrx_module": ("QB", "PG"),
    "Dummy_Bpol2V5_chip": ("QC", "PG"),
    "Dummy_Bpol2V5_carrier_board": ("QD", "PG"),
    "Dummy_Bpol12V_chip": ("QE", "PG"),
    "Dummy_MOPS_chip": ("QF", "PG"),
    "Dummy_Power_cables": ("QG", "PG"),
    "Dummy_CAN_bus_cable": ("QH", "PG"),
    "Dummy_Pigtail": ("QI", "PB"),
    "Dummy_Rigid_flex": ("QK", "PI", "PB"),  # FIXME: "QJ" skipped
    "Dummy_Data_PP0": ("QL", "PI", "PE"),  # FIXME: typo in table 3
    "Dummy_Power_pigtail": ("QM", "PI", "PE"),
    "Dummy_Power_bustape": ("QN", "PI", "PB", "PE"),
    # "Dummy_Bare_bustape": ("", "PE"), # FIXME: missing dummy
    "Dummy_Pigtail_panel": ("QO", "PB"),
    "Dummy_PP0": ("QP", "PI"),
    "Dummy_Finger": ("QV", "PI"),
    "Dummy_Data_link ": ("QQ", "PI", "PB", "PE"),
    "Dummy_Power_DCS_line": ("QR", "PI", "PB", "PE"),
    "Dummy_Environmental_link": ("QS", "PI", "PB", "PE"),
    "Dummy_PP1_connector": ("QT", "PI", "PB", "PE"),
    "Dummy_PP1_connector_pieces_segments": ("QU", "PI", "PB", "PE"),
    # "Dummy_strain_relief": ("", "PB"), # FIXME: missing dummy
    "Dummy_Type_2_power_cable": ("QW", "PI", "PB", "PE"),
    "Dummy_Type_2_optobox_cable": ("QX", "PI", "PB", "PE"),
    "Dummy_PP2_box": ("QY", "PG"),
    "Dummy_Type_3_HV_cable": ("QZ", "PI", "PB", "PE"),
    "Dummy_Type_3_LV_cable": ("Q1", "PI", "PB", "PE"),
    "Dummy_MOPS_cable": ("Q2", "PG"),
    "Dummy_TiLock": ("Q3", "PG"),
    "Dummy_OPTO_MOPS": ("Q4", "PG"),
    "Dummy_PP3_power": ("Q5", "PG"),
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
        "FourInch_bare_module_gel_pack": Error,
        "SixInch_bare_module_gel_pack": Error,
        "Triplet_L0_Stave_PCB": pcb_triplets,
        "Triplet_L0_R0_PCB": pcb_triplets,
        "Triplet_L0_R0p5_PCB": pcb_triplets,
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
        # dummy for testing of GUIs/tutorials
        "Dummy_FE_chip_wafer": fe_chip,
        "Dummy_tutorial_FE_chip": fe_chip,
        "Dummy_sensor_wafer": sensor,
        "Dummy_tutorial_sensor_tile": sensor,
        "Dummy_sensor_test_structure": sensor,
        "Dummy_sensor_half_moon": sensor,
        "Dummy_single_bare_module": bare_module,
        "Dummy_quad_bare_module": bare_module,
        "Dummy_tutorial_bare_module": bare_module,
        "Dummy_bare_module_gel_pack": Error,
        "Dummy_tutorial_PCB": pcb,
        "Dummy_PCB_test_coupon": pcb,
        "Dummy_OB_wirebond_protection_roof": Error,
        "Dummy_tutorial_module": module,
        "Dummy_module_carrier": module_carrier,
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
        # dummy local supports
        "Dummy_IS_capillary": local_supports_is,
        "Dummy_IS_end_tube": local_supports_is,
        "Dummy_IS_cooling_tube": local_supports_is,
        "Dummy_IS_bare_local_support_stave": local_supports_is,
        "Dummy_IS_bare_local_support_ring": local_supports_is,
        "Dummy_IS_ring_local_support_assembly_loaded_ring": local_supports,
        "Dummy_IS_barrel_stave_assembly_loaded_stave": local_supports,
        "Dummy_OB_Base_Block": local_supports,
        "Dummy_OB_Cooling_Block": local_supports,
        "Dummy_OB_TPG_Tile": local_supports,
        "Dummy_OB_Local_Support_Inserts": local_supports,
        "Dummy_OB_Gusset": local_supports,
        "Dummy_OB_Truss": local_supports,
        "Dummy_OB_Half_Ring_Shell": local_supports,
        "Dummy_OB_End_of_longeron_Bracket_End_Gusset": local_supports,
        "Dummy_OB_Pipe_Support": local_supports,
        "Dummy_OB_Evaporator_Sleeves": local_supports,
        "Dummy_OB_Cooling_Pipe_IHR": local_supports,
        "Dummy_OB_Cooling_Pipe_Longeron": local_supports,
        "Dummy_OB_Functional_Pipe_for_IHR": local_supports,
        "Dummy_OB_Functional_Pipe_for_Longeron": local_supports,
        "Dummy_OB_End_of_longeron_Support": local_supports,
        "Dummy_OB_Bare_Module_Cell": local_supports,
        "Dummy_OB_Functional_IHR": local_supports_ihr,
        "Dummy_OB_Functional_Longeron": local_supports_longeron,
        "Dummy_OB_Loaded_Module_Cell": loaded_local_supports_ob_module,
        "Dummy_OB_Loaded_IHR": local_supports,
        "Dummy_OB_Loaded_Longeron": local_supports,
        "Dummy_OB_IHR_Handling_Frame": local_supports,
        "Dummy_OB_Longeron_Handling_Frame": local_supports,
        "Dummy_OB_Bare_Cell_Transport_Box": local_supports,
        "Dummy_OEC_Trapezoids": local_supports,
        "Dummy_OEC_Electrical break": local_supports,
        "Dummy_OEC_Inner_Rim_Insert": local_supports,
        "Dummy_OEC_Outer_Rim_mounting_lugs": local_supports,
        "Dummy_OEC_Inner_Rim_Closeout": local_supports,
        "Dummy_OEC_Outer_Rim_Closeout": local_supports,
        "Dummy_OEC_Pipe_Closeout_support_closeout": local_supports,
        "Dummy_OEC_Half_Sandwich": local_supports,
        "Dummy_OEC_Evaporator": local_supports,
        "Dummy_OEC_Bare_half_ring_assembly_Bare_support": local_supports,
        "Dummy_OEC_Loaded_local_support_loaded_support": local_supports,
        "Dummy_OEC_Handling_frame_support_frame": local_supports,
        "Dummy_OEC_Transport/storage_box_support_box": local_supports,
        "Dummy_Local_support_handling_frame_box": local_supports_frame_box,
        "Dummy_High_voltage_group": local_supports,
        "Dummy_Serial_powering_scheme": local_supports,
        # services
        "Optoboard": optoboard,
        "Optoboard_termination_board": termination_board,  # OB Type-1 Termination Board (FIXME: only PG, no PB)
        "Optobox": optobox,
        "Optobox_powerbox": optobox,
        "Optobox_connector_board": optobox_powerboard_connector,
        "Optobox_optical_fan_out": optobox,
        "Optopanel": Error,  # FIXME
        "Optopanel_cooling_plate": Error,  # FIXME
        "Optobox_powerboard": optobox_powerboard_connector,
        "LpGBT_chip": Error,  # FIXME
        "GBCR_chip": Error,  # FIXME
        "Vtrx_module": Error,  # FIXME
        "Bpol2V5_chip": Error,  # FIXME
        "Bpol2V5_carrier_board": Error,  # FIXME
        "Bpol12V_chip": Error,  # FIXME
        "MOPS_chip": mops_chip,  # FIXME: phrasing in the document is awful
        "Power_cables": Error,  # FIXME
        "CAN_bus_cable": canbus,
        # Type-0 and Type-1 cables below
        "Pigtail": subproject_switch(
            pb=pb_type0_cable
        ),  # IS Type-0  (FIXME: no PI supported)
        "Rigid_flex": subproject_switch(pb=pb_type0_pp0),  # IS Type-0
        "Data_PP0": subproject_switch(
            pe=pe_type0_data
        ),  # IS Type-0  # OB Type-1 Inclined PCB??? (FIXME: not PB)
        "Power_pigtail": subproject_switch(pe=pe_type0_power),  # IS Type-0  # OE Type-0
        "Power_bustape": subproject_switch(
            pe=pe_type0_power
        ),  # FIXME: only PE needed, not PI/PB
        "Bare_bustape": Error,  # FIXME: not used?
        "Pigtail_panel": pb_type0_cable,
        "PP0": subproject_switch(pi=pi_type0_pp0),  # IS only
        "Finger": Error,  # FIXME: not used/defined?
        "Data_link ": subproject_switch(
            pb=pb_type1_data
        ),  # IS Type-1, (FIXME: only PB/PI needed, not PE)
        "Power_DCS_line": subproject_switch(
            pe=pe_type1,
            pb=pb_type1_power,
            pi=is_cable,
        ),  # IS Type-1, (FIXME: only PB/PI needed, not PE)
        "Environmental_link": Error,  # Type-0 and Type-1 cable (FIXME: not defined?)
        "PP1_connector": subproject_switch(pe=pe_type1),  # FIXME: not defined well)
        "PP1_connector_pieces_segments": subproject_switch(),  # FIXME: not defined well)
        # End Type-0 and Type-1
        "Strain_relief": Error,
        "Type_2_power_cable": type2,
        "Type_2_optobox_cable": type2,
        "PP2_box": type2,
        "Type_3_HV_cable": type3,
        "Type_3_LV_cable": type3,
        "MOPS_cable": type3,
        "TiLock": type3,
        "OPTO_MOPS": type3,
        "PP3_power": type4,
        # Dummy services
        "Dummy_Optoboard": optoboard,
        "Dummy_Optoboard_termination_board": termination_board,
        "Dummy_Optobox": optobox,
        "Dummy_Optobox_powerbox": optobox,
        "Dummy_Optobox_connector_board": optobox_powerboard_connector,
        "Dummy_Optobox_optical_fan_out": optobox,
        "Dummy_Optopanel": Error,
        "Dummy_Optopanel_cooling_plate": Error,
        "Dummy_Optobox_powerboard": optobox_powerboard_connector,
        "Dummy_GBCR_chip": Error,
        "Dummy_Vtrx_module": Error,
        "Dummy_Bpol2V5_chip": Error,
        "Dummy_Bpol2V5_carrier_board": Error,
        "Dummy_Bpol12V_chip": Error,
        "Dummy_MOPS_chip": mops_chip,
        "Dummy_Power_cables": Error,
        "Dummy_CAN_bus_cable": canbus,
        "Dummy_Pigtail": subproject_switch(pb=pb_type0_cable),  # IS Type-0
        "Dummy_Rigid_flex": subproject_switch(pb=pb_type0_pp0),  # IS Type-0
        "Dummy_Data_PP0": subproject_switch(
            pe=pe_type0_data
        ),  # IS Type-0  # OB Type-1 Inclined PCB???
        "Dummy_Power_pigtail": subproject_switch(
            pe=pe_type0_power
        ),  # IS Type-0  # OE Type-0
        "Dummy_Power_bustape": subproject_switch(pe=pe_type0_power),
        "Dummy_Pigtail_panel": pb_type0_cable,
        "Dummy_PP0": subproject_switch(pi=pi_type0_pp0),  # IS only
        "Dummy_Finger": Error,
        "Dummy_Data_link ": subproject_switch(pb=pb_type1_data),  # IS Type-1,
        "Dummy_Power_DCS_line": subproject_switch(
            pe=pe_type1, pb=pb_type1_power, pi=is_cable
        ),  # IS Type-1,
        "Dummy_Environmental_link": Error,
        "Dummy_PP1_connector": subproject_switch(pe=pe_type1),
        "Dummy_PP1_connector_pieces_segments": subproject_switch(),
        "Dummy_Type_2_power_cable": type2,
        "Dummy_Type_2_optobox_cable": type2,
        "Dummy_PP2_box": type2,
        "Dummy_Type_3_HV_cable": type3,
        "Dummy_Type_3_LV_cable": type3,
        "Dummy_MOPS_cable": type3,
        "Dummy_TiLock": type3,
        "Dummy_OPTO_MOPS": type3,
        "Dummy_PP3_power": type4,
    },
    # default=Bytes(7),
)
