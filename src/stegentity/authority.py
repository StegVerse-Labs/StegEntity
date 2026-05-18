from dataclasses import dataclass
from typing import Any, Dict, List

from .errors import AuthorityError, ValidationError
from .timeutil import not_expired, parse_time

@dataclass(frozen=True)
class AuthorityToken:
    token_id: str
    status: str
    adapter: str
    target: str
    scopes: List[str]
    issued_at: str
    expires_at: str
    capsule_hash: str
    receipt_hash: str
    raw: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuthorityToken":
        required = ["token_id", "status", "adapter", "target", "scopes", "issued_at", "expires_at", "capsule_hash", "receipt_hash"]
        missing = [key for key in required if key not in data]
        if missing:
            raise ValidationError(f"authority_token_missing_fields:{missing}")
        if not isinstance(data["scopes"], list) or not all(isinstance(x, str) for x in data["scopes"]):
            raise ValidationError("authority_token_scopes_must_be_string_list")
        parse_time(data["issued_at"])
        parse_time(data["expires_at"])
        return cls(
            token_id=str(data["token_id"]),
            status=str(data["status"]),
            adapter=str(data["adapter"]),
            target=str(data["target"]),
            scopes=list(data["scopes"]),
            issued_at=str(data["issued_at"]),
            expires_at=str(data["expires_at"]),
            capsule_hash=str(data["capsule_hash"]),
            receipt_hash=str(data["receipt_hash"]),
            raw=dict(data),
        )

    def validate_for_capsule(self, capsule_hash: str, adapter: str, target: str, required_scopes: List[str]) -> None:
        if self.status != "ALLOW":
            raise AuthorityError(f"authority_token_not_allow:{self.status}")
        if not not_expired(self.expires_at):
            raise AuthorityError("authority_token_expired")
        if self.adapter != adapter:
            raise AuthorityError(f"authority_token_adapter_mismatch:{self.adapter}!={adapter}")
        if self.target not in (target, "*"):
            raise AuthorityError(f"authority_token_target_mismatch:{self.target}!={target}")
        if self.capsule_hash not in (capsule_hash, "*"):
            raise AuthorityError("authority_token_capsule_hash_mismatch")
        missing_scopes = [scope for scope in required_scopes if scope not in self.scopes]
        if missing_scopes:
            raise AuthorityError(f"authority_token_missing_required_scopes:{missing_scopes}")
