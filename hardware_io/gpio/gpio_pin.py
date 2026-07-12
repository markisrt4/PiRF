from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GpioPin:
    """
    Describes one physical pin on a Raspberry Pi GPIO header.
    """

    physical_pin: int
    bcm: int | None
    name: str
    function: str

    @property
    def is_gpio(self) -> bool:
        return self.bcm is not None
