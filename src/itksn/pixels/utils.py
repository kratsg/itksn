from __future__ import annotations

from typing import TypeVar

from construct import (
    Construct,
    Error,
    Switch,
)

# from construct-typing
ParsedType_co = TypeVar("ParsedType_co", covariant=True)  # pylint:disable=invalid-name
BuildTypes_contra = TypeVar("BuildTypes_contra", contravariant=True)


def subproject_switch(
    pg: Construct[ParsedType_co, BuildTypes_contra] | None = None,
    pi: Construct[ParsedType_co, BuildTypes_contra] | None = None,
    pe: Construct[ParsedType_co, BuildTypes_contra] | None = None,
    pb: Construct[ParsedType_co, BuildTypes_contra] | None = None,
) -> Construct[ParsedType_co, BuildTypes_contra]:
    """
    helper utility to pick up a different Construct for different subprojects
    """
    return Switch(
        lambda ctx: ctx.subproject_code,
        {
            "inner_pixel": pi or Error,
            "outer_pixel_barrel": pb or Error,
            "pixel_general": pg or Error,
            "pixel_endcaps": pe or Error,
        },
    )
