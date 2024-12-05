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
        Bytes(1),
        pixel=b"P",
        strip=b"S",
        common=b"C",
    ),
    "subproject_code"
    / Switch(
        lambda ctx: ctx.project_code,
        {
            "pixel": EnumStr(
                Bytes(1),
                inner_pixel=b"I",
                outer_pixel_barrel=b"B",
                pixel_general=b"G",
                pixel_endcaps=b"E",
            ),
            "strip": EnumStr(
                Bytes(1),
                strip_general=b"G",
                strip_barrel=b"B",
                strip_endcaps=b"E",
            ),
            "common": EnumStr(
                Bytes(1),
                common_mechanics=b"CM",
                common_electronics=b"CE",
            ),
        },
    ),
    "component_code"
    / Switch(
        this.subproject_code,
        {
            "inner_pixel": pixels.subproject_codes["PI"],
            "outer_pixel_barrel": pixels.subproject_codes["PB"],
            "pixel_general": pixels.subproject_codes["PG"],
            "pixel_endcaps": pixels.subproject_codes["PE"],
        },
        default=PaddedString(2, "utf8"),
    ),
    "identifier"
    / Switch(
        this.subproject_code,
        {
            "inner_pixel": pixels.identifiers,
            "outer_pixel_barrel": pixels.identifiers,
            "pixel_general": pixels.identifiers,
            "pixel_endcaps": pixels.identifiers,
        },
        default=Bytes(7),
    ),
    Terminated,
)
