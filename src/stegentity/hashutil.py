import base64
import hashlib
import json
from pathlib import Path
from typing import Any

def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()

def canonical_json(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")

def sha256_json(data: Any) -> str:
    return sha256_bytes(canonical_json(data))

def b64_to_bytes(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))

def bytes_to_b64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")
