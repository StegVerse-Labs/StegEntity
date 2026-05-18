from pathlib import Path
from typing import Any, Dict, List
import base64
import shutil

from ..errors import AdapterError, VerificationError
from ..hashutil import sha256_bytes, sha256_file
from ..safe_paths import ensure_parent, resolve_under_root

class LocalFSAdapter:
    name = "local_fs"

    def __init__(self, root: Path, state_dir: Path | None = None):
        self.root = root.resolve()
        self.state_dir = (state_dir or (self.root / "stegentity_state")).resolve()
        self.backup_dir = self.state_dir / "backups"

    def inspect(self, operations) -> Dict[str, Any]:
        items: List[Dict[str, Any]] = []
        for op in operations:
            dest = resolve_under_root(self.root, op.destination)
            items.append({
                "op_id": op.op_id,
                "destination": op.destination,
                "resolved_destination": str(dest),
                "exists": dest.exists(),
                "current_sha256": sha256_file(dest) if dest.exists() and dest.is_file() else None,
                "operation": op.operation,
            })
        return {"adapter": self.name, "root": str(self.root), "operations": items}

    def dry_run(self, operations) -> Dict[str, Any]:
        inspected = self.inspect(operations)
        for item, op in zip(inspected["operations"], operations):
            exists = item["exists"]
            if op.operation == "create" and exists:
                item["would_fail"] = "destination_exists"
            elif op.operation == "replace" and not exists:
                item["would_fail"] = "destination_missing"
            else:
                item["would_fail"] = None
            item["would_write"] = item["would_fail"] is None
        inspected["dry_run"] = True
        return inspected

    def apply(self, operations, capsule_id: str) -> Dict[str, Any]:
        results: List[Dict[str, Any]] = []
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        for op in operations:
            dest = resolve_under_root(self.root, op.destination)
            if op.content_b64 is None:
                raise AdapterError(f"operation_missing_content_b64:{op.op_id}")
            content = base64.b64decode(op.content_b64.encode("utf-8"))
            content_hash = sha256_bytes(content)
            if op.expected_sha256 and op.expected_sha256 != content_hash:
                raise VerificationError(f"operation_expected_hash_mismatch:{op.op_id}")
            exists = dest.exists()
            if op.operation == "create" and exists:
                raise AdapterError(f"destination_exists:{op.destination}")
            if op.operation == "replace" and not exists:
                raise AdapterError(f"destination_missing:{op.destination}")
            if exists and not op.allow_replace:
                raise AdapterError(f"replace_not_allowed:{op.destination}")
            if not exists and not op.allow_create:
                raise AdapterError(f"create_not_allowed:{op.destination}")
            backup_path = None
            if exists and dest.is_file():
                backup_path = self.backup_dir / capsule_id / op.op_id / dest.name
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dest, backup_path)
            ensure_parent(dest)
            if op.operation == "append":
                with dest.open("ab") as f:
                    f.write(content)
                final_hash = sha256_file(dest)
                verified = True if not op.expected_sha256 else final_hash == op.expected_sha256
            else:
                dest.write_bytes(content)
                final_hash = sha256_file(dest)
                verified = final_hash == content_hash
            if not verified:
                raise VerificationError(f"post_write_verification_failed:{op.op_id}")
            results.append({
                "op_id": op.op_id,
                "operation": op.operation,
                "destination": op.destination,
                "resolved_destination": str(dest),
                "created": not exists,
                "replaced": exists and op.operation != "append",
                "appended": op.operation == "append",
                "backup_path": str(backup_path) if backup_path else None,
                "expected_sha256": op.expected_sha256,
                "written_sha256": final_hash,
                "verified": verified,
            })
        return {"adapter": self.name, "root": str(self.root), "operations": results}
