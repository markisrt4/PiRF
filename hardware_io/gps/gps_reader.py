from __future__ import annotations

import logging
import threading
from collections.abc import Callable
from dataclasses import dataclass

import gps


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class GpsData:
    latitude: float | None = None
    longitude: float | None = None
    altitude: float | None = None
    speed: float | None = None
    track: float | None = None
    mode: int | None = None


GpsCallback = Callable[[GpsData], None]


class GpsReader:
    """
    Reads GPS data from gpsd.

    The reader reports GPS values as they are received. It does not apply
    application-specific behavior or interpret how the data should be used.
    """

    def __init__(
        self,
        callback: GpsCallback | None = None,
        host: str = "127.0.0.1",
        port: str = "2947",
    ) -> None:
        if callback is not None and not callable(callback):
            raise TypeError("callback must be callable")

        self._callback = callback
        self._host = host
        self._port = port

        self._session: gps.gps | None = None
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()

    @property
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def open(self) -> None:
        """
        Opens a connection to gpsd.
        """
        if self._session is not None:
            return

        self._session = gps.gps(
            host=self._host,
            port=self._port,
            mode=gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE,
        )

        LOGGER.info(
            "Connected to gpsd at %s:%s",
            self._host,
            self._port,
        )

    def close(self) -> None:
        """
        Closes the gpsd connection.
        """
        if self.is_running:
            self.stop()

        if self._session is not None:
            self._session.close()
            self._session = None

    def start(self, callback: GpsCallback | None = None) -> None:
        """
        Starts reading GPS data in a background thread.
        """
        if callback is not None:
            if not callable(callback):
                raise TypeError("callback must be callable")

            self._callback = callback

        if self._callback is None:
            raise ValueError("A callback is required before starting")

        if self.is_running:
            return

        self.open()
        self._stop_event.clear()

        self._thread = threading.Thread(
            target=self._run,
            name="GpsReader",
            daemon=True,
        )
        self._thread.start()

        LOGGER.info("GPS reader started")

    def stop(self) -> None:
        """
        Stops the GPS reader.
        """
        self._stop_event.set()

        if self._session is not None:
            self._session.close()
            self._session = None

        if (
            self._thread is not None
            and self._thread.is_alive()
            and self._thread is not threading.current_thread()
        ):
            self._thread.join(timeout=1.0)

        self._thread = None

        LOGGER.info("GPS reader stopped")

    def _run(self) -> None:
        try:
            if self._session is None:
                raise RuntimeError("GPS session is not open")

            for report in self._session:
                if self._stop_event.is_set():
                    break

                if report.get("class") != "TPV":
                    continue

                data = GpsData(
                    latitude=report.get("lat"),
                    longitude=report.get("lon"),
                    altitude=report.get("alt"),
                    speed=report.get("speed"),
                    track=report.get("track"),
                    mode=report.get("mode"),
                )

                callback = self._callback

                if callback is not None:
                    callback(data)

        except OSError:
            if not self._stop_event.is_set():
                LOGGER.exception("GPS connection failed")

        except Exception:
            if not self._stop_event.is_set():
                LOGGER.exception("Unexpected GPS reader failure")

    def __enter__(self) -> GpsReader:
        self.open()
        return self

    def __exit__(self, *_args: object) -> None:
        self.close()
