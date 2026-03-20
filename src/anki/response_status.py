from enum import Enum
from typing import final, override

from src.components.user_information import InfoType


class ResponseStatus(Enum):
    SUCCESS = "Success"
    MISSING_ERROR_FIELD = "AnkiConnect Error - Missing error field in response"
    MISSING_RESULT_FIELD = "AnkiConnect Error - Missing result field in response"
    ERROR_REPORTED = "Error"


@final
class ResponseInfo:
    def __init__(
        self,
        status: ResponseStatus,
        message: str | None = None,
        info_type: InfoType = InfoType.DANGER,
    ):
        self.status = status
        self.info_type = info_type
        # Use the enum's value as default message if it's a string and no message is provided
        if message is None:
            self.message = status.value
        else:
            self.message = message

    @override
    def __repr__(self) -> str:
        return f"ResponseInfo(status={self.status.name}, message='{self.message}'), response_type={self.info_type})"


@final
class DecksResponse:
    def __init__(self, info: ResponseInfo, decks: list[str] | None = None):
        self.info = info
        self.decks = decks

    @override
    def __repr__(self) -> str:
        return f"DecksResponse(info={self.info}, decks={self.decks})"


@final
class AddNoteResponse:
    def __init__(self, info: ResponseInfo, note_id: int | None = None):
        self.info = info
        self.note_id = note_id

    @override
    def __repr__(self) -> str:
        return f"AddNoteResponse(info={self.info}, note_id={self.note_id})"
