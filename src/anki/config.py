from src.anki.payloads import AddNoteRequestPayload

HOST_PORT = "http://127.0.0.1:8765"
ADD_NOTE_REQUEST_BODY: AddNoteRequestPayload = {
    "action": "addNote",
    "version": 6,
    "params": {
        "note": {
            "deckName": None,
            "modelName": "KaTeX and Markdown Basic (Color)",
            "fields": {"Front": "", "Back": None},
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "deck",
            },
            "picture": [
                {
                    "filename": None,
                    "data": None,
                    "fields": ["Front"],
                }
            ],
        }
    },
}
