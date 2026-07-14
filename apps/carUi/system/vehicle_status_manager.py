from __future__ import annotations

from collections.abc import Callable

from apps.carUi.radio.radio_status_formatter import format_frequency


class VehicleStatusManager:
    """Coordinate vehicle-related values with top-bar display updates."""

    def __init__(
        self,
        *,
        set_frequency_text: Callable[[str], None],
        set_location_text: Callable[[str], None],
        empty_value: str = "--",
    ) -> None:
        self._set_frequency_text = set_frequency_text
        self._set_location_text = set_location_text
        self._empty_value = empty_value

    def set_frequency(self, frequency_hz: int | None) -> None:
        text = (
            self._empty_value
            if frequency_hz is None
            else format_frequency(frequency_hz, precision=3)
        )
        self._set_frequency_text(text)

    def set_location(
        self,
        latitude: float | None,
        longitude: float | None,
    ) -> None:
        if latitude is None or longitude is None:
            self._set_location_text("🌎 lat.--, lon.--")
            return

        self._set_location_text(
            f"🌎 lat.{latitude:.4f}, lon.{longitude:.4f}"
        )

    def set_location_text(self, text: str) -> None:
        """Pass through preformatted GPS location text."""

        self._set_location_text(text)
