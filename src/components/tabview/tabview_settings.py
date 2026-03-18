import datetime
from enum import Enum
from pathlib import Path
from typing import cast

import customtkinter as ctk
from odf import teletype
from odf.draw import Frame
from odf.draw import Image as odfImage
from odf.opendocument import load
from odf.text import P
from PIL.Image import Image

from src.anki.connect_anki import Anki
from src.anki.response_status import ResponseStatus
from src.components.basic_widgets import CommonLabel, OptionMenu
from src.components.user_information import InfoMessage, InfoType

from src.settings import Colors
from src.components.tabview.export_files import ExtendFile, Extension, NewFile
from src.components.tabview.tabview_utils import SettingsButtons


class ExportOptions(Enum):
    NEW = "Create new file"
    EXTEND = "Extend previously created file"
    ANKI = "Export to Anki deck"


class Settings(ctk.CTkTabview):
    def __init__(self, parent, back_func, help_func):
        super().__init__(
            master=parent,
            fg_color=Colors.SETTINGS_BG,
            segmented_button_fg_color=Colors.SETTINGS_SEGMENTED_BG,
            segmented_button_selected_color=Colors.SETTINGS_SELECTED_BUTTON,
            segmented_button_unselected_color=Colors.SETTINGS_SEGMENTED_BG,
            segmented_button_selected_hover_color=Colors.BUTTON_HOVER,
            segmented_button_unselected_hover_color=Colors.BUTTON_HOVER,
        )
        self.left_menu = parent
        # help window not visible at creation
        self.help_window = None

        # tabs
        self.add("Navigate")
        self.add("Help")

        # buttons for going back to main menu and getting help instructions
        SettingsButtons(
            self.tab("Navigate"),
            "Back to main menu",
            back_func,
        ).pack(expand=True)
        SettingsButtons(
            self.tab("Help"),
            "Help",
            help_func,
        ).pack(expand=True)

        # data
        self.file_path_string = ctk.StringVar()
        self.dir_path_string = ctk.StringVar()
        self.file_name_string = ctk.StringVar()

        # chosing export option
        self.export_option_string = ctk.StringVar(value=ExportOptions.ANKI.value)

        # anki deck option
        self.anki_deck_string = ctk.StringVar()

        self.place(rely=0.75, relx=0, relheight=0.25, relwidth=1)

    def create_button(self, tab: str, text: str, func):
        return SettingsButtons(self.tab(tab), text, func)

    def add_section_for_export(self, image: Image):
        # save image to later export it
        self.image = image

        # create new tab to export answer to a markdown/odt file
        self.add("Export")

        self.export_frame = ctk.CTkFrame(self.tab("Export"))
        self.export_frame.place(
            relx=0.5, rely=0.5, relheight=0.7, relwidth=0.5, anchor="center"
        )

        CommonLabel(self.export_frame, "Select export method:").pack(
            pady=5, expand=True
        )
        export_values = [option.value for option in ExportOptions]
        self.option_menu = OptionMenu(
            self.export_frame, self.export_option_string, export_values
        )

        SettingsButtons(
            self.export_frame,
            "Submit choice",
            self.choose_export_option,
        ).pack(expand=True)

    def choose_export_option(self):
        self.remove_options_layout()
        if self.export_option_string.get() == ExportOptions.NEW.value:
            self.new_file_layout()
        elif self.export_option_string.get() == ExportOptions.EXTEND.value:
            self.extend_file_layout()
        elif self.export_option_string.get() == ExportOptions.ANKI.value:
            self.anki_layout()

    def remove_options_layout(self):
        cast(SettingsButtons, self.option_menu).pack_forget()
        self.remove_children_from_export_frame()

    def remove_children_from_export_frame(self):
        for child in self.export_frame.winfo_children():
            child.destroy()
        # cast(SettingsButtons, self.export_frame).place_forget()

    def anki_layout(self):
        self.anki_connection = Anki()
        decks = self.anki_connection.get_decks()
        InfoMessage(
            self.left_menu.master,
            decks.info.message,
            decks.info.info_type,
        )
        if decks.info.status != ResponseStatus.SUCCESS:
            # restart export
            self.remove_children_from_export_frame()
            self.delete("Export")
            self.add_section_for_export(self.image)
            return

        CommonLabel(self.export_frame, "Select deck:").pack(pady=5, expand=True)

        self.anki_decks = OptionMenu(
            self.export_frame, self.anki_deck_string, decks.decks
        )

        SettingsButtons(
            self.export_frame,
            "Add new note",
            self.add_new_anki_note,
        ).pack(expand=True)

    def new_file_layout(self):
        NewFile(
            self.tab(
                "Export",
            ),
            self.dir_path_string,
            self.file_name_string,
            self.export_solution,
            self.left_menu.master,
        )

    def extend_file_layout(self):
        ExtendFile(
            self.tab("Export"),
            self.file_path_string,
            self.export_solution,
            self.left_menu.master,
        )

    def add_new_anki_note(self):
        answer_text = self.left_menu.textbox.get("0.0", "end")
        response = self.anki_connection.add_note(
            self.anki_deck_string.get(), self.image, answer_text
        )

        # display message for the user if something went wrong or request was successful
        InfoMessage(
            self.left_menu.master,
            f"{response.info.message}\nNote ID: {response.note_id}",
            response.info.info_type,
        )
        if response.info.status == ResponseStatus.SUCCESS:
            self.remove_children_from_export_frame()
            self.delete("Export")

    def export_solution(self, full_path: str, ext: Extension):
        # have to first save img in chosen dir to use it in libreoffice or markdown
        path = Path(full_path)
        path.parent.mkdir(
            parents=True, exist_ok=True
        )  # Ensure the parent directory exists

        # Generate unique filename for the image in the same directory
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        full_image_path = path.parent / f"image_{timestamp}.png"
        self.image.save(full_image_path)
        text_to_write = self.left_menu.textbox.get("0.0", "end")

        try:
            match ext:
                case Extension.ODT.value:
                    self.odt_export(path, text_to_write, full_image_path)
                case Extension.MD.value:
                    self.md_export(path, text_to_write, full_image_path)
                case _:
                    raise Exception
        except Exception:
            InfoMessage(
                self.left_menu.master,
                "Something went wrong while exporting",
                InfoType.DANGER,
            )
            return

        # message of success
        InfoMessage(self.left_menu.master, "Successfully saved file", InfoType.SUCCESS)

        self.remove_children_from_export_frame()
        self.delete("Export")

    def md_export(self, path: Path, text_to_write: str, image_path: Path):
        # Prepare the markdown content to append
        markdown_content = f"![Image]({image_path})\n\n"
        markdown_content += text_to_write + "\n"

        # Append to existing file or create new
        with path.open("a", encoding="utf-8") as md_file:
            md_file.write(markdown_content)

    def odt_export(self, path: Path, text_to_write: str, image_path: Path):
        try:
            textdoc = load(path)
            p_img = P()
            textdoc.text.addElement(p_img)  # pyright: ignore[reportAttributeAccessIssue]
            photoframe = Frame(
                width=f"{self.image.size[0] / 2}pt",
                height=f"{self.image.size[1] / 2}pt",
                anchortype="paragraph",
            )
            href = textdoc.addPicture(image_path)
            photoframe.addElement(odfImage(href=href))
            p_img.addElement(photoframe)
            # adding text
            paragraph = P()
            teletype.addTextToElement(
                paragraph,
                text_to_write,
            )
            textdoc.text.addElement(paragraph)  # pyright: ignore[reportAttributeAccessIssue]
            textdoc.save(path)

            # remove img
            image_path.unlink(missing_ok=True)
        except Exception as err:
            raise err
