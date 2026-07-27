"""
Enumerations for the Memory Engine domain models.
"""
from __future__ import annotations

import enum


class MemoryType(str, enum.Enum):
    """
    Classifies the nature of a stored memory.

    Inherits from `str` so instances serialize cleanly to JSON / Pydantic
    without a custom encoder, while remaining a proper native PostgreSQL
    enum at the database layer.
    """

    SHORT_TERM = "SHORT_TERM"
    LONG_TERM = "LONG_TERM"
    PREFERENCE = "PREFERENCE"
    FACT = "FACT"
    EVENT = "EVENT"
    PROJECT = "PROJECT"
    GOAL = "GOAL"
    TASK = "TASK"
    RELATIONSHIP = "RELATIONSHIP"
    HABIT = "HABIT"
    KNOWLEDGE = "KNOWLEDGE"
    CONVERSATION = "CONVERSATION"