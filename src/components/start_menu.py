from collections.abc import Callable

import customtkinter as ctk

from ..settings import Colors, Fonts, Geometry


class StartMenu(ctk.CTkFrame):
    def __init__(
        self,
        parent: ctk.CTk,
        start_exam_callback: Callable[[], None],
        help_callback: Callable[[], None],
    ) -> None:
        super().__init__(master=parent, fg_color="transparent")
        font = ctk.CTkFont(
            family=Fonts.ANSWER,
            size=Fonts.ANSWER_SIZE,
            weight="bold",
            slant="italic",
        )
        StartButton(self, "IT exam", start_exam_callback, font).pack(
            expand=True, ipadx=5, ipady=20, fill="x"
        )
        StartButton(self, "Help", help_callback, font).pack(
            expand=True, ipadx=5, ipady=20, fill="x"
        )

        self.place(relx=0.5, rely=0.5, relheight=0.5, relwidth=0.3, anchor="center")


class StartButton(ctk.CTkButton):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        text: str,
        command: Callable[[], None],
        font: ctk.CTkFont,
    ) -> None:
        super().__init__(
            master=parent,
            text=text,
            command=command,
            fg_color=Colors.BUTTON,
            hover_color=Colors.BUTTON_HOVER,
            font=font,
            corner_radius=Geometry.CORNER_RADIUS,
        )
