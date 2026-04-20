import subprocess
from typing import Callable, Optional


def launch_airband_am(
    remote_display: str = ":1",
    set_status: Optional[Callable[[str], None]] = None,
) -> None:
    if set_status:
        set_status("Launching airband AM on remote display...")

    command = [
        "bash",
        "-lc",
        (
            f'DISPLAY={remote_display} '
            'sdrpp >/tmp/carsdr-airband.log 2>&1 &'
        ),
    ]

    subprocess.Popen(command)

    if set_status:
        set_status("Airband AM launched")
