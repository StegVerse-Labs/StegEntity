from datetime import datetime, timezone

def parse_time(value: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError("expected RFC3339/ISO timestamp string")
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def now_text() -> str:
    return now_utc().replace(microsecond=0).isoformat().replace("+00:00", "Z")

def not_expired(expires_at: str) -> bool:
    return parse_time(expires_at) > now_utc()
