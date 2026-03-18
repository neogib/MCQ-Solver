from typing import final

import customtkinter as ctk
from PIL.Image import Image

from .components.main_frames import (
    LeftMenu,
    MainContent,
)
from .components.start_menu import StartMenu
from .settings import Geometry
from .windows.help_window import HelpWindow


@final
class App(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("dark")
        super().__init__()
        self.title("MayaBD")
        width = Geometry.MAIN[0]
        height = Geometry.MAIN[1]
        half_width = int(
            (self.winfo_screenwidth() / Geometry.MONITORS / 2) - (width / 2)
        )
        half_height = int((self.winfo_screenheight() / 2) - (height / 2))
        self.geometry(f"{width}x{height}+{half_width}+{half_height}")
        self.minsize(width, height)

        self.columnconfigure(
            (0, 1, 2, 3, 4),
            weight=1,
            uniform="a",
        )
        self.rowconfigure(
            0,
            weight=1,
            uniform="b",
        )
        self.help_window: None | HelpWindow = None
        self.main_content: MainContent | None = None
        self.left_menu: LeftMenu | None = None

        # start widgets
        self.start_menu = StartMenu(
            self,
            self.exam_layout,
            self.help,
        )

        self.mainloop()

    def exam_layout(self):
        self.start_menu.place_forget()

        # main_content widgets on the right side - title + image import
        self.main_content = MainContent(self)

        # left menu widgets - settings + textbox
        self.left_menu = LeftMenu(self, self.back_to_main_menu, self.help)

    def help(self):
        if self.help_window is None:
            self.help_window = HelpWindow(
                self
            )  # create window if its None or destroyed
        else:
            self.help_window.attributes(
                "-topmost",
                True,
            )

    def back_to_main_menu(
        self,
    ):
        assert self.main_content is not None
        assert self.left_menu is not None
        self.main_content.grid_forget()
        self.left_menu.grid_forget()

        self.start_menu = StartMenu(
            self,
            self.exam_layout,
            self.help,
        )

    def paste_next_question_button(self):
        assert self.left_menu is not None
        self.left_menu.add_paste_next_question_button(self.reset_elements)

    def export_settings_section(self, image: Image):
        assert self.left_menu is not None
        self.left_menu.settings.add_section_for_export(image)

    def provide_solution(self, solution: str):
        assert self.left_menu is not None
        self.left_menu.add_solution(solution)

    def reset_elements(self):
        assert self.main_content is not None
        assert self.left_menu is not None
        self.main_content.destroy()
        self.left_menu.reset()

        # create new main content
        self.main_content = MainContent(self)
