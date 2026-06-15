import json
from pathlib import Path
from typing import Any, Dict

from .hashutil import sha256_json
from .timeutil import now_text

def make_receipt(*, receipt_type: str, capsule_hash: str, capsule_id: str, actor_receipt_id: str, authority_token_id: str, adapter: str, target: str, result: Dict[str, Any], role_context: Dict[str, Any] | None = None, role_enforcement: Dict[str, Any] | None = None) -> Dict[str, Any]:
    body = {
        "schema": {"name": "stegverse.stegentity.execution_receipt", "version": "0.1.0"},
        "receipt_type": receipt_type,
        "issued_at": now_text(),
        "capsule_id": capsule_id,
        "capsule_hash": capsule_hash,
        "actor_receipt_id": actor_receipt_id,
        "authority_token_id": authority_token_id,
        "adapter": adapter,
        "target": target,
        "result": result,
    }
    if role_context:
        body["role_context"] = dict(role_context)
    if role_enforcement:
        body["role_enforcement"] = dict(role_enforcement)
    body["receipt_hash"] = sha256_json(body)
    return body


def make_blocked_apply_receipt(*, capsule_hash: str, capsule_id: str, actor_receipt_id: str, authority_token_id: str, adapter: str, target: str, reason: str, blocks: list[str], role_context: Dict[str, Any] | None = None, role_enforcement: Dict[str, Any] | None = None) -> Dict[str, Any]:
    body = {
        "schema": {"name": "stegverse.stegentity.blocked_apply_receipt", "version": "0.1.0"},
        "receipt_type": "blocked_apply",
        "issued_at": now_text(),
        "capsule_id": capsule_id,
        "capsule_hash": capsule_hash,
        "actor_receipt_id": actor_receipt_id,
        "authority_token_id": authority_token_id,
        "adapter": adapter,
        "target": target,
        "reason": reason,
        "blocks": list(blocks),
        "mutation_attempted": False,
        "execution_receipt_emitted": False,
    }
    if role_context:
        body["role_context"] = dict(role_context)
    if role_enforcement:
        body["role_enforcement"] = dict(role_enforcement)
    body["receipt_hash"] = sha256_json(body)
    return body


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    tmp.replace(path)
