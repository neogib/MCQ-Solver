from pathlib import Path
from typing import TYPE_CHECKING, cast

import customtkinter as ctk
from dotenv import dotenv_values
from openai import OpenAI
from PIL.Image import Image

from src.components.basic_widgets import Text
from src.components.user_information import InfoMessage, InfoType
from src.utils.image_processing import encode_pil_image

if TYPE_CHECKING:
    from src.components.main_frames import MainContent

from ..settings import PROMPT_EXPLANATION, Colors, Fonts, Geometry

if TYPE_CHECKING:
    from ..app import App


class SolutionButton(ctk.CTkButton):
    def __init__(
        self,
        parent: "MainContent",
        text: str,
        image: Image,
        main_window: "App",
        question_editor: Text,
        mode: ctk.StringVar,
    ):
        super().__init__(
            master=parent,
            text=text,
            command=self.generate_solution,
            fg_color=Colors.BUTTON,
            hover_color=Colors.BUTTON_HOVER,
            font=ctk.CTkFont(
                family=Fonts.ANSWER,
                size=Fonts.ANSWER_SIZE,
                weight="bold",
            ),
            corner_radius=Geometry.CORNER_RADIUS,
        )
        self.parent = parent
        self.main_window = main_window
        self.image = image
        self.question_editor = question_editor
        self.mode = mode
        # .env file - API KEY for OpenRuoter
        current_file = Path(__file__)
        project_root = current_file.parent.parent.parent
        env_path = project_root / ".env"
        self.api_key = dotenv_values(env_path)["API_KEY"]

        self.place(
            rely=0.95,
            relx=0,
            relheight=0.05,
            relwidth=1,
        )

    def generate_solution(self):
        if self.mode.get() == "text":
            text = self.question_editor.get("0.0", "end")
            prompt = f"{PROMPT_EXPLANATION}\nPytanie załączyłem jako tekst:\n {text}"
            correct_answer = self.chatbot(prompt)
        else:
            prompt = f"{PROMPT_EXPLANATION}\nPytanie załączyłem jako zdjęcie."
            base64_string = encode_pil_image(self.image)
            correct_answer = self.chatbot(prompt, base64_string)

        # TODO, when there is no answer, indicate it to user, try to use different model

        # showing solution and removing additional elements
        if correct_answer:
            self.main_window.provide_solution(correct_answer)
            # the solution was correctly generated so we can add export settings and delete this button
            self.main_window.export_settings_section(self.image)

            self.place_forget()
            self.parent.remove_elements()

    def chatbot(self, prompt: str, base64_img: str | None = None) -> str | None:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        if base64_img:
            content = [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"},
                },
            ]
        else:
            content = prompt

        completion = client.chat.completions.create(
            model="openrouter/hunter-alpha",
            messages=[{"role": "user", "content": content}],  # pyright: ignore[reportArgumentType]
            temperature=0.7,
            top_p=0.5,
        )
        if not completion.choices:
            if completion.model_extra:
                error = cast(str, completion.model_extra["error"]["message"])
                InfoMessage(
                    self.parent.main_window,
                    f"Chatbot error:\n {error}",
                    InfoType.DANGER,
                )
                return None
            InfoMessage(
                self.parent.main_window,
                "Chatbot error: No answer",
                InfoType.DANGER,
            )
            return None

        return completion.choices[0].message.content
