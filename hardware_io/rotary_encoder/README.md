# Rotary Encoder

The `rotary_encoder` component provides a common interface for receiving rotary encoder events.

Two rotary encoder implementations are provided:

- `GpioRotaryEncoder`
- `SeesawRotaryEncoder`

Both implementations use the `RotaryEncoder` interface and report rotation and button events using callbacks.

## Rotary Encoder Interface

The `RotaryEncoder` interface reports the following events:

- Rotation
- Button pressed
- Button released

Rotation callbacks receive the number of encoder steps.

```python
def rotated(steps: int) -> None:
    print(f"Rotated: {steps}")
```

Positive values indicate clockwise rotation.

Negative values indicate counterclockwise rotation.

Example:

```text
+1
+2
-1
```

The reported direction can be reversed when creating an encoder.

## GPIO Rotary Encoder

The `GpioRotaryEncoder` reads a rotary encoder connected directly to Raspberry Pi GPIO pins.

The encoder uses two GPIO inputs for rotation:

- Channel A
- Channel B

An optional GPIO input can be used for the encoder push button.

### Pin Numbering

`GpioRotaryEncoderPins` uses physical Raspberry Pi header pin numbers.

For example:

```python
from hardware_io.rotary_encoder import (
    GpioRotaryEncoder,
    GpioRotaryEncoderPins,
)


encoder = GpioRotaryEncoder(
    pins=GpioRotaryEncoderPins(
        pin_a=11,
        pin_b=13,
        button=15,
    )
)
```

In this example:

```text
Physical Pin 11 -> BCM GPIO17
Physical Pin 13 -> BCM GPIO27
Physical Pin 15 -> BCM GPIO22
```

Physical header pin numbers are converted to BCM GPIO numbers using the GPIO header mapping.

### Using the GPIO Encoder

```python
import time

from hardware_io.rotary_encoder import (
    GpioRotaryEncoder,
    GpioRotaryEncoderPins,
)


def rotated(steps: int) -> None:
    print(f"Rotated: {steps}")


def button_pressed() -> None:
    print("Button pressed")


def button_released() -> None:
    print("Button released")


encoder = GpioRotaryEncoder(
    pins=GpioRotaryEncoderPins(
        pin_a=11,
        pin_b=13,
        button=15,
    )
)

encoder.start(
    rotated=rotated,
    button_pressed=button_pressed,
    button_released=button_released,
)

try:
    while True:
        encoder.tick()
        time.sleep(0.01)

except KeyboardInterrupt:
    pass

finally:
    encoder.cleanup()
```

The `tick()` method dispatches accumulated rotation events and should be called periodically.

## Seesaw Rotary Encoder

The `SeesawRotaryEncoder` reads a rotary encoder through an Adafruit Seesaw I2C device.

Multiple Seesaw rotary encoders can share the same I2C bus.

Each Seesaw device must use a unique I2C address.

The default address is:

```text
0x36
```

Additional encoders can be configured using different addresses.

For example:

```text
Encoder 1 -> 0x36
Encoder 2 -> 0x37
Encoder 3 -> 0x38
```

The I2C address is configured using the address jumpers on the Seesaw board.

### Using One Seesaw Encoder

```python
from hardware_io.rotary_encoder import SeesawRotaryEncoder


def rotated(steps: int) -> None:
    print(f"Rotated: {steps}")


def button_pressed() -> None:
    print("Button pressed")


def button_released() -> None:
    print("Button released")


encoder = SeesawRotaryEncoder(
    address=0x36,
)

encoder.start(
    rotated=rotated,
    button_pressed=button_pressed,
    button_released=button_released,
)
```

The Seesaw encoder monitors rotation and button events in a background thread.

The `tick()` method is not required for the Seesaw implementation.

### Using Multiple Seesaw Encoders

A single I2C bus can be shared between multiple encoders.

```python
import board

from hardware_io.rotary_encoder import SeesawRotaryEncoder


i2c = board.I2C()

encoder_1 = SeesawRotaryEncoder(
    address=0x36,
    i2c=i2c,
)

encoder_2 = SeesawRotaryEncoder(
    address=0x37,
    i2c=i2c,
)

encoder_3 = SeesawRotaryEncoder(
    address=0x38,
    i2c=i2c,
)
```

Each encoder can use its own callbacks.

## Required Libraries

### GPIO Rotary Encoder

The GPIO implementation requires the Raspberry Pi GPIO library.

On Raspberry Pi OS:

```bash
sudo apt install python3-rpi.gpio
```

The Python package can also be installed using:

```bash
python3 -m pip install RPi.GPIO
```

### Seesaw Rotary Encoder

The Seesaw implementation requires the Adafruit Blinka and Seesaw libraries.

Install the required Python packages using:

```bash
python3 -m pip install \
    adafruit-blinka \
    adafruit-circuitpython-seesaw
```

### I2C Support

I2C must be enabled on the Raspberry Pi when using Seesaw rotary encoders.

I2C can be enabled using:

```bash
sudo raspi-config
```

Select:

```text
Interface Options
    -> I2C
        -> Enable
```

The connected I2C devices can be displayed using `i2cdetect`.

Install the I2C tools:

```bash
sudo apt install i2c-tools
```

Scan the I2C bus:

```bash
i2cdetect -y 1
```

Example output with three Seesaw encoders:

```text
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- 36 37 38 -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

The addresses `0x36`, `0x37`, and `0x38` indicate three detected Seesaw devices.

## Component Tests

Example CLI applications are provided in the `component_test` directory.

```text
rotary_encoder/
├── __init__.py
├── rotary_encoder_if.py
├── gpio_rotary_encoder.py
├── seesaw_rotary_encoder.py
├── README.md
└── component_test/
    ├── __init__.py
    ├── gpio_rotary_encoder_cli.py
    └── seesaw_rotary_encoder_cli.py
```

## GPIO Encoder Component Test

Run the GPIO rotary encoder component test from the project root:

```bash
python3 -m hardware_io.rotary_encoder.component_test.gpio_rotary_encoder_cli \
    --pin-a 11 \
    --pin-b 13 \
    --button 15
```

The pin arguments use physical Raspberry Pi header pin numbers.

Example output:

```text
GPIO rotary encoder component test
Channel A physical pin: 11
Channel B physical pin: 13
Button physical pin: 15
Press Ctrl+C to stop.

Rotated clockwise: +1
Rotated clockwise: +1
Button pressed
Button released
Rotated counterclockwise: -1
```

Use the `--reverse` option to reverse the reported rotation direction:

```bash
python3 -m hardware_io.rotary_encoder.component_test.gpio_rotary_encoder_cli \
    --pin-a 11 \
    --pin-b 13 \
    --button 15 \
    --reverse
```

Press `Ctrl+C` to stop the component test.

## Seesaw Encoder Component Test

The Seesaw component test monitors three rotary encoders on a shared I2C bus.

The default addresses are:

```text
0x36
0x37
0x38
```

Run the component test from the project root:

```bash
python3 -m hardware_io.rotary_encoder.component_test.seesaw_rotary_encoder_cli
```

Example output:

```text
Initializing shared I2C bus...

Seesaw rotary encoder component test
Configured encoders:
  encoder-1: 0x36
  encoder-2: 0x37
  encoder-3: 0x38

Rotate or press any encoder.
Press Ctrl+C to stop.

[encoder-1 0x36] rotated clockwise: +1
[encoder-2 0x37] button pressed
[encoder-2 0x37] button released
[encoder-3 0x38] rotated counterclockwise: -1
```

Custom I2C addresses can be specified using command-line arguments:

```bash
python3 -m hardware_io.rotary_encoder.component_test.seesaw_rotary_encoder_cli \
    --encoder-1-address 0x36 \
    --encoder-2-address 0x37 \
    --encoder-3-address 0x38
```

Use the `--reverse` option to reverse the reported rotation direction for all encoders:

```bash
python3 -m hardware_io.rotary_encoder.component_test.seesaw_rotary_encoder_cli \
    --reverse
```

Press `Ctrl+C` to stop the component test.

## Design

The rotary encoder interface reports rotation and button events using callbacks.

Hardware-specific behavior is contained within each rotary encoder implementation.

The GPIO implementation uses Raspberry Pi GPIO interrupts and dispatches accumulated rotation through `tick()`.

The Seesaw implementation reads encoder state over I2C and monitors the devices using background threads.
