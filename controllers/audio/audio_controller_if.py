from __future__ import annotations

from abc import ABC, abstractmethod


class AudioControllerIf(ABC):
    """
    Interface for controlling audio output volume.
    """

    @property
    @abstractmethod
    def maximum_level(self) -> int:
        """Return the maximum discrete volume level."""

    @abstractmethod
    def volume_up(self) -> int:
        """
        Increase volume and return the resulting level.
        """

    @abstractmethod
    def volume_down(self) -> int:
        """
        Decrease volume and return the resulting level.
        """

    @abstractmethod
    def get_volume_level(self) -> int:
        """
        Return the current discrete volume level.
        """

    @abstractmethod
    def set_volume_level(self, level: int) -> int:
        """
        Set the volume level and return the resulting level.
        """

    @abstractmethod
    def is_muted(self) -> bool:
        """Return whether audio output is muted."""

    @abstractmethod
    def toggle_mute(self) -> bool:
        """Toggle mute and return the resulting muted state."""

    def adjust_volume(self, steps: int) -> int:
        """
        Adjust the current volume by a number of discrete steps.
        """
        current_level = self.get_volume_level()
        return self.set_volume_level(current_level + steps)
