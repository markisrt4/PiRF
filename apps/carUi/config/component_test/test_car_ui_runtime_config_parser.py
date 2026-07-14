from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from apps.carUi.config.component_test.car_ui_runtime_config_test_app import main


VALID_TOML = """
[runtime]
remote_display = ":2"

[rigctl]
host = "127.0.0.1"
port = 4532

[[radios]]
key = "fm_radio"
config = "fm_radio.json"
backend = "rigctl"
launcher = "sdrpp"
enabled = true
"""


class CarUiRuntimeConfigTestAppTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.project_root = Path(self.temp_dir.name)
        self.radio_dir = self.project_root / "config" / "radio"
        self.radio_dir.mkdir(parents=True)
        (self.radio_dir / "fm_radio.json").write_text(
            "{}",
            encoding="utf-8",
        )

        self.config_path = self.project_root / "runtime.toml"
        self.config_path.write_text(VALID_TOML, encoding="utf-8")

    def test_valid_config_returns_zero(self) -> None:
        result = main(
            [
                str(self.config_path),
                "--project-root",
                str(self.project_root),
                "--quiet",
            ]
        )
        self.assertEqual(0, result)

    def test_invalid_config_returns_one(self) -> None:
        self.config_path.write_text(
            "[rigctl]\nport = 70000\n",
            encoding="utf-8",
        )

        result = main(
            [
                str(self.config_path),
                "--project-root",
                str(self.project_root),
                "--quiet",
            ]
        )
        self.assertEqual(1, result)

    def test_skip_radio_file_check_allows_missing_json(self) -> None:
        missing_path = self.project_root / "missing.toml"
        missing_path.write_text(
            VALID_TOML.replace("fm_radio.json", "missing.json"),
            encoding="utf-8",
        )

        result = main(
            [
                str(missing_path),
                "--project-root",
                str(self.project_root),
                "--skip-radio-file-check",
                "--quiet",
            ]
        )
        self.assertEqual(0, result)


if __name__ == "__main__":
    unittest.main()
