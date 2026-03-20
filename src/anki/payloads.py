from typing import TypedDict


class AnkiResponsePayload(TypedDict):
    error: object | None
    result: object


class AddNotePicturePayload(TypedDict):
    filename: str | None
    data: str | None
    fields: list[str]


class AddNoteFieldsPayload(TypedDict):
    Front: str
    Back: str | None


class AddNoteOptionsPayload(TypedDict):
    allowDuplicate: bool
    duplicateScope: str


class AddNoteNotePayload(TypedDict):
    deckName: str | None
    modelName: str
    fields: AddNoteFieldsPayload
    options: AddNoteOptionsPayload
    picture: list[AddNotePicturePayload]


class AddNoteParamsPayload(TypedDict):
    note: AddNoteNotePayload


class AddNoteRequestPayload(TypedDict):
    action: str
    version: int
    params: AddNoteParamsPayload
