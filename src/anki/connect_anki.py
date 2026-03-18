from datetime import datetime

import requests
from PIL.Image import Image

from src.anki.config import ADD_NOTE_REQUEST_BODY, HOST_PORT
from src.anki.response_status import (
    AddNoteResponse,
    DecksResponse,
    ResponseInfo,
    ResponseStatus,
)
from src.components.user_information import InfoType
from src.utils.image_processing import encode_pil_image


class Anki:
    """
    This class is used to communicate with AnkiConnect plugin and add new notes to the chosen deck.
    To use it AnkiConnect Add-on plugin is required.
    """

    def __init__(self):
        self.host_port: str = HOST_PORT

    @staticmethod
    def validate_response(data: dict, success_msg: str) -> ResponseInfo:
        if (
            data.get("error", 0) == 0
        ):  # no error field, if error is missing it will become 0, if error is None everything is all right
            return ResponseInfo(ResponseStatus.MISSING_ERROR_FIELD)
        elif data.get("result", 0) == 0:
            print("response is missing required result field")
            return ResponseInfo(ResponseStatus.MISSING_RESULT_FIELD)
        elif data["error"]:
            return ResponseInfo(ResponseStatus.ERROR_REPORTED, data["error"])

        return ResponseInfo(ResponseStatus.SUCCESS, success_msg, InfoType.SUCCESS)

    def post_request(self, data: dict) -> ResponseInfo | dict:
        try:
            response = requests.post(self.host_port, json=data)
            response.raise_for_status()  # Raises HTTPError for bad status codes (4XX, 5XX)

            # Process the response...
            data = response.json()

        except requests.exceptions.HTTPError as err:
            # Handle HTTP errors (status codes 4XX, 5XX)
            return ResponseInfo(
                ResponseStatus.ERROR_REPORTED, f"HTTP error occurred: {err}"
            )

        except requests.exceptions.ConnectionError as err:
            # Handle connection errors (DNS failures, refused connections, etc)
            return ResponseInfo(
                ResponseStatus.ERROR_REPORTED,
                "Connection error occurred. \nCheck that the anki application is open and\nthat AnkiConnect is installed.",
            )
        except requests.exceptions.Timeout as err:
            # Handle timeout errors
            return ResponseInfo(
                ResponseStatus.ERROR_REPORTED, f"Timeout error occurred: {err}"
            )

        except requests.exceptions.RequestException as err:
            # Handle any other requests-related errors
            return ResponseInfo(
                ResponseStatus.ERROR_REPORTED, f"Request error occurred: {err}"
            )

        return data  # the response was successful

    def get_decks(self) -> DecksResponse:
        data = {"action": "deckNames", "version": 6}

        response = self.post_request(data)
        if isinstance(response, ResponseInfo):
            return DecksResponse(info=response)

        validation = self.validate_response(
            response, success_msg="Decks were retrieved successfully"
        )  # check does response include required fields and no error
        if validation.status != ResponseStatus.SUCCESS:
            return DecksResponse(info=validation)
        return DecksResponse(info=validation, decks=response["result"])

    def add_note(self, deck: str, img: Image, answer: str) -> AddNoteResponse:
        current_date = datetime.now()
        filename = f"{current_date.strftime('%Y%m%d%H%M%S')}.jpg"
        base64_data = encode_pil_image(img)
        request_data = ADD_NOTE_REQUEST_BODY

        answer = answer.replace("\n", "<br>")  # anki require <br> for new line

        # update default request body template for adding new notes
        request_data["params"]["note"]["deckName"] = deck
        request_data["params"]["note"]["picture"][0]["filename"] = filename
        request_data["params"]["note"]["picture"][0]["data"] = base64_data
        request_data["params"]["note"]["fields"]["Back"] = answer

        # make request to add new note
        response = self.post_request(request_data)

        if isinstance(response, ResponseInfo):
            return AddNoteResponse(info=response)

        validation = self.validate_response(
            response, success_msg="Note was added successfully"
        )  # check does response include required fields and no error
        if validation.status != ResponseStatus.SUCCESS:
            return AddNoteResponse(info=validation)
        return AddNoteResponse(info=validation, note_id=response["result"])
