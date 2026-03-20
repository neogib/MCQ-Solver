from collections.abc import Callable
from tkinter import Event, Misc
from typing import TYPE_CHECKING, cast, final

import customtkinter as ctk
from PIL import Image, ImageGrab, ImageTk, UnidentifiedImageError

from src.components.basic_widgets import CommonLabel
from src.components.tabview.tabview_utils import SettingsButtons
from src.components.user_information import InfoMessage, InfoType
from src.settings import Colors

if TYPE_CHECKING:
    from src.app import App
    from src.components.main_frames import MainContent


# helper function for calculating new size of image, so it will fit in canvas and will keep its aspect ratio
def calculate_new_size(
    image_width: int,
    image_height: int,
    canvas_width: int,
    canvas_height: int,
) -> tuple[int, int]:
    image_ratio = image_width / image_height
    canvas_ratio = canvas_width / canvas_height
    if (
        image_ratio > canvas_ratio
    ):  # if image ratio is bigger than canvas ratio, it means that we need to adjust width, because if we adjust height, image will be wider than canvas
        new_image_width = canvas_width
        new_image_height = new_image_width / image_ratio
    else:
        new_image_height = canvas_height
        new_image_width = new_image_height * image_ratio
    return int(new_image_width), int(new_image_height)


@final
class ImageImport(ctk.CTkFrame):
    def __init__(self, parent: "MainContent", main_window: "App") -> None:
        super().__init__(master=parent, fg_color=Colors.IMAGE_FRAME)
        self.main_content = parent
        self.main_window = main_window

        # creating attribute image_output for later usage when image will be pasted
        self.image_output: ImageOutput | None = None

        # widgets
        self.button_import = SettingsButtons(self, "Import image", self.open_dialog)

        self.label_paste = CommonLabel(
            self, "or just paste an image from clipboard (press Ctrl-V)"
        )
        self.button_import.place(relx=0.5, rely=0.4, anchor="center")
        self.label_paste.place(relx=0.5, rely=0.6, anchor="center")
        # binding
        self.bind("<Motion>", lambda _: self.focus_set())  # pyright: ignore[reportUnknownLambdaType]
        self.bind("<Leave>", lambda _: self.main_window.focus_set())  # pyright: ignore[reportUnknownLambdaType]
        self.main_window.bind(
            "<Control-KeyPress-v>",
            self.paste_image,
        )

        # place in mainContent with 50% height
        self.place(rely=0.08, relx=0, relheight=0.5, relwidth=1)

        # later used instance variables
        self.image: Image.Image | None = None
        self.image_tk: ImageTk.PhotoImage | None = None

    def open_dialog(self) -> None:
        path = ctk.filedialog.askopenfilename(
            filetypes=(),
            title="Choose image",
            initialdir="/home",
        )
        if path:
            self.focus_set()
            self.paste_image(path=path)

    def paste_image(
        self,
        _: "Event[Misc] | None" = None,
        path: str | None = None,
    ) -> None:
        if self.focus_get() == self:
            # working on image
            try:
                img = Image.open(path) if path else ImageGrab.grabclipboard()
                if isinstance(
                    img, list
                ):  # if list of filenames is returned, we raise the error, because we want only one image
                    raise UnidentifiedImageError
                self.image = img
            except UnidentifiedImageError:
                InfoMessage(
                    cast(ctk.CTkFrame, self.main_content.master),
                    "Unsupported image format\nOR\nNo image found in clipboard",
                    InfoType.INFO,
                )
                return
            if not self.image:
                InfoMessage(
                    cast(ctk.CTkFrame, self.main_content.master),
                    "No image found in clipboard",
                    InfoType.INFO,
                )
                return
            self.image_tk = ImageTk.PhotoImage(image=self.image)

            # working on layout
            self.button_import.place_forget()
            self.label_paste.place_forget()

            self.image_output = ImageOutput(
                self,
                self.resize_image,
            )
            self.main_content.add_elements(self.image)  # add edit box, answer button
            self.main_window.paste_next_question_button()

    def resize_image(self, event: "Event[Misc]") -> None:
        assert self.image is not None
        assert self.image_output is not None
        image_width, image_height = calculate_new_size(
            self.image.width, self.image.height, event.width, event.height
        )
        # resizing image
        resized_image = self.image.resize(
            (
                int(image_width),
                int(image_height),
            )
        )
        self.image_tk = ImageTk.PhotoImage(image=resized_image)

        # placing image
        self.image_output.create_image(
            event.width / 2,
            event.height / 2,
            image=self.image_tk,
        )


class ImageOutput(ctk.CTkCanvas):
    def __init__(
        self,
        parent: ImageImport,
        resize_image_func: Callable[["Event[Misc]"], None],
    ) -> None:
        super().__init__(
            master=parent,
            background=Colors.IMAGE_FRAME,
            highlightthickness=0,
        )

        self.pack(expand=True, fill="both")
        self.bind("<Configure>", resize_image_func)
