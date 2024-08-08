# Examples

---

## Pixel FE Chip Name to Serial Number

```py
from itksn.core import SerialNumberStruct

serialNumber = SerialNumberStruct.build(
    dict(
        atlas_project="atlas_detector",
        system_code="phaseII_upgrade",
        project_code="pixel_general",
        subproject_code="FE_chip",
        identifier=str(0x130D7).zfill(7).encode("utf-8"),  # (1)!
    )
)
assert serialNumber == b"20UPGFC0078039"  # (2)!
```

1. One passes in the integer representation of the chip name which is treated as
   an integer in python, which we convert to a string and fill with leading
   zeros using `str.zfill` and then encode as bytes (for the underlying
   `construct` object to build out.
2. The result of this is the serial number as bytes, not a string. One can
   decode as normal.
