from abc import ABC, abstractmethod
from typing import Optional

from .radio_types import RadioMode


class RadioBackendIf(ABC):

    @abstractmethod
    def get_frequency(self) -> int:
        pass

    @abstractmethod
    def set_frequency(self, frequency_hz: int) -> None:
        pass

    @abstractmethod
    def set_mode(self, mode: RadioMode) -> None:
        pass

    @abstractmethod
    def get_signal_strength(self) -> Optional[float]:
        pass

    @abstractmethod
    def get_snr(self) -> Optional[float]:
        pass

    @abstractmethod
    def get_rds(self) -> Optional[str]:
        pass
