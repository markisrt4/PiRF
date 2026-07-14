from __future__ import annotations

import os
from pathlib import Path

from apps.carUi.runtime.radio_runtime_factory import create_car_ui_runtime
from apps.carUi.uiControlPanel import UiControlPanel
from hardware_io.gps.gps_reader import GpsReader
from controllers.lighting.leddmx_bluetooth_controller import LedDmxBluetoothController


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_CONFIG_PATH = (
    PROJECT_ROOT / "apps" / "carUi" / "config" / "car_ui_runtime.toml"
)


def main() -> None:
    runtime = create_car_ui_runtime(
        RUNTIME_CONFIG_PATH,
        project_root=PROJECT_ROOT,
    )

    gps_device = GpsReader()
    gps_device.start()

    lighting_controller = LedDmxBluetoothController(
        address=os.getenv("CARUI_LIGHTING_ADDRESS"),
    )

    app = UiControlPanel(
        runtime=runtime,
        gps_device=gps_device,
        lighting_controller=lighting_controller,
    )
    app.register_default_callbacks()
    app.start_gps_ui_updates()
    app.mainloop()


if __name__ == "__main__":
    main()
