# PiRF Radio Config

Example:

```python
from config.radio_config_manager import (
    load_fm_radio_config,
    load_airband_am_config,
    load_weather_band_config,
    load_ham_radio_config,
)

fm = load_fm_radio_config()
airband = load_airband_am_config()
weather = load_weather_band_config()
ham = load_ham_radio_config()

print(fm.default_mode)
print(weather.presets[0].frequency_hz)
```

Files:

```text
config/
  __init__.py
  radio_config_manager.py
  radio/
    fm_radio.json
    airband_am.json
    weather_band.json
    ham_radio.json
```
