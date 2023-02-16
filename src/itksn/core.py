from __future__ import annotations

from construct import (
    Bytes,
    PaddedString,
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
        default=PaddedString(2, "utf8"),
    ),
    "identifier"
    / Switch(
        this.project_code,
        {
            "inner_pixel": pixels.identifiers,
            "outer_pixel_barrel": pixels.identifiers,
            "pixel_general": pixels.identifiers,
        },
        default=Bytes(7),
    ),
    Terminated,
)
