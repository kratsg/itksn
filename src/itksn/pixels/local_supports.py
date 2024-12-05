from __future__ import annotations

from construct import (
    Bytes,
    Struct,
)

from itksn.common import EnumStr
from itksn.pixels.common import pcb_manufacturer

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

yy_identifiers = {
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
}
