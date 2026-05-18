import base64
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timedelta, timezone

from src.stegentity.authority import AuthorityToken
from src.stegentity.capsule import MaintenanceCapsule
from src.stegentity.receipt import VerifiedReceipt
from src.stegentity.runtime import StegEntityRuntime

def iso(dt):
    return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")

class TestRuntimeLocalFS(unittest.TestCase):
    def make_capsule(self):
        content = b"test content\n"
        return {
            "schema": {"name": "stegverse.maintenance_capsule", "version": "0.1.0"},
            "capsule_id": "test-capsule-0001",
            "created_at": iso(datetime.now(timezone.utc)),
            "target": {"adapter": "local_fs", "target_id": "test-target"},
            "transition": {"transition_id": "T-120", "transition_name": "File Creation"},
            "admissibility": {"decision": "ALLOW"},
            "dependencies": ["local fs"],
            "consequences": ["writes file"],
            "rollback_plan": ["backup if exists"],
            "verification": {"required": True, "method": "sha256_after_write"},
            "operations": [{
                "op_id": "op1",
                "operation": "create_or_replace",
                "destination": "hello.txt",
                "content_b64": base64.b64encode(content).decode("utf-8"),
                "expected_sha256": None,
                "required_scopes": ["local_fs:write"],
                "allow_create": True,
                "allow_replace": True
            }]
        }

    def make_receipt_and_token(self, capsule_hash):
        now = datetime.now(timezone.utc)
        receipt = {
            "receipt_id": "test-receipt",
            "actor_class": "ai",
            "scopes": ["local_fs:write"],
            "issued_at": iso(now),
            "expires_at": iso(now + timedelta(minutes=10)),
            "assurance_level": 2,
            "issuer": "stegid",
            "kid": "test",
            "payload_hash": capsule_hash,
            "sig": "test"
        }
        token = {
            "token_id": "test-token",
            "status": "ALLOW",
            "adapter": "local_fs",
            "target": "test-target",
            "scopes": ["local_fs:write"],
            "issued_at": iso(now),
            "expires_at": iso(now + timedelta(minutes=10)),
            "capsule_hash": capsule_hash,
            "receipt_hash": capsule_hash
        }
        return receipt, token

    def test_apply_writes_file_and_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            capsule = MaintenanceCapsule.from_dict(self.make_capsule())
            capsule_hash = capsule.hash()
            receipt_raw, token_raw = self.make_receipt_and_token(capsule_hash)
            receipt = VerifiedReceipt.from_dict(receipt_raw)
            token = AuthorityToken.from_dict(token_raw)
            runtime = StegEntityRuntime(root)
            dry = runtime.dry_run(capsule, receipt, token)
            self.assertEqual(dry["status"], "ok")
            result = runtime.apply(capsule, receipt, token)
            self.assertEqual(result["status"], "ok")
            self.assertTrue((root / "hello.txt").exists())
            self.assertTrue((root / "stegentity_receipts" / "test-capsule-0001.execution_receipt.json").exists())

if __name__ == "__main__":
    unittest.main()
