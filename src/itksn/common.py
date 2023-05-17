from __future__ import annotations

import sys
from typing import TYPE_CHECKING

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from construct import (
    Adapter,
    Construct,
    MappingError,
)

if TYPE_CHECKING:
    from construct import Context

    TheAdapter = Adapter[bytes, bytes, "EnumByteString", str]
else:
    Context = "Context"  # pylint: disable=invalid-name
    TheAdapter = Adapter


class EnumByteString(str):
    """
    Like EnumIntegerString but for Bytes.
    """

    bytevalue: bytes

    def __repr__(self: Self) -> str:
        return f"EnumByteString.new({self.bytevalue!s}, {str.__repr__(self)})"

    def __int__(self: Self) -> bytes:
        return self.bytevalue

    @staticmethod
    def new(bytevalue: bytes, stringvalue: str) -> EnumByteString:
        """
        Create EnumByteString object as a class constructor
        """
        ret = EnumByteString(stringvalue)
        ret.bytevalue = bytevalue
        return ret


class EnumStr(TheAdapter):
    r"""
    This is exactly the same as construct.Enum, but supports byte subcons.
    """

    def __init__(self: Self, subcon: Construct[bytes, bytes], **mapping: bytes) -> None:
        super().__init__(subcon)
        self.encmapping: dict[str, bytes] = {
            EnumByteString.new(v, k): v for k, v in mapping.items()
        }
        self.decmapping: dict[bytes, EnumByteString] = {
            v: EnumByteString.new(v, k) for k, v in mapping.items()
        }
        self.ksymapping: dict[bytes, str] = {v: k for k, v in mapping.items()}

    def __getattr__(self, name: str) -> EnumByteString:
        if name in self.encmapping:
            return self.decmapping[self.encmapping[name]]
        raise AttributeError

    def _decode(self, obj: bytes, _: Context, __: str):  # type: ignore[no-untyped-def]
        try:
            return self.decmapping[obj]
        except KeyError:
            return EnumByteString.new(obj, "")

    def _encode(self, obj: str, _: Context, path: str):  # type: ignore[no-untyped-def]
        try:
            return self.encmapping[obj]
        except KeyError as exc:
            msg = f"building failed, no mapping for {obj!r}"
            raise MappingError(msg, path=path) from exc

    def _emitparse(self, code):  # type: ignore[no-untyped-def]
        fname = f"factory_{code.allocateId()}"
        code.append(f"{fname} = {self.decmapping!r}")
        return f"reuse(({self.subcon._compileparse(code)}), lambda x: {fname}.get(x, EnumInteger(x)))"  # type: ignore[attr-defined]  # pylint: disable=protected-access

    def _emitbuild(self, code):  # type: ignore[no-untyped-def]
        fname = f"factory_{code.allocateId()}"
        code.append(f"{fname} = {self.encmapping!r}")
        return f"reuse({fname}.get(obj, obj), lambda obj: ({self.subcon._compilebuild(code)}))"  # type: ignore[attr-defined]  # pylint: disable=protected-access

    def _emitprimitivetype(self, ksy, _):  # type: ignore[no-untyped-def]
        name = f"enum_{ksy.allocateId()}"
        ksy.enums[name] = self.ksymapping
        return name
