"""
Domain-level exceptions for the Memory Engine's retrieval/reasoning core.
"""
from __future__ import annotations


class MemoryEngineError(Exception):
    """Base class for all retrieval-engine errors."""


class InvalidRetrievalRequestError(MemoryEngineError):
    """Raised when a retrieval request is structurally valid but semantically unusable."""