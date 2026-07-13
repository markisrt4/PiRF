# Bluetooth

The `bluetooth` component provides low-level Bluetooth communication and discovery utilities.

## BLE Scanner

The `BleScanner` scans for nearby Bluetooth Low Energy devices.

It returns discovered devices as `BleDeviceInfo` objects.

Each device may contain:

- Bluetooth address
- Device name
- Advertised local name
- Signal strength
- Advertised service UUIDs
- Manufacturer data

The scanner returns all discovered BLE devices and does not filter them by protocol or device type.

## Dependency

The Bluetooth component requires `bleak`.

Install it using:

```bash
python3 -m pip install bleak
```

Linux systems also require Bluetooth support through BlueZ.

On Debian or Raspberry Pi OS:

```bash
sudo apt install bluetooth bluez
```

The Bluetooth adapter must be enabled before scanning.

Check the adapter using:

```bash
bluetoothctl show
```

## Component Test

A BLE scanner CLI component test is provided in the `component_test` directory.

```text
bluetooth/
├── __init__.py
├── ble_scanner.py
├── README.md
└── component_test/
    ├── __init__.py
    └── ble_scan_cli.py
```

Run the component test from the project root:

```bash
python3 -m hardware_io.bluetooth.component_test.ble_scan_cli
```

The default scan duration is 10 seconds.

A different scan duration can be specified using `--timeout`:

```bash
python3 -m hardware_io.bluetooth.component_test.ble_scan_cli \
    --timeout 15
```

Example output:

```text
Scanning for Bluetooth Low Energy devices for 10.0 seconds...

============================================================
0A:FE:EF:0C:57:3C
Name: None
Local name: None
RSSI: -56
Service UUIDs: []
Manufacturer data: {}
============================================================
12:34:5A:05:9C:54
Name: KONNWEI
Local name: KONNWEI
RSSI: -68
Service UUIDs: ['00001101-0000-1000-8000-00805f9b34fb']
Manufacturer data: {}
============================================================
Found 2 BLE device(s).
```

## Design

The Bluetooth component provides generic Bluetooth discovery and communication functionality.

It does not identify devices for a specific protocol or assign meaning to discovered devices.
