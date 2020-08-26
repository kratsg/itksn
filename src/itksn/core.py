from construct import Enum, Struct, Bytes, EnumIntegerString


class EnumStr(Enum):
    def _decode(self, obj, context, path):
        try:
            return self.decmapping[obj]
        except KeyError:
            return EnumIntegerString.new(obj, "")


SerialNumberStruct = "SerialNumber" / Struct(
    "atlas_project" / EnumStr(Bytes(2), atlas_detector=b"20"),
    "system_code" / EnumStr(Bytes(1), phaseII_upgrade=b"U",),
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
    "subproject_code" / Bytes(2),
    "identifier" / Bytes(7),
)
