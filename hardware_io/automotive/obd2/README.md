# OBD-II

The `obd2` component provides a hardware abstraction for communicating with OBD-II adapters.

Higher-level Drive UbiquitOS components should use the `Obd2Adapter` interface rather than depending directly on a specific adapter implementation.

## OBD-II Adapter

The `Obd2Adapter` class defines the common interface used by OBD-II adapter implementations.

An adapter is responsible for:

- Connecting to the OBD-II hardware
- Disconnecting from the hardware
- Reporting connection state
- Sending commands
- Returning an `Obd2Response`

## OBD-II Response

The `Obd2Response` class provides a common response format for OBD-II adapters.

A response contains:

- The command that was sent
- The raw adapter response
- Parsed response lines

## Adapter Implementations

Adapter-specific implementations are stored in their own directories.

Current implementations:

- ELM327

Higher-level components should depend on `Obd2Adapter` rather than a specific adapter implementation.

## Example

```python
from hardware_io.automotive.obd2 import Obd2Adapter


def send_engine_rpm_request(adapter: Obd2Adapter) -> None:
    response = adapter.send_command("010C")

    print(response.raw)
```

## Component Test

A simple CLI component test is provided in the `component_test` directory.

Run the test from the project root:

```bash
python3 -m hardware_io.automotive.obd2.component_test.obd2_cli
```

The component test connects to an OBD-II adapter and allows commands to be entered interactively.

## Design

The OBD-II hardware layer is responsible for communication with OBD-II adapter hardware.

OBD-II PID interpretation, vehicle state, and application-specific behavior should be handled by higher-level components.
