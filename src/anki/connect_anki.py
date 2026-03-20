from copy import deepcopy
from collections.abc import Mapping
from datetime import datetime
from typing import cast

import requests
from PIL.Image import Image

from src.anki.config import ADD_NOTE_REQUEST_BODY, HOST_PORT
from src.anki.payloads import AddNoteRequestPayload, AnkiResponsePayload
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
    def validate_response(data: AnkiResponsePayload, success_msg: str) -> ResponseInfo:
        error = data["error"]
        if error is not None:
            return ResponseInfo(ResponseStatus.ERROR_REPORTED, str(error))

        return ResponseInfo(ResponseStatus.SUCCESS, success_msg, InfoType.SUCCESS)

    def post_request(
        self, data: Mapping[str, object]
    ) -> ResponseInfo | AnkiResponsePayload:
        try:
            response = requests.post(self.host_port, json=data)
            response.raise_for_status()  # Raises HTTPError for bad status codes (4XX, 5XX)

            # Process the response...
            response_data = cast(object, response.json())
            if not isinstance(response_data, dict):
                return ResponseInfo(
                    ResponseStatus.ERROR_REPORTED,
                    "Invalid response format: expected JSON object.",
                )
            response_dict = cast(dict[str, object], response_data)
            if "error" not in response_dict:
                return ResponseInfo(ResponseStatus.MISSING_ERROR_FIELD)
            if "result" not in response_dict:
                return ResponseInfo(ResponseStatus.MISSING_RESULT_FIELD)
            response_payload: AnkiResponsePayload = {
                "error": response_dict["error"],
                "result": response_dict["result"],
            }

        except requests.exceptions.HTTPError as err:
            # Handle HTTP errors (status codes 4XX, 5XX)
            return ResponseInfo(
                ResponseStatus.ERROR_REPORTED, f"HTTP error occurred: {err}"
            )

        except requests.exceptions.ConnectionError:
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

        return response_payload  # the response was successful

    def get_decks(self) -> DecksResponse:
        data: dict[str, object] = {"action": "deckNames", "version": 6}

        response = self.post_request(data)
        if isinstance(response, ResponseInfo):
            return DecksResponse(info=response)

        validation = self.validate_response(
            response, success_msg="Decks were retrieved successfully"
        )  # check does response include required fields and no error
        if validation.status != ResponseStatus.SUCCESS:
            return DecksResponse(info=validation)

        decks_raw = response["result"]
        if not isinstance(decks_raw, list) or not all(
            isinstance(deck, str) for deck in decks_raw
        ):
            return DecksResponse(
                info=ResponseInfo(
                    ResponseStatus.ERROR_REPORTED,
                    "AnkiConnect returned invalid deck list format.",
                )
            )

        return DecksResponse(info=validation, decks=decks_raw)

    def add_note(self, deck: str, img: Image, answer: str) -> AddNoteResponse:
        current_date = datetime.now()
        filename = f"{current_date.strftime('%Y%m%d%H%M%S')}.jpg"
        base64_data = encode_pil_image(img)
        request_data: AddNoteRequestPayload = deepcopy(ADD_NOTE_REQUEST_BODY)

        answer = answer.replace("\n", "<br>")  # anki require <br> for new line

        # update default request body template for adding new notes
        request_data["params"]["note"]["deckName"] = deck
        request_data["params"]["note"]["picture"][0]["filename"] = filename
        request_data["params"]["note"]["picture"][0]["data"] = base64_data
        request_data["params"]["note"]["fields"]["Back"] = answer

        # make request to add new note
        response = self.post_request(cast(Mapping[str, object], request_data))

        if isinstance(response, ResponseInfo):
            return AddNoteResponse(info=response)

        validation = self.validate_response(
            response, success_msg="Note was added successfully"
        )  # check does response include required fields and no error
        if validation.status != ResponseStatus.SUCCESS:
            return AddNoteResponse(info=validation)

        note_id_raw = response["result"]
        if not isinstance(note_id_raw, int):
            return AddNoteResponse(
                info=ResponseInfo(
                    ResponseStatus.ERROR_REPORTED,
                    "AnkiConnect returned invalid note id format.",
                )
            )

        return AddNoteResponse(info=validation, note_id=note_id_raw)
