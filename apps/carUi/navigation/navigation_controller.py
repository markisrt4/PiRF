from __future__ import annotations
from __future__ import annotations

import tkinter as tk
from collections.abc import Callable

from apps.carUi.panels.top_bar_panel import TopBarPanel


class NavigationController:
    """Own Car UI content transitions and top-bar navigation state."""

    def __init__(
        self,
        content_frame: tk.Frame,
        top_bar: TopBarPanel,
        set_status: Callable[[str], None],
    ) -> None:
        self._content_frame = content_frame
        self._top_bar = top_bar
        self._set_status = set_status

    @property
    def content_frame(self) -> tk.Frame:
        return self._content_frame

    def clear_content(self) -> None:
        for child in self._content_frame.winfo_children():
            child.destroy()

    def show_root(
        self,
        *,
        title: str,
        builder: Callable[[], None],
        status: str,
        root_target: Callable[[], None],
    ) -> None:
        self.clear_content()
        self._top_bar.set_title(title)
        self._top_bar.set_back_command(root_target)
        self._top_bar.hide_back_button()
        builder()
        self._set_status(status)

    def show_screen(
        self,
        *,
        title: str,
        builder: Callable[[], None],
        status: str,
        back_target: Callable[[], None],
    ) -> None:
        self.clear_content()
        self._top_bar.set_title(title)
        self._top_bar.set_back_command(back_target)
        self._top_bar.show_back_button()
        builder()
        self._set_status(status)
