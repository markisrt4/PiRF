# Environmental Hardware I/O

The `hardware_io.environmental` package provides hardware interfaces and concrete implementations for environmental sensors such as barometric pressure sensors.

The goal of this package is to expose **raw environmental measurements** from physical devices while remaining independent of any application, user interface, or higher-level processing. Environmental calculations such as weather prediction, altitude estimation, sensor fusion, or trend analysis belong in higher-level controllers.

## Design Goals

- Hardware abstraction through common interfaces
- Application-independent design
- Consistent units across all implementations
- Support multiple sensor vendors and communication methods
- Simple, primitive getter-based API
- Suitable for embedded and Raspberry Pi platforms

## Current Sensors

| Device | Interface | Measurements |
|---------|-----------|--------------|
| BMP390 | I²C | Atmospheric pressure, temperature |

Future implementations may include:

- BMP388
- BMP280
- BME280
- BME680
- SHT31
- Other environmental sensors

## Directory Layout

```text
environmental/
├── __init__.py
├── barometric_sensor_if.py
├── bmp390.py
├── component_test/
└── README.md
```

## Responsibilities

This module is responsible for:

- Initializing environmental sensors
- Reading pressure measurements
- Reading temperature measurements
- Managing hardware resources
- Reporting sensor status

This module is **not** responsible for:

- Altitude calculations
- Weather forecasting
- Pressure trend analysis
- Sensor fusion
- Navigation
- Data logging
- User interface

Those responsibilities belong to higher-level controllers.

## Units

The hardware interfaces expose measurements using SI units.

| Measurement | Unit |
|-------------|------|
| Pressure | Pascals (Pa) |
| Temperature | Degrees Celsius (°C) |

Returning consistent units allows higher-level software to perform calculations without needing device-specific conversions.

## Example

```python
from hardware_io.environmental import Bmp390

sensor = Bmp390()

try:
    sensor.start()

    pressure = sensor.get_pressure_pa()
    temperature = sensor.get_temperature_c()

    print(f"Pressure: {pressure:.1f} Pa")
    print(f"Temperature: {temperature:.1f} °C")

finally:
    sensor.stop()
```

## Raspberry Pi Dependencies

The BMP390 implementation uses Adafruit's CircuitPython driver.

```bash
python3 -m pip install \
    adafruit-blinka \
    adafruit-circuitpython-bmp3xx
```

## Component Testing

Concrete sensor implementations should provide a command-line application under `component_test/` that allows hardware verification without requiring higher-level software.

Typical information displayed by a component test includes:

- Device detection
- I²C address
- Pressure
- Temperature
- Update rate
- Error reporting

## Future Expansion

This package is intended to grow as additional environmental sensors are supported.

Potential future capabilities include:

- Humidity sensors
- Ambient light sensors
- Air quality sensors
- Carbon dioxide sensors
- Volatile organic compound (VOC) sensors
- Multiple sensor implementations sharing common interfaces

The public interfaces should remain stable while allowing additional hardware implementations to be added without affecting client applications.
