import tkinter as tk
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class AircraftTileSpec:
    key: str
    label: str
    icon: str


class AircraftPanel(tk.Frame):
    def __init__(self, parent: tk.Widget, on_tile_pressed: Callable[[str], None]) -> None:
        super().__init__(parent, bg="#1e1e1e")
        self.on_tile_pressed = on_tile_pressed

        self.tile_specs = [
            AircraftTileSpec("adsb", "ADS-B", "🛩️"),
            AircraftTileSpec("airband_am", "Airband AM", "✈️📻"),
        ]

        self._build_ui()

    def _build_ui(self) -> None:
        grid = tk.Frame(self, bg="#1e1e1e")
        grid.pack(fill="both", expand=True)

        cols = 2
        rows = 1

        for row in range(rows):
            grid.rowconfigure(row, weight=1, uniform="aircraft_row")
        for col in range(cols):
            grid.columnconfigure(col, weight=1, uniform="aircraft_col")

        for index, spec in enumerate(self.tile_specs):
            tile = self._create_tile(grid, spec)
            tile.grid(row=0, column=index, sticky="nsew", padx=16, pady=16)

    def _create_tile(self, parent: tk.Widget, spec: AircraftTileSpec) -> tk.Frame:
        tile = tk.Frame(
            parent,
            bg="#2a2a2a",
            highlightthickness=2,
            highlightbackground="#3f4a52",
            highlightcolor="#8ca0ad",
            bd=0,
            cursor="hand2",
        )

        icon_label = tk.Label(
            tile,
            text=spec.icon,
            font=("DejaVu Sans", 42),
            bg="#2a2a2a",
            fg="#ffffff",
        )
        icon_label.pack(expand=True, pady=(20, 8))

        text_label = tk.Label(
            tile,
            text=spec.label,
            font=("DejaVu Sans", 16, "bold"),
            bg="#2a2a2a",
            fg="#ffffff",
            wraplength=220,
            justify="center",
        )
        text_label.pack(pady=(0, 20))

        self._bind_click_recursive(tile, spec.key)
        return tile

    def _bind_click_recursive(self, widget: tk.Widget, key: str) -> None:
        widget.bind("<Button-1>", lambda event, k=key: self.on_tile_pressed(k))
        for child in widget.winfo_children():
            self._bind_click_recursive(child, key)
