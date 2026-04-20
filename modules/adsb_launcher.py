import subprocess
from pathlib import Path
from typing import Callable, Optional


def launch_adsb_dashboard(
    remote_display: str = ":1",
    set_status: Optional[Callable[[str], None]] = None,
    url: str = "http://127.0.0.1/tar1090",
) -> None:
    """
    Launch the ADS-B web UI on the remote X display.

    Expected project layout:
      <project_root>/
        modules/
        apps/carUi/
          run_adsb.sh
    """
    project_root = Path(__file__).resolve().parent.parent
    car_ui_dir = project_root / "apps" / "carUi"

    if set_status:
        set_status("Launching ADS-B dashboard on remote display...")

    command = [
        "bash",
        "-lc",
        (
            f'cd "{car_ui_dir}" && '
            './run_adsb.sh >/tmp/carsdr-adsb.log 2>&1 & '
            f'DISPLAY={remote_display} xdg-open "{url}" '
            '>/tmp/carsdr-adsb-browser.log 2>&1 &'
        ),
    ]

    subprocess.Popen(command)

    if set_status:
        set_status("ADS-B dashboard launched")
