import argparse
import json
from pathlib import Path

from .runtime import StegEntityRuntime, load_authority, load_capsule, load_receipt

def print_json(data):
    print(json.dumps(data, indent=2))

def main(argv=None):
    parser = argparse.ArgumentParser(prog="stegentity")
    sub = parser.add_subparsers(dest="cmd", required=True)

    validate_p = sub.add_parser("validate")
    validate_p.add_argument("capsule")
    validate_p.add_argument("--receipt")
    validate_p.add_argument("--authority")
    validate_p.add_argument("--root", default=".")

    dry_p = sub.add_parser("dry-run")
    dry_p.add_argument("capsule")
    dry_p.add_argument("--receipt", required=True)
    dry_p.add_argument("--authority", required=True)
    dry_p.add_argument("--root", default=".")

    apply_p = sub.add_parser("apply")
    apply_p.add_argument("capsule")
    apply_p.add_argument("--receipt", required=True)
    apply_p.add_argument("--authority", required=True)
    apply_p.add_argument("--root", default=".")

    args = parser.parse_args(argv)

    try:
        capsule = load_capsule(Path(args.capsule))
        if args.cmd == "validate" and (not args.receipt or not args.authority):
            print_json({
                "status": "ok",
                "mode": "structural_validate",
                "capsule_id": capsule.capsule_id,
                "capsule_hash": capsule.hash(),
                "adapter": capsule.adapter,
                "target": capsule.target,
                "operation_count": len(capsule.operations),
                "required_scopes": capsule.required_scopes(),
            })
            return 0
        receipt = load_receipt(Path(args.receipt))
        authority = load_authority(Path(args.authority))
        runtime = StegEntityRuntime(Path(args.root))
        if args.cmd == "validate":
            print_json(runtime.validate(capsule, receipt, authority))
        elif args.cmd == "dry-run":
            print_json(runtime.dry_run(capsule, receipt, authority))
        elif args.cmd == "apply":
            print_json(runtime.apply(capsule, receipt, authority))
        return 0
    except Exception as exc:
        print_json({"status": "failed", "error": str(exc), "error_type": exc.__class__.__name__})
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
