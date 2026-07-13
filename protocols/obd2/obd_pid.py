from __future__ import annotations

from typing import Protocol, TypeVar


T = TypeVar("T")


class ObdPid(Protocol[T]):
    """
    Interface for decoding an OBD-II PID response.
    """

    @property
    def pid(self) -> int:
        ...

    def decode(self, data: bytes) -> T | None:
        ...


def byte_at(data: bytes, index: int) -> int:
    try:
        return data[index]
    except IndexError:
        raise ValueError(
            f"OBD-II response does not contain byte {index}"
        ) from None
