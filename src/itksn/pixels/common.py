from __future__ import annotations

from construct import Bytes

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
