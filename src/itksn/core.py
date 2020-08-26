from construct import Enum, Struct, Bytes

SerialNumberStruct = "SerialNumber" / Struct(
    "atlas_project" / Enum(Bytes(2), atlas_detector=b"20"),
    "system_code" / Enum(Bytes(1), phaseII_upgrade=b"U",),
    "project_code" / Bytes(2),
    "subproject_code" / Bytes(2),
    "identifier" / Bytes(7),
)
"""
from construct import Switch

SerialNumberStruct = "SerialNumber" / Struct(
    "atlas_project" / Enum(Bytes(2),
        atlas_detector = b"20"
    ),
    "system_code" / Enum(Bytes(1),
        phaseII_upgrade = b"U",
    ),
    "project_code" / Enum(Bytes(2),
        inner_pixel = b"PI",
        outer_pixel_barrel = b"PB",
        pixel_general = b"PG",
        pixel_endcaps = b"PE",
        strip_general = b"SG",
        strip_barrel = b"SB",
        strip_endcaps = b"SE",
        common_mechanics = b"CM",
        common_electronics = b"CE"
    ),
    "subproject_code" / Bytes(2),
    "identifier" / Bytes(7)
)
"""
