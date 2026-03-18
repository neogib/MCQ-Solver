from typing import TYPE_CHECKING, cast

import customtkinter as ctk
from PIL import Image, ImageGrab, ImageTk, UnidentifiedImageError

from src.components.user_information import InfoMessage, InfoType

from src.settings import Colors
from src.components.basic_widgets import CommonLabel
from src.components.tabview.tabview_settings import SettingsButtons

if TYPE_CHECKING:
    from src.app import App


class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, main_window: "App"):
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
        self.bind("<Motion>", lambda _: self.focus_set())
        self.bind("<Leave>", lambda _: self.main_window.focus_set())
        self.main_window.bind(
            "<Control-KeyPress-v>",
            self.paste_image,
        )

        # place in mainContent with 50% height
        self.place(rely=0.08, relx=0, relheight=0.5, relwidth=1)

    def open_dialog(self):
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
        _=None,
        path=None,
    ):
        if self.focus_get() == self:
            # working on image
            try:
                self.image = Image.open(path) if path else ImageGrab.grabclipboard()
            except UnidentifiedImageError:
                InfoMessage(
                    self.main_content.master,
                    "Unsupported image format\nOR\nNo image found in clipboard",
                    InfoType.INFO,
                )
                return
            if not self.image:
                InfoMessage(
                    self.main_content.master,
                    "No image found in clipboard",
                    InfoType.INFO,
                )
                return
            self.image_ratio = self.image.size[0] / self.image.size[1]
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

    def resize_image(self, event):
        self.canvas_ratio = event.width / event.height
        self.canvas_width = event.width
        self.canvas_height = event.height
        # checking is image ratio bigger than canvas ratio (which means i need to adjust width, image height will automatically be smaller than canvas height) or smaller than canvas ratio
        if self.image_ratio > self.canvas_ratio:
            self.image_width = event.width
            self.image_height = self.image_width / self.image_ratio
        else:
            self.image_height = event.height
            self.image_width = self.image_height * self.image_ratio
        self.place_image()

    def place_image(self):
        # resizing image
        resized_image = cast(Image.Image, self.image).resize(
            (
                int(self.image_width),
                int(self.image_height),
            )
        )
        self.image_tk = ImageTk.PhotoImage(image=resized_image)

        # placing image
        cast(ImageOutput, self.image_output).create_image(
            self.canvas_width / 2,
            self.canvas_height / 2,
            image=self.image_tk,
        )


class ImageOutput(ctk.CTkCanvas):
    def __init__(self, parent, resize_image_func):
        super().__init__(
            master=parent,
            background=Colors.IMAGE_FRAME,
            highlightthickness=0,
        )

        self.pack(expand=True, fill="both")
        self.bind("<Configure>", resize_image_func)
