import base64
import json
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone

ROOT = Path(__file__).resolve().parents[1]
DEMO_ROOT = ROOT / "demo_target"
EXAMPLES = ROOT / "examples"

def iso(dt):
    return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")

def main():
    if DEMO_ROOT.exists():
        shutil.rmtree(DEMO_ROOT)
    DEMO_ROOT.mkdir(parents=True)

    message = b"Hello from StegEntity local_fs adapter.\n"
    capsule = {
        "schema": {"name": "stegverse.maintenance_capsule", "version": "0.1.0"},
        "capsule_id": "demo-local-file-replacement-0001",
        "created_at": iso(datetime.now(timezone.utc)),
        "target": {"adapter": "local_fs", "target_id": "demo_target"},
        "transition": {"transition_id": "T-120", "transition_name": "File Creation", "transition_family": "Installation"},
        "admissibility": {"decision": "ALLOW", "basis": "demo authority token and receipt"},
        "dependencies": ["local filesystem write permission"],
        "consequences": ["demo_target/hello.txt will be created or replaced"],
        "rollback_plan": ["restore from stegentity_state/backups if prior file existed"],
        "verification": {"required": True, "method": "sha256_after_write"},
        "operations": [{
            "op_id": "op-write-hello",
            "operation": "create_or_replace",
            "destination": "hello.txt",
            "content_b64": base64.b64encode(message).decode("utf-8"),
            "expected_sha256": None,
            "required_scopes": ["local_fs:write"],
            "description": "Write hello.txt inside demo target.",
            "allow_create": True,
            "allow_replace": True
        }]
    }

    EXAMPLES.mkdir(exist_ok=True)
    capsule_path = EXAMPLES / "local_file_replacement_capsule.json"
    capsule_path.write_text(json.dumps(capsule, indent=2), encoding="utf-8")

    proc = subprocess.run([sys.executable, "-m", "src.stegentity.cli", "validate", str(capsule_path)], cwd=ROOT, text=True, capture_output=True, check=True)
    capsule_hash = json.loads(proc.stdout)["capsule_hash"]

    now = datetime.now(timezone.utc)
    receipt = {
        "receipt_id": "demo-receipt-0001",
        "actor_class": "ai",
        "scopes": ["local_fs:write"],
        "issued_at": iso(now),
        "expires_at": iso(now + timedelta(minutes=30)),
        "assurance_level": 2,
        "signals": [],
        "issuer": "stegid",
        "kid": "demo-key",
        "payload_hash": capsule_hash,
        "sig": "demo-signature-owned-by-stegid-in-production"
    }
    authority = {
        "token_id": "demo-tvc-token-0001",
        "status": "ALLOW",
        "adapter": "local_fs",
        "target": "demo_target",
        "scopes": ["local_fs:write"],
        "issued_at": iso(now),
        "expires_at": iso(now + timedelta(minutes=30)),
        "capsule_hash": capsule_hash,
        "receipt_hash": receipt["payload_hash"]
    }

    receipt_path = EXAMPLES / "verified_receipt.json"
    authority_path = EXAMPLES / "authority_token.json"
    receipt_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    authority_path.write_text(json.dumps(authority, indent=2), encoding="utf-8")

    dry = subprocess.run([sys.executable, "-m", "src.stegentity.cli", "dry-run", str(capsule_path), "--root", str(DEMO_ROOT), "--receipt", str(receipt_path), "--authority", str(authority_path)], cwd=ROOT, text=True, capture_output=True, check=True)
    apply = subprocess.run([sys.executable, "-m", "src.stegentity.cli", "apply", str(capsule_path), "--root", str(DEMO_ROOT), "--receipt", str(receipt_path), "--authority", str(authority_path)], cwd=ROOT, text=True, capture_output=True, check=True)

    print("DRY RUN:")
    print(dry.stdout)
    print("APPLY:")
    print(apply.stdout)
    print("WROTE:", DEMO_ROOT / "hello.txt")

if __name__ == "__main__":
    main()
