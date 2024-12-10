from __future__ import annotations

from construct import (
    Bytes,
    Computed,
    Const,
    Pointer,
    Select,
    Struct,
    Switch,
)

from itksn.common import EnumStr

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

type0_component: dict[str, dict[tuple[str, str], str]] = {
    "Data_PP0": {  # "DP"
        ("Barrel_Triplet", "NA"): "L0 Barrel Data Flex",
        ("Barrel_Quad", "F1"): "L1 Barrel Data Flex",
        ("Barrel_Quad", "F2"): "L1 Barrel Data Flex",
        ("Barrel_Quad", "F3"): "L1 Barrel Data Flex",
        ("Barrel_Quad", "F4"): "L1 Barrel Data Flex",
        ("Ring0_Triplet", "F1"): "R0 Data Flex",
        ("Ring0_Triplet", "F2"): "R0 Data Flex",
        ("Ring0_Triplet", "F3"): "R0 Data Flex",
        ("Ring05_Triplet", "F1"): "R0.5 Data Flex",
        ("Ring05_Triplet", "F2"): "R0.5 Data Flex",
    },
    "Power_pigtail": {  # "PP"
        ("Barrel_Triplet", "NA"): "L0 Barrel Power Flex",
        ("Barrel_Quad", "F1"): "L1 Barrel Power Flex",
        ("Barrel_Quad", "F2"): "L1 Barrel Power Flex",
        ("Ring0_Triplet", "NA"): "R0 Power",
        ("Ring0_Triplet", "F1"): "R0 Power Jumper",
    },
    "Rigid_flex": {  # "RF"
        ("Ring_Both", "NA"): "Coupled Ring R0/R1",
        ("Ring_Quad", "NA"): "Quad Ring R1",
        ("Ring0_Triplet", "NA"): "Intermediate Ring",
    },
    "Pigtail": {  # "PG"
        ("Ring_Quad", "NA"): "Quad Module Z-Ray Flex",
        ("Ring_Both", "F1"): "Type-0 to PP0",
        ("Ring_Both", "F2"): "Type-0 to PP0",
    },
}

is_type0_cable = Struct(
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
        Ring0_Triplet=b"2",
        Ring_Quad=b"3",
        Ring_Both=b"4",
        Ring05_Triplet=b"5",
    ),
    "subflavor"
    / EnumStr(
        Bytes(1),
        NA=b"0",
        F1=b"1",
        F2=b"2",
        F3=b"3",
        F4=b"4",
        F5=b"5",
        F6=b"6",
    ),
    "component"
    / Computed(
        lambda ctx: type0_component[ctx._.component_code][(ctx.flavor, ctx.subflavor)],  # type: ignore[arg-type,return-value]
    ),
    "number" / Bytes(4),
)

type1_production_version = EnumStr(
    Bytes(1),
    Prototype=b"0",
    Pre_production=b"1",
    Production=b"2",
    Dummy=b"9",
)

is_type1_cable = Struct(
    "production_version" / type1_production_version,
    "flavor"
    / EnumStr(
        Bytes(1),
        L0L1=b"0",
        L02xL1=b"1",
        Coupled_Ring=b"2",
        Intermediate_Ring=b"3",
        QR1=b"4",
        QR2=b"5",
    ),
    "number" / Bytes(5),
)

pp1 = Struct(
    "production_version" / type1_production_version,
    "glenair_part"
    / EnumStr(
        Bytes(1),
        Type_2_Header=b"0",
        Type_1_Receptacle=b"1",
        Strain_Arm=b"3",
        Filter_Plug=b"9",
    ),
    "flavor"
    / EnumStr(
        Bytes(1),
        N=b"0",
        A=b"1",
        B=b"2",
        C=b"3",
        D=b"4",
        E=b"5",
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

yy_identifiers = {
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
    "Pigtail": ("PG", "PI", "PB"),
    "Rigid_flex": ("RF", "PI", "PB"),
    "Data_PP0": ("DP", "PI", "PE"),
    "Power_pigtail": ("PP", "PI", "PE"),
    "Power_bustape": ("PB", "PI", "PB", "PE"),
    "Bare_bustape": ("NB", "PE"),
    "Pigtail_panel": ("PL", "PB"),
    "PP0": ("0P", "PI"),  # FIXME: conflict with Triplet_L0_R0_PC
    "Finger": ("FI", "PI"),
    "Type_1_Data_link ": ("D1", "PI", "PB", "PE"),
    "Type_1_Power_DCS_line": ("P1", "PI", "PB", "PE"),
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
    "Dummy_Type_1_Data_link ": ("QQ", "PI", "PB", "PE"),
    "Dummy_Type_1_Power_DCS_line": ("QR", "PI", "PB", "PE"),
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
