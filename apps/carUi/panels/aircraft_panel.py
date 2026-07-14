from __future__ import annotations

import tkinter as tk
from dataclasses import dataclass
from typing import Callable

from apps.common.uiTheme import COLORS, MENU_TILE_STYLE


@dataclass(frozen=True)
class AircraftTileSpec:
    key: str
    label: str
    subtitle: str
    detail: str


class AircraftPanel(tk.Frame):
    def __init__(
        self,
        parent: tk.Widget,
        on_adsb_pressed: Callable[[], None],
        on_airband_pressed: Callable[[], None],
        create_tile: Callable[[tk.Widget, str, str, str, str], tk.Frame],
    ) -> None:
        super().__init__(parent, bg=COLORS["app_bg"])

        self._on_adsb_pressed = on_adsb_pressed
        self._on_airband_pressed = on_airband_pressed
        self._create_tile = create_tile
        compact_ui = bool(getattr(parent.winfo_toplevel(), "compact_ui", False))
        self._style = MENU_TILE_STYLE["compact" if compact_ui else "normal"]
        self._tile_specs = (
            AircraftTileSpec("adsb", "ADS-B", "Aircraft tracking", "Launch tar1090 web UI"),
            AircraftTileSpec("airband_am", "AIRBAND AM", "Aircraft chatter", "Launch SDR++ airband receiver"),
        )
        self._build_ui()

    def _build_ui(self) -> None:
        grid = tk.Frame(self, bg=COLORS["app_bg"])
        grid.pack(fill="both", expand=True)

        for column in range(len(self._tile_specs)):
            grid.columnconfigure(column, weight=1, uniform="aircraft_col")
        grid.rowconfigure(0, weight=1, uniform="aircraft_row")

        callbacks = {
            "adsb": self._on_adsb_pressed,
            "airband_am": self._on_airband_pressed,
        }

        for column, spec in enumerate(self._tile_specs):
            tile = self._create_tile(grid, spec.key, spec.label, spec.subtitle, spec.detail)
            tile.grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=self._style["tile_padx"],
                pady=self._style["tile_pady"],
            )
            self._bind_click_recursive(tile, callbacks[spec.key])

    def _bind_click_recursive(self, widget: tk.Widget, callback: Callable[[], None]) -> None:
        widget.bind("<Button-1>", lambda event: callback())
        for child in widget.winfo_children():
            self._bind_click_recursive(child, callback)
