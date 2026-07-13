from __future__ import annotations

from abc import ABC, abstractmethod

from protocols.obd2.obd2_request import Obd2Request
from protocols.obd2.obd2_response import Obd2Response


class Obd2AdapterIf(ABC):
    """
    Interface for performing OBD-II diagnostic requests.
    """

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        ...

    @abstractmethod
    def connect(self) -> None:
        ...

    @abstractmethod
    def disconnect(self) -> None:
        ...

    @abstractmethod
    def request(
        self,
        request: Obd2Request,
    ) -> Obd2Response | None:
        ...
