import customtkinter as ctk

from src.settings import Colors, Fonts


class Title(ctk.CTkLabel):
    def __init__(self, parent: ctk.CTkFrame):
        super().__init__(
            master=parent,
            text="IT exam auto solutions",
            font=ctk.CTkFont(
                family=Fonts.TITLE,
                size=Fonts.TITLE_SIZE,
                slant="italic",
                weight="bold",
            ),
        )

        self.place(rely=0, relx=0, relheight=0.07, relwidth=1)


class Text(ctk.CTkTextbox):
    def __init__(self, parent: ctk.CTkFrame | ctk.CTkToplevel):
        super().__init__(
            master=parent,
            wrap="word",
            fg_color=Colors.TEXTBOX,
            font=ctk.CTkFont(
                family=Fonts.NORMAL, size=Fonts.NORMAL_SIZE, weight="normal"
            ),
            border_color=Colors.BORDER_TEXTBOX,
            border_width=2,
            border_spacing=10,
            corner_radius=15,
        )


class CommonLabel(ctk.CTkLabel):
    def __init__(self, parent: ctk.CTkFrame | ctk.CTkToplevel, text: str):
        super().__init__(
            master=parent,
            text=text,
            font=ctk.CTkFont(
                family=Fonts.NORMAL, size=Fonts.NORMAL_SIZE, weight="normal"
            ),
        )


class RadioButton(ctk.CTkRadioButton):
    def __init__(
        self, parent: ctk.CTkFrame, text: str, variable: ctk.StringVar, value: str
    ):
        super().__init__(
            master=parent,
            text=text,
            font=ctk.CTkFont(
                family=Fonts.NORMAL, size=Fonts.NORMAL_SIZE, weight="normal"
            ),
            variable=variable,
            value=value,
            fg_color=Colors.BUTTON,
            hover_color=Colors.BUTTON_HOVER,
        )
        self.variable: ctk.StringVar = variable


class OptionMenu(ctk.CTkOptionMenu):
    def __init__(
        self, parent: ctk.CTkFrame, variable: ctk.StringVar, values: list[str]
    ):
        super().__init__(
            master=parent,
            variable=variable,
            values=values,
            fg_color=Colors.SETTINGS_SEGMENTED_BG,
            button_color=Colors.SETTINGS_SEGMENTED_BG,
            button_hover_color=Colors.BUTTON_HOVER,
            dropdown_fg_color=Colors.SETTINGS_SEGMENTED_BG,
            dropdown_hover_color=Colors.BUTTON_HOVER,
        )
        self.pack(expand=True)
