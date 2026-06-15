import json
from pathlib import Path

from src.stegentity.hashutil import bytes_to_b64, sha256_json


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def build_capsule() -> dict:
    message = "Hello from StegEntity role-context local_fs adapter.\n"
    return {
        "schema": {
            "name": "stegverse.maintenance_capsule",
            "version": "0.1.0",
        },
        "capsule_id": "demo-role-context-file-replacement-0001",
        "created_at": "2026-06-15T17:00:00Z",
        "target": {
            "adapter": "local_fs",
            "target_id": "demo_target",
        },
        "transition": {
            "transition_id": "RT-004",
            "transition_name": "Role Context File Creation",
            "transition_family": "Installation",
        },
        "role_context": {
            "actor_role": "StegAgent",
            "counterparty_role": "StegEntity",
            "role_transition": "RT-004",
            "role_constraint": "execution_requires_admissibility",
            "symmetry_basis": "receipt+tvc+capsule",
            "completion_invariant_required": True,
        },
        "admissibility": {
            "decision": "ALLOW",
            "basis": "demo role-context authority token and receipt",
        },
        "dependencies": [
            "local filesystem write permission",
        ],
        "consequences": [
            "demo_target/role_context_hello.txt will be created or replaced",
        ],
        "rollback_plan": [
            "restore from stegentity_state/backups if prior file existed",
        ],
        "verification": {
            "required": True,
            "method": "sha256_after_write",
        },
        "operations": [
            {
                "op_id": "op-write-role-context-hello",
                "operation": "create_or_replace",
                "destination": "role_context_hello.txt",
                "content_b64": bytes_to_b64(message.encode("utf-8")),
                "expected_sha256": None,
                "required_scopes": [
                    "local_fs:write",
                ],
                "description": "Write role_context_hello.txt inside demo target.",
                "allow_create": True,
                "allow_replace": True,
            }
        ],
    }


def build_receipt(capsule_hash: str) -> dict:
    return {
        "receipt_id": "demo-role-context-receipt-0001",
        "actor_class": "ai",
        "scopes": [
            "local_fs:write",
        ],
        "issued_at": "2026-06-15T17:00:01Z",
        "expires_at": "2027-01-01T00:00:00Z",
        "assurance_level": 2,
        "signals": [],
        "issuer": "stegid",
        "kid": "demo-key",
        "payload_hash": capsule_hash,
        "sig": "demo-signature-owned-by-stegid-in-production",
    }


def build_authority(capsule_hash: str) -> dict:
    return {
        "token_id": "demo-role-context-tvc-token-0001",
        "status": "ALLOW",
        "adapter": "local_fs",
        "target": "demo_target",
        "scopes": [
            "local_fs:write",
        ],
        "issued_at": "2026-06-15T17:00:01Z",
        "expires_at": "2027-01-01T00:00:00Z",
        "capsule_hash": capsule_hash,
        "receipt_hash": capsule_hash,
    }


def main() -> int:
    capsule = build_capsule()
    capsule_hash = sha256_json(capsule)
    write_json(EXAMPLES / "role_context_file_replacement_capsule.json", capsule)
    write_json(EXAMPLES / "role_context_verified_receipt.json", build_receipt(capsule_hash))
    write_json(EXAMPLES / "role_context_authority_token.json", build_authority(capsule_hash))
    print(capsule_hash)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
