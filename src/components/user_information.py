from enum import Enum
from typing import TYPE_CHECKING, final

import customtkinter as ctk

if TYPE_CHECKING:
    from src.app import App
from src.components.basic_widgets import CommonLabel
from src.settings import AlertsColors, Fonts


class InfoType(Enum):
    SUCCESS = AlertsColors.SUCCESS
    DANGER = AlertsColors.DANGER
    INFO = AlertsColors.INFO


@final
class InfoMessage(ctk.CTkFrame):
    def __init__(
        self,
        parent: "ctk.CTkFrame | App",
        message: str,
        info_type: InfoType,
        auto_destroy_after: int = 5000,
    ):
        """
        Creates an information window that auto-destroys after a specified time

        Parameters:
        parent -- Parent widget
        message -- Message to display
        type -- Type of information (SUCCESS, DANGER, INFO)
        auto_destroy_after -- Time in milliseconds before auto-destruction (default: 5000ms/5s)
        """
        super().__init__(master=parent, fg_color="transparent")

        # Container with rounded corners
        container = ctk.CTkButton(
            master=self,
            corner_radius=20,
            fg_color=info_type.value["bg"],
            hover_color=info_type.value["bg"],
            text=" ",
            state="disabled",
        )
        container.place(x=0, y=0, relwidth=1, relheight=1)

        # Message label
        self.message_label = CommonLabel(self, text=message)
        self.message_label.configure(
            font=ctk.CTkFont(
                family=Fonts.NORMAL,
                size=Fonts.NORMAL_SIZE,
                weight="bold",
            ),
            text_color=info_type.value["text"],
            fg_color=info_type.value["bg"],
        )
        self.message_label.place(
            relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9
        )

        # Close button (X) in top right corner
        self.close_button = ctk.CTkButton(
            master=self,
            text="X",
            width=25,
            height=25,
            corner_radius=0,
            fg_color=info_type.value["bg"],
            bg_color=info_type.value["bg"],
            hover_color="#fff",
            text_color=info_type.value["text"],
            font=ctk.CTkFont(weight="bold"),
            command=self.destroy_window,
            border_width=0,
        )
        self.close_button.place(relx=0.95, rely=0.15, anchor="center")

        # Position the window
        self.place(rely=0.01, relx=0.01, relheight=0.1, relwidth=0.43)

        # Schedule auto-destruction
        self.after_id = self.after(auto_destroy_after, self.destroy_window)

    def destroy_window(self):
        """Destroy the window and cancel any pending auto-destruction"""
        if hasattr(self, "after_id") and self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None  # Clean up the reference
        self.destroy()
