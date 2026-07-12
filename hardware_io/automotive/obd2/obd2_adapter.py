from __future__ import annotations

from abc import ABC, abstractmethod

from hardware_io.automotive.obd2.obd2_response import Obd2Response


class Obd2Adapter(ABC):
    """
    Interface implemented by OBD-II adapter hardware.

    Higher-level OBD-II components should depend on this interface rather
    than a specific adapter such as an ELM327.
    """

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """
        Return whether the adapter is currently connected.
        """

    @abstractmethod
    def connect(self) -> None:
        """
        Connect to and initialize the adapter.
        """

    @abstractmethod
    def disconnect(self) -> None:
        """
        Disconnect from the adapter.
        """

    @abstractmethod
    def send_command(self, command: str) -> Obd2Response:
        """
        Send an OBD-II or adapter-specific command.
        """
