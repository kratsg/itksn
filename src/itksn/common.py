from __future__ import annotations

from construct import (
    Context,
    Enum,
    EnumIntegerString,
)


class EnumStr(Enum):  # type: ignore[type-arg]  # pylint: disable=abstract-method
    """
    EnumStr class type for decoding strings without attempting to convert to integer.
    """

    def _decode(self, obj: int, _: Context, __: str) -> str | EnumIntegerString:
        """
        Attempt the decoding to string form
        """
        try:
            return self.decmapping[obj]
        except KeyError:
            return EnumIntegerString.new(obj, "")
