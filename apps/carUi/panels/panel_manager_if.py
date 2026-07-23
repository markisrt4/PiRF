from abc import ABC, abstractmethod
import tkinter as tk
from collections.abc import Callable
from typing import Any

from apps.carUi.input import PanelEncoderCallbacks


class PanelManagerIf(ABC):
    def __init__(self, app: Any) -> None:
        self.app = app

    @abstractmethod
    def show(self) -> None:
        pass

    def prepare_panel(self, title: str) -> bool:
        self.clear_encoder_callbacks()

        navigation = getattr(self.app, "navigation", None)
        if navigation is not None:
            navigation.clear_content()
        else:
            self.app._clear_content()

        self.set_title(title)
        self.app.top_bar.show_back_button()
        return True

    def set_encoder_callbacks(
        self,
        *,
        rotated: Callable[[int, int], None] | None = None,
        button_pressed: Callable[[int], None] | None = None,
        button_released: Callable[[int], None] | None = None,
    ) -> None:
        """
        Route non-volume encoder events to this panel while it is displayed.

        Rotation callbacks receive the contextual encoder slot and signed step
        count. Button callbacks receive the contextual encoder slot.
        """
        setter = getattr(self.app, "set_panel_encoder_callbacks", None)
        if setter is None:
            return

        setter(
            PanelEncoderCallbacks(
                rotated=rotated,
                button_pressed=button_pressed,
                button_released=button_released,
            )
        )

    def clear_encoder_callbacks(self) -> None:
        clear = getattr(self.app, "clear_panel_encoder_callbacks", None)
        if clear is not None:
            clear()

    def set_title(self, title: str) -> None:
        if hasattr(self.app, "set_panel_title"):
            self.app.set_panel_title(title)
        else:
            self.app.top_bar.set_title(title)

    def set_status(self, message: str) -> None:
        status_bar = getattr(self.app, "status_bar", None)
        if status_bar is not None:
            status_bar.set_status(message)
        else:
            self.app.status_var.set(message)

    @property
    def content_frame(self) -> tk.Frame:
        return self.app.content_frame

    @property
    def remote_display(self) -> str:
        return self.app.remote_display

    def create_tile(
        self,
        parent: tk.Widget,
        key: str,
        label: str,
        subtitle: str,
        detail: str,
    ) -> tk.Frame:
        return self.app.create_subpanel_tile(parent, key, label, subtitle, detail)
