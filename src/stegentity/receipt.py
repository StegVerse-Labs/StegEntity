from dataclasses import dataclass
from typing import Any, Dict, List

from .errors import AuthorityError, ValidationError
from .timeutil import not_expired, parse_time

@dataclass(frozen=True)
class VerifiedReceipt:
    receipt_id: str
    actor_class: str
    scopes: List[str]
    issued_at: str
    expires_at: str
    assurance_level: int
    issuer: str
    kid: str
    payload_hash: str
    sig: str
    raw: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VerifiedReceipt":
        required = ["receipt_id", "actor_class", "scopes", "issued_at", "expires_at", "assurance_level", "issuer", "kid", "payload_hash", "sig"]
        missing = [key for key in required if key not in data]
        if missing:
            raise ValidationError(f"verified_receipt_missing_fields:{missing}")
        if not isinstance(data["scopes"], list) or not all(isinstance(x, str) for x in data["scopes"]):
            raise ValidationError("verified_receipt_scopes_must_be_string_list")
        parse_time(data["issued_at"])
        parse_time(data["expires_at"])
        return cls(
            receipt_id=str(data["receipt_id"]),
            actor_class=str(data["actor_class"]),
            scopes=list(data["scopes"]),
            issued_at=str(data["issued_at"]),
            expires_at=str(data["expires_at"]),
            assurance_level=int(data["assurance_level"]),
            issuer=str(data["issuer"]),
            kid=str(data["kid"]),
            payload_hash=str(data["payload_hash"]),
            sig=str(data["sig"]),
            raw=dict(data),
        )

    def validate_for_capsule(self, capsule_hash: str, required_scopes: List[str], minimum_assurance: int = 1) -> None:
        if not not_expired(self.expires_at):
            raise AuthorityError("verified_receipt_expired")
        if self.assurance_level < minimum_assurance:
            raise AuthorityError("verified_receipt_assurance_too_low")
        missing_scopes = [scope for scope in required_scopes if scope not in self.scopes]
        if missing_scopes:
            raise AuthorityError(f"verified_receipt_missing_required_scopes:{missing_scopes}")
        if self.payload_hash not in (capsule_hash, "*"):
            raise AuthorityError("verified_receipt_payload_hash_mismatch")
