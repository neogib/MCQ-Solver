import customtkinter as ctk
import emoji

from src.components.basic_widgets import CommonLabel, Text
from src.settings import HELP_TEXT, Fonts, Geometry


class HelpWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(master=parent)
        width = Geometry.HELP[0]
        height = Geometry.HELP[1]
        half_width = int(
            (self.winfo_screenwidth() / Geometry.MONITORS / 2) - (width / 2)
        )
        half_height = int((self.winfo_screenheight() / 2) - (height / 2))

        self.geometry(f"{width}x{height}+{half_width}+{half_height}")
        self.minsize(width, height)
        self.title("Help")

        self.help_title = CommonLabel(self, "How does this program work?")
        self.help_title.configure(
            font=ctk.CTkFont(
                family=Fonts.TITLE, size=Fonts.ANSWER_SIZE, weight="normal"
            )
        )
        self.help_title.pack(pady=5)

        self.help_text = Text(self)
        self.help_text.insert("end", HELP_TEXT)
        self.help_text.insert("end", emoji.emojize("Good luck! 	:grinning_face:"))

        self.help_text.configure(state="disabled")
        self.help_text.pack(expand=True, fill="both", padx=8, pady=5)
