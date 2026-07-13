from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable


RotationCallback = Callable[[int], None]
ButtonCallback = Callable[[], None]


class RotaryEncoderIf(ABC):
    """
    Interface for receiving rotary encoder events.

    Positive rotation values indicate clockwise movement.
    Negative rotation values indicate counterclockwise movement.
    """

    @property
    @abstractmethod
    def is_running(self) -> bool:
        """
        Return whether the encoder is currently being monitored.
        """

    @abstractmethod
    def start(
        self,
        rotated: RotationCallback,
        button_pressed: ButtonCallback | None = None,
        button_released: ButtonCallback | None = None,
    ) -> None:
        """
        Start monitoring the rotary encoder.

        Args:
            rotated:
                Called when the encoder rotates.

                The callback receives the number of encoder steps since the
                previous event.

            button_pressed:
                Called when the encoder button is pressed.

            button_released:
                Called when the encoder button is released.
        """

    @abstractmethod
    def stop(self) -> None:
        """
        Stop monitoring the rotary encoder.
        """
