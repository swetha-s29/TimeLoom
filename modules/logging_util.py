import json
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("data/logs")
LOG_FILE = LOG_DIR / "timeloom_logs.jsonl"

LOG_DIR.mkdir(parents=True, exist_ok=True)


def log_event(event: dict):
    event["timestamp"] = datetime.utcnow().isoformat()

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
