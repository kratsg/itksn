from __future__ import annotations

from construct import (
    Bytes,
    Error,
    Switch,
)

from itksn.common import EnumStr
from itksn.pixels import local_supports, modules, services, utils

yy_identifiers = {
    **modules.yy_identifiers,
    **services.yy_identifiers,
    **local_supports.yy_identifiers,
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
        "FE_chip_wafer": modules.fe_chip,
        "FE_chip": modules.fe_chip,
        "Planar_sensor_wafer_100um_thickness": modules.sensor,
        "Planar_sensor_wafer_150um_thickness": modules.sensor,
        "ThreeD_sensor_wafer": modules.sensor,
        "L0_inner_pixel_3D_sensor_wafer_25x100um": modules.sensor,
        "L0_inner_pixel_3D_sensor_wafer_50x50um": modules.sensor,
        "L1_inner_pixel_sensor_wafer_100um_thickness": modules.sensor,
        "Outer_pixel_sensor_wafer_150um_thickness": modules.sensor,
        "Half_size_planar_sensor_tile_100um_thickness": modules.sensor,
        "Half_size_planar_sensor_tile_150um_thickness": modules.sensor,
        "Full_size_planar_sensor_tile_100um_thickness": modules.sensor,
        "Full_size_planar_sensor_tile_150um_thickness": modules.sensor,
        "Half_size_3D_sensor_tile_25x100um": modules.sensor,
        "Full_size_3D_sensor_tile_25x100um": modules.sensor,
        "Half_size_3D_sensor_tile_50x50um": modules.sensor,
        "Full_size_3D_sensor_tile_50x50um": modules.sensor,
        "L0_inner_pixel_3D_sensor_tile_25x100um": modules.sensor,
        "L0_inner_pixel_3D_sensor_tile_50x50um": modules.sensor,
        "L1_inner_pixel_quad_sensor_tile": modules.sensor,
        "Outer_pixel_quad_sensor_tile": modules.sensor,
        "Planar_Sensor_test_structure_100um_thickness": modules.sensor,
        "Planar_Sensor_test_structure_150um_thickness": modules.sensor,
        "ThreeD_Sensor_test_structure_25x100um": modules.sensor,
        "ThreeD_Sensor_test_structure_50x50um": modules.sensor,
        "Planar_Sensor_half_moon_100um_thickness": modules.sensor,
        "Planar_Sensor_half_moon_150um_thickness": modules.sensor,
        "ThreeD_Sensor_half_moon_25x100um": modules.sensor,
        "ThreeD_Sensor_half_moon_50x50um": modules.sensor,
        "Single_bare_module": modules.bare_module,
        "Dual_bare_module": modules.bare_module,
        "Quad_bare_module": modules.bare_module,
        "Digital_single_bare_module": modules.bare_module,
        "Digital_quad_bare_module": modules.bare_module,
        "FourInch_bare_module_gel_pack": Error,
        "SixInch_bare_module_gel_pack": Error,
        "Triplet_L0_Stave_PCB": modules.pcb_triplets,
        "Triplet_L0_R0_PCB": modules.pcb_triplets,
        "Triplet_L0_R0p5_PCB": modules.pcb_triplets,
        "Quad_PCB": modules.pcb,
        "Dual_PCB": modules.pcb,
        "PCB_test_coupon": modules.pcb,
        "OB_wirebond_protection_roof": Error,
        "Triplet_L0_stave_module": modules.triplet_module,
        "Triplet_L0_Ring0_module": modules.triplet_module,
        "Triplet_L0_Ring0p5_module": modules.triplet_module,
        "L1_quad_module": modules.module,
        "Outer_system_quad_module": modules.module,
        "Dual_chip_module": modules.module,
        "Single_chip_module": modules.module,
        "Digital_triplet_L0_stave_module": modules.triplet_module,
        "Digital_triplet_L0_ring0_module": modules.triplet_module,
        "Digital_triplet_L0_ring0p5_module": modules.triplet_module,
        "Digital_quad_module": modules.module,
        "Digital_L1_quad_module": modules.module,
        "Dummy_triplet_L0_stave_module": modules.triplet_module,
        "Dummy_triplet_L0_ring0_module": modules.triplet_module,
        "Dummy_triplet_L0_ring0p5_module": modules.triplet_module,
        "Dummy_quad_module": modules.module,
        "Dummy_L1_quad_module": modules.module,
        "Module_carrier": modules.module_carrier,
        # dummy for testing of GUIs/tutorials
        "Dummy_FE_chip_wafer": modules.fe_chip,
        "Dummy_tutorial_FE_chip": modules.fe_chip,
        "Dummy_sensor_wafer": modules.sensor,
        "Dummy_tutorial_sensor_tile": modules.sensor,
        "Dummy_sensor_test_structure": modules.sensor,
        "Dummy_sensor_half_moon": modules.sensor,
        "Dummy_single_bare_module": modules.bare_module,
        "Dummy_quad_bare_module": modules.bare_module,
        "Dummy_tutorial_bare_module": modules.bare_module,
        "Dummy_bare_module_gel_pack": Error,
        "Dummy_tutorial_PCB": modules.pcb,
        "Dummy_PCB_test_coupon": modules.pcb,
        "Dummy_OB_wirebond_protection_roof": Error,
        "Dummy_tutorial_module": modules.module,
        "Dummy_module_carrier": modules.module_carrier,
        # local supports
        "IS_capillary": local_supports.local_supports_is,
        "IS_end_tube": local_supports.local_supports_is,
        "IS_cooling_tube": local_supports.local_supports_is,
        "IS_bare_local_support_stave": local_supports.local_supports_is,
        "IS_bare_local_support_ring": local_supports.local_supports_is,
        "IS_ring_local_support_assembly_loaded_ring": local_supports.local_supports,
        "IS_barrel_stave_assembly_loaded_stave": local_supports.local_supports,
        "OB_Base_Block": local_supports.local_supports,
        "OB_Cooling_Block": local_supports.local_supports,
        "OB_TPG_Tile": local_supports.local_supports,
        "OB_Local_Support_Inserts": local_supports.local_supports,
        "OB_Gusset": local_supports.local_supports,
        "OB_Truss": local_supports.local_supports,
        "OB_Half_Ring_Shell": local_supports.local_supports,
        "OB_End_of_longeron_Bracket_End_Gusset": local_supports.local_supports,
        "OB_Pipe_Support": local_supports.local_supports,
        "OB_Evaporator_Sleeves": local_supports.local_supports,
        "OB_Cooling_Pipe_IHR": local_supports.local_supports,
        "OB_Cooling_Pipe_Longeron": local_supports.local_supports,
        "OB_Functional_Pipe_for_IHR": local_supports.local_supports,
        "OB_Functional_Pipe_for_Longeron": local_supports.local_supports,
        "OB_End_of_longeron_Support": local_supports.local_supports,
        "OB_Bare_Module_Cell": local_supports.local_supports,
        "OB_Functional_IHR": local_supports.local_supports_ihr,
        "OB_Functional_Longeron": local_supports.local_supports_longeron,
        "OB_Loaded_Module_Cell": local_supports.loaded_local_supports_ob_module,
        "OB_Loaded_IHR": local_supports.local_supports,
        "OB_Loaded_Longeron": local_supports.local_supports,
        "OB_IHR_Handling_Frame": local_supports.local_supports,
        "OB_Longeron_Handling_Frame": local_supports.local_supports,
        "OB_Bare_Cell_Transport_Box": local_supports.local_supports,
        "OEC_Trapezoids": local_supports.local_supports,
        "OEC_Electrical break": local_supports.local_supports,
        "OEC_Inner_Rim_Insert": local_supports.local_supports,
        "OEC_Outer_Rim_mounting_lugs": local_supports.local_supports,
        "OEC_Inner_Rim_Closeout": local_supports.local_supports,
        "OEC_Outer_Rim_Closeout": local_supports.local_supports,
        "OEC_Pipe_Closeout_support_closeout": local_supports.local_supports,
        "OEC_Half_Sandwich": local_supports.local_supports,
        "OEC_Evaporator": local_supports.local_supports,
        "OEC_Bare_half_ring_assembly_Bare_support": local_supports.local_supports,
        "OEC_Loaded_local_support_loaded_support": local_supports.local_supports,
        "OEC_Handling_frame_support_frame": local_supports.local_supports,
        "OEC_Transport/storage_box_support_box": local_supports.local_supports,
        "Local_support_handling_frame_box": local_supports.local_supports_frame_box,
        "High_voltage_group": local_supports.local_supports,
        "Serial_powering_scheme": local_supports.local_supports,
        # dummy local supports
        "Dummy_IS_capillary": local_supports.local_supports_is,
        "Dummy_IS_end_tube": local_supports.local_supports_is,
        "Dummy_IS_cooling_tube": local_supports.local_supports_is,
        "Dummy_IS_bare_local_support_stave": local_supports.local_supports_is,
        "Dummy_IS_bare_local_support_ring": local_supports.local_supports_is,
        "Dummy_IS_ring_local_support_assembly_loaded_ring": local_supports.local_supports,
        "Dummy_IS_barrel_stave_assembly_loaded_stave": local_supports.local_supports,
        "Dummy_OB_Base_Block": local_supports.local_supports,
        "Dummy_OB_Cooling_Block": local_supports.local_supports,
        "Dummy_OB_TPG_Tile": local_supports.local_supports,
        "Dummy_OB_Local_Support_Inserts": local_supports.local_supports,
        "Dummy_OB_Gusset": local_supports.local_supports,
        "Dummy_OB_Truss": local_supports.local_supports,
        "Dummy_OB_Half_Ring_Shell": local_supports.local_supports,
        "Dummy_OB_End_of_longeron_Bracket_End_Gusset": local_supports.local_supports,
        "Dummy_OB_Pipe_Support": local_supports.local_supports,
        "Dummy_OB_Evaporator_Sleeves": local_supports.local_supports,
        "Dummy_OB_Cooling_Pipe_IHR": local_supports.local_supports,
        "Dummy_OB_Cooling_Pipe_Longeron": local_supports.local_supports,
        "Dummy_OB_Functional_Pipe_for_IHR": local_supports.local_supports,
        "Dummy_OB_Functional_Pipe_for_Longeron": local_supports.local_supports,
        "Dummy_OB_End_of_longeron_Support": local_supports.local_supports,
        "Dummy_OB_Bare_Module_Cell": local_supports.local_supports,
        "Dummy_OB_Functional_IHR": local_supports.local_supports_ihr,
        "Dummy_OB_Functional_Longeron": local_supports.local_supports_longeron,
        "Dummy_OB_Loaded_Module_Cell": local_supports.loaded_local_supports_ob_module,
        "Dummy_OB_Loaded_IHR": local_supports.local_supports,
        "Dummy_OB_Loaded_Longeron": local_supports.local_supports,
        "Dummy_OB_IHR_Handling_Frame": local_supports.local_supports,
        "Dummy_OB_Longeron_Handling_Frame": local_supports.local_supports,
        "Dummy_OB_Bare_Cell_Transport_Box": local_supports.local_supports,
        "Dummy_OEC_Trapezoids": local_supports.local_supports,
        "Dummy_OEC_Electrical break": local_supports.local_supports,
        "Dummy_OEC_Inner_Rim_Insert": local_supports.local_supports,
        "Dummy_OEC_Outer_Rim_mounting_lugs": local_supports.local_supports,
        "Dummy_OEC_Inner_Rim_Closeout": local_supports.local_supports,
        "Dummy_OEC_Outer_Rim_Closeout": local_supports.local_supports,
        "Dummy_OEC_Pipe_Closeout_support_closeout": local_supports.local_supports,
        "Dummy_OEC_Half_Sandwich": local_supports.local_supports,
        "Dummy_OEC_Evaporator": local_supports.local_supports,
        "Dummy_OEC_Bare_half_ring_assembly_Bare_support": local_supports.local_supports,
        "Dummy_OEC_Loaded_local_support_loaded_support": local_supports.local_supports,
        "Dummy_OEC_Handling_frame_support_frame": local_supports.local_supports,
        "Dummy_OEC_Transport/storage_box_support_box": local_supports.local_supports,
        "Dummy_Local_support_handling_frame_box": local_supports.local_supports_frame_box,
        "Dummy_High_voltage_group": local_supports.local_supports,
        "Dummy_Serial_powering_scheme": local_supports.local_supports,
        # services
        "Optoboard": services.optoboard,
        "Optoboard_termination_board": services.termination_board,  # OB Type-1 Termination Board (FIXME: only PG, no PB)
        "Optobox": services.optobox,
        "Optobox_powerbox": services.optobox,
        "Optobox_connector_board": services.optobox_powerboard_connector,
        "Optobox_optical_fan_out": services.optobox,
        "Optopanel": Error,  # FIXME
        "Optopanel_cooling_plate": Error,  # FIXME
        "Optobox_powerboard": services.optobox_powerboard_connector,
        "LpGBT_chip": Error,  # FIXME
        "GBCR_chip": Error,  # FIXME
        "Vtrx_module": Error,  # FIXME
        "Bpol2V5_chip": Error,  # FIXME
        "Bpol2V5_carrier_board": Error,  # FIXME
        "Bpol12V_chip": Error,  # FIXME
        "MOPS_chip": services.mops_chip,  # FIXME: phrasing in the document is awful
        "Power_cables": Error,  # FIXME
        "CAN_bus_cable": services.canbus,
        # Type-0 and Type-1 cables below
        "Pigtail": utils.subproject_switch(
            pi=services.is_type0_cable, pb=services.pb_type0_cable
        ),  # IS Type-0  (FIXME: no PI supported)
        "Rigid_flex": utils.subproject_switch(
            pi=services.is_type0_cable, pb=services.pb_type0_pp0
        ),  # IS Type-0
        "Data_PP0": utils.subproject_switch(
            pi=services.is_type0_cable, pe=services.pe_type0_data
        ),  # IS Type-0  # OB Type-1 Inclined PCB??? (FIXME: not PB)
        "Power_pigtail": utils.subproject_switch(
            pi=services.is_type0_cable, pe=services.pe_type0_power
        ),  # IS Type-0  # OE Type-0
        "Power_bustape": utils.subproject_switch(
            pe=services.pe_type0_power
        ),  # FIXME: only PE needed, not PI/PB
        "Bare_bustape": Error,  # FIXME: not used?
        "Pigtail_panel": services.pb_type0_cable,
        "PP0": utils.subproject_switch(pi=services.pi_type0_pp0),  # IS only
        "Finger": Error,  # FIXME: not used/defined?
        "Type_1_Data_link ": utils.subproject_switch(
            pb=services.pb_type1_data
        ),  # IS Type-1, (FIXME: only PB/PI needed, not PE)
        "Type_1_Power_DCS_line": utils.subproject_switch(
            pe=services.pe_type1,
            pb=services.pb_type1_power,
            pi=services.is_type1_cable,
        ),  # IS Type-1, (FIXME: only PB/PI needed, not PE)
        "Environmental_link": Error,  # Type-0 and Type-1 cable (FIXME: not defined?)
        "PP1_connector": utils.subproject_switch(
            pi=services.pp1, pe=services.pe_type1
        ),  # FIXME: not defined well)
        "PP1_connector_pieces_segments": utils.subproject_switch(),  # FIXME: not defined well)
        # End Type-0 and Type-1
        "Strain_relief": Error,
        "Type_2_power_cable": services.type2,
        "Type_2_optobox_cable": services.type2,
        "PP2_box": services.type2,
        "Type_3_HV_cable": services.type3,
        "Type_3_LV_cable": services.type3,
        "MOPS_cable": services.type3,
        "TiLock": services.type3,
        "OPTO_MOPS": services.type3,
        "PP3_power": services.type4,
        # Dummy services
        "Dummy_Optoboard": services.optoboard,
        "Dummy_Optoboard_termination_board": services.termination_board,
        "Dummy_Optobox": services.optobox,
        "Dummy_Optobox_powerbox": services.optobox,
        "Dummy_Optobox_connector_board": services.optobox_powerboard_connector,
        "Dummy_Optobox_optical_fan_out": services.optobox,
        "Dummy_Optopanel": Error,
        "Dummy_Optopanel_cooling_plate": Error,
        "Dummy_Optobox_powerboard": services.optobox_powerboard_connector,
        "Dummy_GBCR_chip": Error,
        "Dummy_Vtrx_module": Error,
        "Dummy_Bpol2V5_chip": Error,
        "Dummy_Bpol2V5_carrier_board": Error,
        "Dummy_Bpol12V_chip": Error,
        "Dummy_MOPS_chip": services.mops_chip,
        "Dummy_Power_cables": Error,
        "Dummy_CAN_bus_cable": services.canbus,
        "Dummy_Pigtail": utils.subproject_switch(
            pi=services.is_type0_cable, pb=services.pb_type0_cable
        ),  # IS Type-0
        "Dummy_Rigid_flex": utils.subproject_switch(
            pi=services.is_type0_cable, pb=services.pb_type0_pp0
        ),  # IS Type-0
        "Dummy_Data_PP0": utils.subproject_switch(
            pi=services.is_type0_cable, pe=services.pe_type0_data
        ),  # IS Type-0  # OB Type-1 Inclined PCB???
        "Dummy_Power_pigtail": utils.subproject_switch(
            pi=services.is_type0_cable, pe=services.pe_type0_power
        ),  # IS Type-0  # OE Type-0
        "Dummy_Power_bustape": utils.subproject_switch(pe=services.pe_type0_power),
        "Dummy_Pigtail_panel": services.pb_type0_cable,
        "Dummy_PP0": utils.subproject_switch(pi=services.pi_type0_pp0),  # IS only
        "Dummy_Finger": Error,
        "Dummy_Type_1_Data_link ": utils.subproject_switch(
            pb=services.pb_type1_data
        ),  # IS Type-1,
        "Dummy_Type_1_Power_DCS_line": utils.subproject_switch(
            pe=services.pe_type1, pb=services.pb_type1_power, pi=services.is_type1_cable
        ),  # IS Type-1,
        "Dummy_Environmental_link": Error,
        "Dummy_PP1_connector": utils.subproject_switch(
            pi=services.pp1, pe=services.pe_type1
        ),
        "Dummy_PP1_connector_pieces_segments": utils.subproject_switch(),
        "Dummy_Type_2_power_cable": services.type2,
        "Dummy_Type_2_optobox_cable": services.type2,
        "Dummy_PP2_box": services.type2,
        "Dummy_Type_3_HV_cable": services.type3,
        "Dummy_Type_3_LV_cable": services.type3,
        "Dummy_MOPS_cable": services.type3,
        "Dummy_TiLock": services.type3,
        "Dummy_OPTO_MOPS": services.type3,
        "Dummy_PP3_power": services.type4,
    },
    # default=Bytes(7),
)

__all__ = ("identifiers",)
