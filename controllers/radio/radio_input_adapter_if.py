from __future__ import annotations

from typing import Protocol


class RadioInputAdapterIf(Protocol):
    """Lifecycle contract for devices that map input into radio operations."""

    def connect(self) -> None: ...

    def disconnect(self) -> None: ...
