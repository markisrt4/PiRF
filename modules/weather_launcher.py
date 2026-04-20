import subprocess
from pathlib import Path
from typing import Callable, Optional


def launch_weather_dashboard(
    remote_display: str = ":1",
    set_status: Optional[Callable[[str], None]] = None,
) -> None:
    """
    Launch the Streamlit weather dashboard and open it on the remote X display.

    Expected project layout:
      <project_root>/
        modules/
        apps/carUi/
          run_weather_dash.sh
          weather_dash.py
    """
    project_root = Path(__file__).resolve().parent.parent
    car_ui_dir = project_root / "apps" / "carUi"

    if set_status:
        set_status("Launching weather dashboard on remote display...")

    command = [
        "bash",
        "-lc",
        (
            f'cd "{car_ui_dir}" && '
            'pgrep -f "streamlit run weather_dash.py" >/dev/null || '
            './run_weather_dash.sh >/tmp/carsdr-weather.log 2>&1 & '
            f'DISPLAY={remote_display} xdg-open http://127.0.0.1:8501 '
            '>/tmp/carsdr-weather-browser.log 2>&1 &'
        ),
    ]

    subprocess.Popen(command)

    if set_status:
        set_status("Weather dashboard launched")