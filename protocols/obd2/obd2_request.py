from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Obd2Request:
    """
    Represents an OBD-II diagnostic request.
    """

    mode: int
    pid: int | None = None

    def __post_init__(self) -> None:
        if not 0 <= self.mode <= 0xFF:
            raise ValueError("mode must be in range 0x00..0xFF")

        if self.pid is not None and not 0 <= self.pid <= 0xFF:
            raise ValueError("pid must be in range 0x00..0xFF")
