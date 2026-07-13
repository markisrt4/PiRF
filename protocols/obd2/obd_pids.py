from __future__ import annotations


class EngineLoadPid:
    @property
    def pid(self) -> int:
        return 0x04

    def decode(self, data: bytes) -> float | None:
        if len(data) < 1:
            return None

        return data[0] * 100.0 / 255.0


class EngineRpmPid:
    @property
    def pid(self) -> int:
        return 0x0C

    def decode(self, data: bytes) -> int | None:
        if len(data) < 2:
            return None

        return int(((data[0] * 256) + data[1]) / 4)


class VehicleSpeedPid:
    @property
    def pid(self) -> int:
        return 0x0D

    def decode(self, data: bytes) -> float | None:
        if len(data) < 1:
            return None

        return data[0] * 0.621371


class IntakeManifoldPressurePid:
    @property
    def pid(self) -> int:
        return 0x0B

    def decode(self, data: bytes) -> int | None:
        if len(data) < 1:
            return None

        return data[0]


class BarometricPressurePid:
    @property
    def pid(self) -> int:
        return 0x33

    def decode(self, data: bytes) -> int | None:
        if len(data) < 1:
            return None

        return data[0]


class ThrottlePositionPid:
    @property
    def pid(self) -> int:
        return 0x11

    def decode(self, data: bytes) -> float | None:
        if len(data) < 1:
            return None

        return data[0] * 100.0 / 255.0


class AcceleratorPedalPositionPid:
    @property
    def pid(self) -> int:
        return 0x49

    def decode(self, data: bytes) -> float | None:
        if len(data) < 1:
            return None

        return data[0] * 100.0 / 255.0


class CoolantTempPid:
    @property
    def pid(self) -> int:
        return 0x05

    def decode(self, data: bytes) -> float | None:
        if len(data) < 1:
            return None

        temp_c = data[0] - 40
        return temp_c * 9.0 / 5.0 + 32.0


class IntakeAirTempPid:
    @property
    def pid(self) -> int:
        return 0x0F

    def decode(self, data: bytes) -> float | None:
        if len(data) < 1:
            return None

        temp_c = data[0] - 40
        return temp_c * 9.0 / 5.0 + 32.0


class MassAirFlowPid:
    @property
    def pid(self) -> int:
        return 0x10

    def decode(self, data: bytes) -> float | None:
        if len(data) < 2:
            return None

        return ((data[0] * 256) + data[1]) / 100.0


class FuelLevelPid:
    @property
    def pid(self) -> int:
        return 0x2F

    def decode(self, data: bytes) -> float | None:
        if len(data) < 1:
            return None

        return data[0] * 100.0 / 255.0


class ControlModuleVoltagePid:
    @property
    def pid(self) -> int:
        return 0x42

    def decode(self, data: bytes) -> float | None:
        if len(data) < 2:
            return None

        return ((data[0] * 256) + data[1]) / 1000.0
