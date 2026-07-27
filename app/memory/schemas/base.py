"""
Shared Pydantic v2 base configuration for the Memory Engine schema layer.

Centralizing the base model here guarantees every schema in this module
serializes/validates identically (ORM mode, enum-by-value, strict
extra-field handling) without repeating `model_config` in every file.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ORMBaseSchema(BaseModel):
    """
    Base for schemas that are read FROM ORM instances (`Memory` model).

    `from_attributes=True` allows `Model.model_validate(orm_instance)`.
    `use_enum_values=True` ensures enum fields serialize as their plain
    string value rather than `MemoryType.FACT` repr.
    """

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        populate_by_name=True,
    )


class StrictBaseSchema(BaseModel):
    """
    Base for input schemas (Create/Update payloads).

    `extra="forbid"` rejects unknown fields outright — enterprise APIs
    should never silently ignore typos or unsupported client fields.
    """

    model_config = ConfigDict(
        extra="forbid",
        use_enum_values=True,
        str_strip_whitespace=True,
    )