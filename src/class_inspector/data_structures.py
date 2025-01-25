from __future__ import annotations

from typing import Optional

import attrs
from attrs.validators import instance_of, optional


@attrs.define
class ParamDetails:
    name: str = attrs.field(validator=[instance_of(str)])
    annot: str = attrs.field(default="", validator=[instance_of(str)])
    default: Optional[str] = attrs.field(
        default=None, validator=[optional(instance_of(str))]
    )


@attrs.define
class FuncDetails:
    name: str = attrs.field()
    params: dict = attrs.field(default=None)
    return_annot: str = attrs.field(default="", validator=[instance_of(str)])
    raises: list = attrs.field(default=None)
    class_name: str = attrs.field(default="")

    def __attrs_post_init__(self):
        self.params = self.params or {}
        self.raises = self.raises or []
