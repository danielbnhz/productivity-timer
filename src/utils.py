import time
from datetime import datetime, timezone

def now_utc_ts() -> int:
    """Unix timestamp (seconds), UTC"""
    return int(time.time())

def now_utc_iso() -> str:
    """Human-readable UTC timestamp"""
    return datetime.now(timezone.utc).isoformat()

def seconds_to_hms(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"


def generate_session_id() -> str:
    return uuid.uuid4().hex

def minutes_to_seconds(minutes: float) -> int:
    if minutes < 0:
        raise ValueError("Minutes cannot be negative")
    return int(minutes * 60)
