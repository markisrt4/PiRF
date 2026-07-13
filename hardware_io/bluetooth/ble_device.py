from attr import dataclass


@dataclass(frozen=True)
class BleDeviceInfo:
    address: str
    name: str | None
    rssi: int | None
    service_uuids: tuple[str, ...]
