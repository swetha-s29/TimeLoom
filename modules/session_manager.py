import json
import uuid
from pathlib import Path

SESSIONS_DIR = Path("data/sessions")
SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


def create_session() -> str:
    session_id = str(uuid.uuid4())
    session_file = SESSIONS_DIR / f"{session_id}.json"

    with open(session_file, "w", encoding="utf-8") as f:
        json.dump({"history": []}, f)

    return session_id


def load_session(session_id: str) -> dict:
    session_file = SESSIONS_DIR / f"{session_id}.json"
    if not session_file.exists():
        return {"history": []}

    with open(session_file, "r", encoding="utf-8") as f:
        return json.load(f)


def update_session(session_id: str, user_input: str, response: str, max_turns: int = 3):
    session = load_session(session_id)

    session["history"].append({
        "user": user_input,
        "assistant": response
    })

    # Keep only last N turns
    session["history"] = session["history"][-max_turns:]

    session_file = SESSIONS_DIR / f"{session_id}.json"
    with open(session_file, "w", encoding="utf-8") as f:
        json.dump(session, f, indent=2)
        
def export_session(session_id: str) -> str:
    session_file = SESSIONS_DIR / f"{session_id}.json"
    if not session_file.exists():
        raise FileNotFoundError("Session not found")

    export_path = SESSIONS_DIR / f"{session_id}_export.json"
    export_path.write_text(session_file.read_text(), encoding="utf-8")

    return str(export_path)
