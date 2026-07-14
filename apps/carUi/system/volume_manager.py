from __future__ import annotations

from collections.abc import Callable


class VolumeManager:
    """Coordinate audio volume operations with UI state updates."""

    def __init__(
        self,
        *,
        audio_controller,
        set_volume_level: Callable[[int], None],
        set_status: Callable[[str], None],
    ) -> None:
        self._audio_controller = audio_controller
        self._set_volume_level = set_volume_level
        self._set_status = set_status

    def get_level(self) -> int:
        return self._audio_controller.get_volume_level()

    def volume_up(self) -> None:
        try:
            level = self._audio_controller.volume_up()
            self._set_volume_level(level)
            self._set_status("Volume up")
        except Exception as exc:
            self._set_status(f"Volume up failed: {exc}")
            print(f"[VOLUME] Volume up failed: {exc}")

    def volume_down(self) -> None:
        try:
            level = self._audio_controller.volume_down()
            self._set_volume_level(level)
            self._set_status("Volume down")
        except Exception as exc:
            self._set_status(f"Volume down failed: {exc}")
            print(f"[VOLUME] Volume down failed: {exc}")
