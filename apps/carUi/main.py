import subprocess
import tkinter as tk
from dataclasses import dataclass
from typing import Callable, Dict, Optional

from weatherPanel import WeatherPanel


@dataclass(frozen=True)
class TileSpec:
    key: str
    label: str
    icon: str


class SDRControlPanel(tk.Tk):
    """
    Touch-friendly SDR launcher UI.

    Notes:
    - Starts fullscreen by default for 7-inch displays
    - Main screen stays dark, with a light banner on top
    - Weather is an in-app subscreen implemented in a separate file
    - Pressing Weather triggers the registered callback first
    """

    def __init__(
        self,
        callbacks: Optional[Dict[str, Callable[[str], None]]] = None,
        title: str = "SDR Control Panel",
        remote_display: str = ":1",
    ) -> None:
        super().__init__()

        self.callbacks: Dict[str, Callable[[str], None]] = callbacks or {}
        self.remote_display = remote_display

        self.title(title)
        self.geometry("1024x600")
        self.minsize(800, 480)
        self.configure(bg="#1e1e1e")
        self.attributes("-fullscreen", True)

        self.main_tile_specs = [
            TileSpec("fm_radio", "FM Radio", "📻"),
            TileSpec("ham_radio", "Ham Radio", "📡📻"),
            TileSpec("aircraft", "Aircraft", "✈"),
            TileSpec("lighting", "Lighting", "🔆"),
            TileSpec("weather", "Weather", "🌦️"),
            TileSpec("settings", "Settings", "⚙"),
        ]

        self.status_var = tk.StringVar(value="Ready")
        self.content_frame: Optional[tk.Frame] = None

        self._build_ui()
        self.show_main_menu()
        self.bind("<Escape>", self._toggle_fullscreen)

    def _build_ui(self) -> None:
        container = tk.Frame(self, bg="#1e1e1e")
        container.pack(fill="both", expand=True)

        self.top_bar = tk.Frame(container, bg="#dfe7eb", height=68)
        self.top_bar.pack(fill="x", side="top")
        self.top_bar.pack_propagate(False)

        self.left_button = tk.Button(
            self.top_bar,
            text="",
            font=("DejaVu Sans", 16, "bold"),
            bg="#dfe7eb",
            fg="#1d2429",
            activebackground="#cfd9de",
            activeforeground="#1d2429",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2",
            command=self.show_main_menu,
        )
        self.left_button.pack(side="left", padx=(10, 0), pady=10)
        self.left_button.pack_forget()

        self.title_label = tk.Label(
            self.top_bar,
            text="Mark's CarSDR Control Panel",
            font=("DejaVu Sans", 20, "bold"),
            bg="#dfe7eb",
            fg="#1d2429",
        )
        self.title_label.pack(side="left", padx=20)

        self.power_button = tk.Button(
            self.top_bar,
            text="⏻",
            font=("DejaVu Sans", 20, "bold"),
            bg="#c62828",
            fg="#ffffff",
            activebackground="#a91f1f",
            activeforeground="#ffffff",
            bd=0,
            width=3,
            pady=4,
            command=self.destroy,
            cursor="hand2",
        )
        self.power_button.pack(side="right", padx=16, pady=10)

        self.content_frame = tk.Frame(container, bg="#1e1e1e")
        self.content_frame.pack(fill="both", expand=True, padx=18, pady=18)

        status_bar = tk.Label(
            container,
            textvariable=self.status_var,
            anchor="w",
            bg="#111111",
            fg="#f2f2f2",
            font=("DejaVu Sans", 12),
            padx=14,
            pady=10,
        )
        status_bar.pack(fill="x", side="bottom")

    def _clear_content(self) -> None:
        if self.content_frame is None:
            return
        for child in self.content_frame.winfo_children():
            child.destroy()

    def _build_main_tile_grid(self) -> None:
        if self.content_frame is None:
            return

        self._clear_content()
        grid_frame = tk.Frame(self.content_frame, bg="#1e1e1e")
        grid_frame.pack(fill="both", expand=True)

        rows = 2
        cols = 3
        for row in range(rows):
            grid_frame.rowconfigure(row, weight=1, uniform="tile_row")
        for col in range(cols):
            grid_frame.columnconfigure(col, weight=1, uniform="tile_col")

        for index, spec in enumerate(self.main_tile_specs):
            row = index // cols
            col = index % cols
            tile = self._create_tile(grid_frame, spec)
            tile.grid(row=row, column=col, sticky="nsew", padx=12, pady=12)

    def _create_tile(self, parent: tk.Widget, spec: TileSpec) -> tk.Frame:
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

        self._bind_click_recursive(tile, spec)
        return tile

    def _bind_click_recursive(self, widget: tk.Widget, spec: TileSpec) -> None:
        widget.bind("<Button-1>", lambda event, s=spec: self._on_tile_clicked(s))
        widget.bind("<ButtonRelease-1>", lambda event, w=widget: self._clear_tile_focus(w))

        if isinstance(widget, (tk.Frame, tk.Label)):
            for child in widget.winfo_children():
                self._bind_click_recursive(child, spec)

    def _run_callback(self, key: str) -> None:
        callback = self.callbacks.get(key)
        if callback is None:
            return
        try:
            callback(key)
        except Exception as exc:
            self.status_var.set(f"Callback error in {key}: {exc}")
            print(f"[UI] Callback error for {key}: {exc}")

    def _on_tile_clicked(self, spec: TileSpec) -> None:
        self.status_var.set(f"Selected: {spec.label}")
        self._run_callback(spec.key)

    def _on_weather_tile_pressed(self, key: str) -> None:
        self.status_var.set(f"Selected: {key}")
        self._run_callback(key)

    def show_main_menu(self) -> None:
        self.title_label.config(text="Mark's CarSDR Control Panel")
        self.left_button.pack_forget()
        self._build_main_tile_grid()
        self.status_var.set("Ready")

    def show_weather_menu(self) -> None:
        if self.content_frame is None:
            return

        self.title_label.config(text="Weather")
        self.left_button.config(text="←")
        self.left_button.pack(side="left", padx=(10, 0), pady=10)

        self._clear_content()
        weather_view = WeatherPanel(
            self.content_frame,
            on_tile_pressed=self._on_weather_tile_pressed,
        )
        weather_view.pack(fill="both", expand=True)
        self.status_var.set("Weather menu ready")

    def launch_weather_band_radio(self) -> None:
        try:
            self.status_var.set("Launching SDR++ on remote display...")
            command = [
                "bash",
                "-lc",
                (
                    f'DISPLAY={self.remote_display} '
                    'sdrpp >/tmp/carsdr-sdrpp-weather.log 2>&1 &'
                ),
            ]
            subprocess.Popen(command)
            self._tune_sdrpp_to_weather_band()
            self.status_var.set("Weather band radio launched at 162.550 MHz FM")
        except Exception as exc:
            self.status_var.set(f"Weather radio launch failed: {exc}")
            print(f"[UI] launch_weather_band_radio error: {exc}")

    def launch_forecast(self) -> None:
        try:
            self.status_var.set("Launching forecast dashboard on remote display...")
            command = [
                "bash",
                "-lc",
                (
                    f'DISPLAY={self.remote_display} '
                    'xdg-open "https://forecast.weather.gov/MapClick.php?FcstType=graphical" '
                    '>/tmp/carsdr-forecast.log 2>&1 &'
                ),
            ]
            subprocess.Popen(command)
            self.status_var.set("Forecast dashboard launched")
        except Exception as exc:
            self.status_var.set(f"Forecast launch failed: {exc}")
            print(f"[UI] launch_forecast error: {exc}")

    def _tune_sdrpp_to_weather_band(self) -> None:
        print("[UI] Tune SDR++ to 162.550 MHz, mode=FM")

    def _clear_tile_focus(self, widget: tk.Widget) -> None:
        try:
            widget.focus_set()
        except Exception:
            pass

    def _toggle_fullscreen(self, event=None) -> None:
        current = bool(self.attributes("-fullscreen"))
        self.attributes("-fullscreen", not current)
        mode = "enabled" if not current else "disabled"
        self.status_var.set(f"Fullscreen {mode}")


# -----------------------------
# Example callback functions
# Replace these with real logic.
# -----------------------------
def on_fm_radio(component: str) -> None:
    print(f"Launching {component}: tune to FM mode")


def on_ham_radio(component: str) -> None:
    print(f"Launching {component}: open ham/CB radio controls")


def on_aircraft(component: str) -> None:
    print(f"Launching {component}: load airband preset")


def on_lighting(component: str) -> None:
    print(f"Launching {component}: open LED lighting controls")


def make_on_weather(app: "SDRControlPanel") -> Callable[[str], None]:
    def on_weather(component: str) -> None:
        print(f"Launching {component}: opening weather submenu")
        app.show_weather_menu()
    return on_weather


def make_on_weather_band_radio(app: "SDRControlPanel") -> Callable[[str], None]:
    def on_weather_band_radio(component: str) -> None:
        print(f"Launching {component}: weather band radio action")
        app.launch_weather_band_radio()
    return on_weather_band_radio


def make_on_forecast(app: "SDRControlPanel") -> Callable[[str], None]:
    def on_forecast(component: str) -> None:
        print(f"Launching {component}: forecast action")
        app.launch_forecast()
    return on_forecast


def on_settings(component: str) -> None:
    print(f"Launching {component}: open settings page")


if __name__ == "__main__":
    app = SDRControlPanel(callbacks={})

    app.callbacks.update({
        "fm_radio": on_fm_radio,
        "ham_radio": on_ham_radio,
        "aircraft": on_aircraft,
        "lighting": on_lighting,
        "weather": make_on_weather(app),
        "weather_band_radio": make_on_weather_band_radio(app),
        "forecast": make_on_forecast(app),
        "settings": on_settings,
    })

    app.mainloop()
