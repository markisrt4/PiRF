"""Raspberry Pi GPIO pushbutton implementation."""

from __future__ import annotations

from threading import Lock

from gpiozero import Button

from hardware_io.buttons.push_button_callback_if import PushButtonCallbackIf
from hardware_io.buttons.push_button_if import PushButtonIf
from hardware_io.buttons.push_button_state import PushButtonState


class RpiGpioPushButton(PushButtonIf):
    """Pushbutton connected to a Raspberry Pi GPIO input.

    The button may be wired as either active-low or active-high.

    For the typical active-low configuration, connect one switch terminal
    to the GPIO input and the other switch terminal to ground. The internal
    pull-up resistor is enabled automatically.
    """

    def __init__(
        self,
        gpio_pin: int,
        callback: PushButtonCallbackIf | None = None,
        *,
        active_low: bool = True,
        debounce_seconds: float = 0.05,
    ) -> None:
        """Initialize the GPIO pushbutton.

        Args:
            gpio_pin: BCM GPIO pin number.
            callback: Optional callback object for press and release events.
            active_low: True when pressing the button connects GPIO to ground.
            debounce_seconds: Time during which repeated transitions are ignored.

        Raises:
            ValueError: If gpio_pin or debounce_seconds is invalid.
        """
        if gpio_pin < 0:
            raise ValueError("gpio_pin must be non-negative")

        if debounce_seconds < 0:
            raise ValueError("debounce_seconds must be non-negative")

        self._gpio_pin = gpio_pin
        self._callback = callback
        self._active_low = active_low
        self._debounce_seconds = debounce_seconds

        self._button: Button | None = None
        self._lock = Lock()

    def start(self) -> None:
        """Configure the GPIO input and begin monitoring button events."""
        with self._lock:
            if self._button is not None:
                return

            pull_up = self._active_low

            self._button = Button(
                pin=self._gpio_pin,
                pull_up=pull_up,
                active_state=None,
                bounce_time=self._debounce_seconds,
            )

            self._button.when_pressed = self._handle_pressed
            self._button.when_released = self._handle_released

    def stop(self) -> None:
        """Stop monitoring and release the GPIO resource."""
        with self._lock:
            button = self._button
            self._button = None

        if button is None:
            return

        button.when_pressed = None
        button.when_released = None
        button.close()

    def get_state(self) -> PushButtonState:
        """Return the current physical state of the button.

        Raises:
            RuntimeError: If the pushbutton has not been started.
        """
        with self._lock:
            button = self._button

        if button is None:
            raise RuntimeError("Pushbutton has not been started")

        if button.is_pressed:
            return PushButtonState.PRESSED

        return PushButtonState.RELEASED

    def set_callback(
        self,
        callback: PushButtonCallbackIf | None,
    ) -> None:
        """Set or clear the callback object."""
        with self._lock:
            self._callback = callback

    def _handle_pressed(self) -> None:
        """Forward a GPIO press event to the configured callback."""
        with self._lock:
            callback = self._callback

        if callback is not None:
            callback.pressed()

    def _handle_released(self) -> None:
        """Forward a GPIO release event to the configured callback."""
        with self._lock:
            callback = self._callback

        if callback is not None:
            callback.released()

    def __enter__(self) -> RpiGpioPushButton:
        """Start the pushbutton when entering a context."""
        self.start()
        return self

    def __exit__(self, *_: object) -> None:
        """Stop the pushbutton when leaving a context."""
        self.stop()
