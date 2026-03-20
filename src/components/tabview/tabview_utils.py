from collections.abc import Callable

import customtkinter as ctk

from src.settings import Colors, Fonts


class SettingsButtons(ctk.CTkButton):
    def __init__(
        self, parent: ctk.CTkFrame, text: str, func: Callable[[], None] | None = None
    ):
        super().__init__(
            master=parent,
            text=text,
            command=func,
            font=ctk.CTkFont(
                family=Fonts.NORMAL, size=Fonts.NORMAL_SIZE, weight="normal"
            ),
            fg_color=Colors.BUTTON,
            hover_color=Colors.BUTTON_HOVER,
        )


class SettingsEntry(ctk.CTkEntry):
    def __init__(self, parent: ctk.CTkFrame, textvariable: ctk.Variable):
        super().__init__(
            master=parent,
            textvariable=textvariable,
            font=ctk.CTkFont(
                family=Fonts.NORMAL, size=Fonts.NORMAL_SIZE, weight="normal"
            ),
        )

        self.pack(expand=True, fill="x", padx=10, pady=5)
