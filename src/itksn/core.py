from __future__ import annotations

from construct import (
    Bytes,
    Struct,
    Switch,
    Terminated,
    this,
)

from itksn import pixels
from itksn.common import EnumStr

SerialNumberStruct = "SerialNumber" / Struct(
    "atlas_project" / EnumStr(Bytes(2), atlas_detector=b"20"),
    "system_code"
    / EnumStr(
        Bytes(1),
        phaseII_upgrade=b"U",
    ),
    "project_code"
    / EnumStr(
        Bytes(2),
        inner_pixel=b"PI",
        outer_pixel_barrel=b"PB",
        pixel_general=b"PG",
        pixel_endcaps=b"PE",
        strip_general=b"SG",
        strip_barrel=b"SB",
        strip_endcaps=b"SE",
        common_mechanics=b"CM",
        common_electronics=b"CE",
    ),
    "subproject_code"
    / Switch(
        this.project_code,
        {
            "inner_pixel": pixels.subproject_codes,
            "outer_pixel_barrel": pixels.subproject_codes,
            "pixel_general": pixels.subproject_codes,
        },
        default=Bytes(2),
    ),
    "identifier"
    / Switch(
        this.subproject_code,
        {
            "FE_chip_wafer": pixels.fe_chip_wafer,
            "Market_Survey_sensor_wafer": pixels.sensor,
            "L0_inner_pixel_3D_sensor_wafer": pixels.sensor,
            "L0_inner_pixel_planar_sensor_wafer": pixels.sensor,
            "L1_inner_pixel_sensor_wafer_thickness_100mum": pixels.sensor,
            "Outer_pixel_sensor_wafer_thickness_150mum": pixels.sensor,
            "Dummy_sensor_wafer": pixels.sensor,
            "Market_survey_sensor_tile": pixels.sensor,
            "L0_inner_pixel_3D_sensor_tile": pixels.sensor,
            "L0_inner_pixel_planar_sensor_tile": pixels.sensor,
            "L1_inner_pixel_quad_sensor_tile": pixels.sensor,
            "Outer_pixel_quad_sensor_tile": pixels.sensor,
            "Single_bare_module": pixels.bare_module,
            "Dual_bare_module": pixels.bare_module,
            "Quad_bare_module": pixels.bare_module,
            "Digital_single_bare_module": pixels.bare_module,
            "Digital_quad_bare_module": pixels.bare_module,
            "Dummy_single_bare_module": pixels.bare_module,
            "Dummy_quad_bare_module": pixels.bare_module,
            "Triplet_L0_Stave_PCB": pixels.pcb,
            "Triplet_L0_R0_PCB": pixels.pcb,
            "Triplet_L0_R0p5_PCB": pixels.pcb,
            "Quad_PCB": pixels.pcb,
            "Dual_PCB": pixels.pcb,
            "PCB_test_coupon": pixels.pcb,
            "Triplet_L0_stave_module": pixels.module,
            "Triplet_L0_Ring0_module": pixels.module,
            "Triplet_L0_Ring0p5_module": pixels.module,
            "L1_quad_module": pixels.module,
            "Outer_system_quad_module": pixels.module,
            "Dual_chip_module": pixels.module,
            "Digital_triplet_module": pixels.module,
            "Digital_quad_module": pixels.module,
            "Dummy_triplet_module": pixels.module,
            "Dummy_quad_module": pixels.module,
            "Module_carrier": pixels.module_carrier,
        },
        default=Bytes(7),
    ),
    Terminated,
)
