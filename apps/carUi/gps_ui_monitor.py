from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from typing import Optional


class GPSUIMonitor:
    """Poll a GPS source and publish structured position updates."""

    def __init__(
        self,
        *,
        root: tk.Misc,
        get_gps_device: Callable[[], object | None],
        set_position: Callable[[float | None, float | None], None],
        set_status: Callable[[str], None] | None = None,
    ) -> None:
        self._root = root
        self._get_gps_device = get_gps_device
        self._set_position = set_position
        self._set_status = set_status
        self._after_id: Optional[str] = None

    def start(self, interval_ms: int) -> None:
        if interval_ms <= 0:
            raise ValueError("interval_ms must be greater than zero")
        self.stop()
        self._poll(interval_ms)

    def stop(self) -> None:
        if self._after_id is None:
            return
        try:
            self._root.after_cancel(self._after_id)
        except tk.TclError:
            pass
        self._after_id = None

    def _poll(self, interval_ms: int) -> None:
        gps_device = self._get_gps_device()
        if gps_device is None:
            self._set_position(None, None)
            self._publish_status("GPS unavailable")
        else:
            self._read_position(gps_device)

        self._after_id = self._root.after(
            interval_ms,
            lambda: self._poll(interval_ms),
        )

    def _read_position(self, gps_device: object) -> None:
        try:
            position = gps_device.position()
            latitude = position.get("lat")
            longitude = position.get("lon")
            has_fix = bool(position.get("fix"))

            if has_fix and latitude is not None and longitude is not None:
                self._set_position(float(latitude), float(longitude))
                return

            self._set_position(None, None)
            self._publish_status("GPS searching")
        except (AttributeError, KeyError, TypeError, ValueError, OSError) as exc:
            self._set_position(None, None)
            self._publish_status(f"GPS error: {exc}")

    def _publish_status(self, message: str) -> None:
        if self._set_status is not None:
            self._set_status(message)
