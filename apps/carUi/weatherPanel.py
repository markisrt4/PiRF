import tkinter as tk
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class WeatherTileSpec:
    key: str
    label: str
    icon: str


class WeatherPanel(tk.Frame):
    """
    In-app weather subscreen.

    This is intentionally a Frame, not a Toplevel window, so the main app can
    swap it in and out as a subscreen while still keeping the weather UI in a
    separate file.
    """

    def __init__(
        self,
        parent: tk.Misc,
        on_tile_pressed: Callable[[str], None],
        bg_color: str = "#1e1e1e",
        tile_bg: str = "#2a2a2a",
        tile_border: str = "#3f4a52",
    ) -> None:
        super().__init__(parent, bg=bg_color)
        self.on_tile_pressed = on_tile_pressed
        self.bg_color = bg_color
        self.tile_bg = tile_bg
        self.tile_border = tile_border

        self.tile_specs = [
            WeatherTileSpec("weather_band_radio", "Weather Band Radio", "📶"),
            WeatherTileSpec("forecast", "Forecast", "🌦️"),
        ]

        self._build_ui()

    def _build_ui(self) -> None:
        grid = tk.Frame(self, bg=self.bg_color)
        grid.pack(fill="both", expand=True)

        columns = 2
        rows = 1
        for row in range(rows):
            grid.rowconfigure(row, weight=1, uniform="weather_row")
        for col in range(columns):
            grid.columnconfigure(col, weight=1, uniform="weather_col")

        for index, spec in enumerate(self.tile_specs):
            tile = self._create_tile(grid, spec)
            tile.grid(row=0, column=index, sticky="nsew", padx=12, pady=12)

    def _create_tile(self, parent: tk.Misc, spec: WeatherTileSpec) -> tk.Frame:
        tile = tk.Frame(
            parent,
            bg=self.tile_bg,
            highlightthickness=2,
            highlightbackground=self.tile_border,
            bd=0,
            cursor="hand2",
        )

        icon_label = tk.Label(
            tile,
            text=spec.icon,
            font=("DejaVu Sans", 42),
            bg=self.tile_bg,
            fg="#ffffff",
        )
        icon_label.pack(expand=True, pady=(20, 8))

        text_label = tk.Label(
            tile,
            text=spec.label,
            font=("DejaVu Sans", 16, "bold"),
            bg=self.tile_bg,
            fg="#ffffff",
            wraplength=260,
            justify="center",
        )
        text_label.pack(pady=(0, 20))

        self._bind_click_recursive(tile, spec.key)
        return tile

    def _bind_click_recursive(self, widget: tk.Misc, key: str) -> None:
        widget.bind("<Button-1>", lambda event, k=key: self.on_tile_pressed(k))

        if isinstance(widget, (tk.Frame, tk.Label)):
            for child in widget.winfo_children():
                self._bind_click_recursive(child, key)
