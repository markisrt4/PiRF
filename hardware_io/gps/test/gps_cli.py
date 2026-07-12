#!/usr/bin/env python3

import time

from hardware_io.gps import GpsData, GpsReader


def gps_data_received(data: GpsData) -> None:
    print(
        f"lat={data.latitude} "
        f"lon={data.longitude} "
        f"alt={data.altitude} "
        f"speed={data.speed} "
        f"track={data.track} "
        f"mode={data.mode}"
    )


def main() -> None:
    reader = GpsReader(callback=gps_data_received)

    try:
        reader.start()

        print("Reading GPS data from gpsd")
        print("Press Ctrl+C to exit.\n")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping GPS reader...")

    finally:
        reader.stop()


if __name__ == "__main__":
    main()
