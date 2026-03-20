from collections.abc import Callable
from enum import Enum
from os.path import exists, isfile
from typing import final

import customtkinter as ctk
from odf.opendocument import OpenDocumentText

from src.components.basic_widgets import CommonLabel
from src.components.tabview.tabview_utils import SettingsButtons, SettingsEntry
from src.components.user_information import InfoMessage, InfoType
from src.settings import Colors


class Extension(Enum):
    ODT = "odt"
    MD = "md"


def parse_extension(value: str) -> Extension | None:
    extension = value.split(".")[-1].lower()
    if extension == Extension.ODT.value:
        return Extension.ODT
    if extension == Extension.MD.value:
        return Extension.MD
    return None


@final
class ExtendFile(ctk.CTkFrame):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        path_string: ctk.StringVar,
        export_func: Callable[[str, Extension], None],
        main_window: ctk.CTkFrame,
    ):
        super().__init__(master=parent, fg_color=Colors.SETTINGS_SEGMENTED_BG)
        self.export_func = export_func
        self.path_string = path_string
        self.main_window = main_window
        SettingsButtons(self, "Open file search", self.open_file_dialog).pack(
            expand=True, pady=5
        )
        SettingsEntry(self, self.path_string)
        SettingsButtons(self, "Save solution to a file", self.extend_file).pack(
            expand=True, pady=5
        )

        self.pack(expand=True, fill="both")

    def open_file_dialog(self):
        path = ctk.filedialog.askopenfilename(
            filetypes=(("libreoffice files", "*.odt"), ("markdown files", "*.md")),
            title="Choose file to extend",
        )
        self.path_string.set(path)

    def extend_file(self):
        if not isfile(self.path_string.get()):
            InfoMessage(
                self.main_window,
                "File does not exist",
                InfoType.DANGER,
            )
            return
        extension = parse_extension(self.path_string.get())
        if extension is None:
            InfoMessage(
                self.main_window,
                "Invalid file extension",
                InfoType.DANGER,
            )
            return
        self.export_func(self.path_string.get(), extension)


@final
class NewFile(ctk.CTkFrame):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        dir_path: ctk.StringVar,
        file_name: ctk.StringVar,
        export_func: Callable[[str, Extension], None],
        main_window: ctk.CTkFrame,
    ) -> None:
        super().__init__(master=parent, fg_color=Colors.SETTINGS_SEGMENTED_BG)
        self.dir_path = dir_path
        self.file_name = file_name
        self.export_func = export_func
        self.main_window = main_window
        NewFilePath(
            self,
            dir_path,
        )
        FileName(
            self,
            file_name,
        )
        SettingsButtons(parent, "Create new file", self.create_new_file).place(
            relx=0.5,
            rely=0.87,
            anchor="center",
        )

        # place settings in tab Export with 75% height
        self.place(
            relx=0.01,
            rely=0.01,
            relheight=0.75,
            relwidth=1,
        )

    def create_new_file(self) -> None:
        full_path = f"{self.dir_path.get()}/{self.file_name.get()}"
        extension = parse_extension(self.file_name.get())
        if extension is None:
            InfoMessage(
                self.main_window,
                "Invalid file extension",
                InfoType.DANGER,
            )
            return
        if exists(full_path):
            InfoMessage(
                self.main_window,
                "File already exists",
                InfoType.DANGER,
            )
            return

        if extension is Extension.ODT:
            textdoc = OpenDocumentText()
            textdoc.save(full_path)  # save file to later extend it
        self.export_func(full_path, extension)


@final
class NewFilePath(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, path_string: ctk.StringVar) -> None:
        super().__init__(master=parent, fg_color=Colors.SETTINGS_SEGMENTED_BG)
        self.path_string = path_string
        SettingsButtons(self, "Open directory search", self.open_dir_dialog).pack(
            pady=5, expand=True
        )
        SettingsEntry(self, self.path_string)

        self.pack(side="left", expand=True, fill="both", padx=10, pady=5)

    def open_dir_dialog(self) -> None:
        path = ctk.filedialog.askdirectory(
            title="Choose directory to create file",
            initialdir="/home",
        )
        self.path_string.set(path)


@final
class FileName(ctk.CTkFrame):
    def __init__(
        self, parent: ctk.CTkFrame, file_name_string: ctk.StringVar
    ) -> None:
        super().__init__(master=parent, fg_color=Colors.SETTINGS_SEGMENTED_BG)
        self.file_name = file_name_string
        CommonLabel(self, "Enter new file name:").pack(pady=5, expand=True)
        SettingsEntry(self, self.file_name)

        self.pack(side="left", expand=True, fill="both", padx=10, pady=5)
