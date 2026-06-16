import json
from pathlib import Path


MANIFEST_PATH = Path("activation_manifest.json")

REQUIRED_TOP_LEVEL = {
    "schema",
    "repository",
    "activation",
    "canonical_commands",
    "activation_evidence",
    "activation_requirements",
    "non_claims",
    "gap_status",
    "documents",
}

REQUIRED_COMMANDS = {
    "build_role_context_demo",
    "verify_generated_demo",
    "activation_manifest_check",
    "unit_tests",
    "role_context_demo_check",
    "activation_check",
}

REQUIRED_EVIDENCE_TRUE = {
    "local_runtime",
    "local_filesystem_adapter",
    "capsule_validation",
    "verified_receipt_consumption",
    "authority_token_consumption",
    "dry_run_path",
    "successful_apply_path",
    "refused_apply_path",
    "execution_receipt_emission",
    "refusal_receipt_emission",
    "outcome_report_emission",
    "blocked_outcome_report_emission",
    "role_enforcement_output",
    "completion_invariant_output",
    "ci_activation_check",
}

REQUIRED_SUCCESS_REQUIREMENTS = {
    "validation_succeeds",
    "dry_run_succeeds",
    "apply_succeeds",
    "target_state_written",
    "execution_receipt_emitted",
    "apply_outcome_report_emitted",
    "completion_invariant_required",
    "completion_invariant_satisfied",
    "completion_invariant_hash_matched",
    "completion_invariant_consistent_across_return_receipt_and_report",
}

REQUIRED_REFUSAL_REQUIREMENTS = {
    "apply_refused_before_mutation",
    "target_state_not_written",
    "blocked_apply_receipt_emitted",
    "execution_receipt_not_emitted",
    "blocked_outcome_report_emitted",
    "blocked_outcome_hash_bound_to_refusal_receipt",
}

REQUIRED_NON_CLAIMS_FALSE = {
    "production_deployment_readiness",
    "live_stegid_minting",
    "live_tv_tvc_issuance",
    "multi_adapter_parity",
    "cross_repo_admissibility_completion",
    "org_wide_governance_completion",
}

REQUIRED_DOCUMENTS = {
    "activation_status",
    "activation_doctrine",
    "activation_gap_list",
    "local_activation_runbook",
    "ci_failure_guide",
    "role_transition_policy",
    "verification",
}


class ManifestError(AssertionError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ManifestError(message)


def require_keys(container: dict, required: set[str], label: str) -> None:
    missing = sorted(required - set(container))
    require(not missing, f"{label}_missing_keys:{missing}")


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    require_keys(manifest, REQUIRED_TOP_LEVEL, "manifest")
    require(manifest["schema"]["name"] == "stegverse.stegentity.activation_manifest", "schema_name_mismatch")
    require(manifest["schema"]["version"] == "0.1.0", "schema_version_mismatch")

    repo = manifest["repository"]
    require(repo["organization"] == "StegVerse-Labs", "repository_organization_mismatch")
    require(repo["name"] == "StegEntity", "repository_name_mismatch")
    require(repo["external_dependencies_required"] is False, "external_dependencies_should_be_false")

    activation = manifest["activation"]
    require(activation["status"] == "activation_candidate", "activation_status_mismatch")
    require(activation["posture"] == "local_governed_runtime_module", "activation_posture_mismatch")
    require(isinstance(activation["activation_percent_estimate"], int), "activation_percent_not_int")
    require(activation["production_complete"] is False, "production_complete_should_be_false")
    require(activation["org_wide_complete"] is False, "org_wide_complete_should_be_false")

    commands = manifest["canonical_commands"]
    require_keys(commands, REQUIRED_COMMANDS, "canonical_commands")
    require(commands["activation_manifest_check"] == "python tools/verify_activation_manifest.py", "activation_manifest_check_command_mismatch")
    require(commands["activation_check"] == "python tools/check_repo_activation.py", "activation_check_command_mismatch")

    evidence = manifest["activation_evidence"]
    require_keys(evidence, REQUIRED_EVIDENCE_TRUE, "activation_evidence")
    for key in REQUIRED_EVIDENCE_TRUE:
        require(evidence[key] is True, f"activation_evidence_not_true:{key}")

    requirements = manifest["activation_requirements"]
    require(set(requirements["success_path"]) >= REQUIRED_SUCCESS_REQUIREMENTS, "success_path_requirements_incomplete")
    require(set(requirements["refusal_path"]) >= REQUIRED_REFUSAL_REQUIREMENTS, "refusal_path_requirements_incomplete")

    non_claims = manifest["non_claims"]
    require_keys(non_claims, REQUIRED_NON_CLAIMS_FALSE, "non_claims")
    for key in REQUIRED_NON_CLAIMS_FALSE:
        require(non_claims[key] is False, f"non_claim_should_be_false:{key}")

    gap_status = manifest["gap_status"]
    require(gap_status["G1_full_role_transition_enforcement"] == "partial", "g1_status_mismatch")
    require(gap_status["G2_completion_invariant_enforcement"] == "partial", "g2_status_mismatch")
    require(gap_status["G4_multi_adapter_readiness"] == "open", "g4_status_mismatch")

    documents = manifest["documents"]
    require_keys(documents, REQUIRED_DOCUMENTS, "documents")
    for key, path in documents.items():
        require(Path(path).exists(), f"document_path_missing:{key}:{path}")

    print(json.dumps({"status": "ok", "manifest": str(MANIFEST_PATH)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
