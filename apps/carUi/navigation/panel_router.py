from __future__ import annotations

from collections.abc import Callable


class PanelRouter:
    """Route navigation keys to registered screen actions."""

    def __init__(self) -> None:
        self._routes: dict[str, Callable[[], None]] = {}

    def register(
        self,
        key: str,
        action: Callable[[], None],
        *,
        replace: bool = False,
    ) -> None:
        normalized_key = key.strip()
        if not normalized_key:
            raise ValueError("Route key must not be empty")

        if normalized_key in self._routes and not replace:
            raise ValueError(f"Route already registered: {normalized_key}")

        self._routes[normalized_key] = action

    def register_many(
        self,
        routes: dict[str, Callable[[], None]],
        *,
        replace: bool = False,
    ) -> None:
        for key, action in routes.items():
            self.register(key, action, replace=replace)

    def open(self, key: str) -> None:
        try:
            action = self._routes[key]
        except KeyError as exc:
            available = ", ".join(sorted(self._routes)) or "<none>"
            raise KeyError(
                f"No navigation route registered for '{key}'. "
                f"Available routes: {available}"
            ) from exc

        action()

    def contains(self, key: str) -> bool:
        return key in self._routes

    def keys(self) -> tuple[str, ...]:
        return tuple(self._routes.keys())
