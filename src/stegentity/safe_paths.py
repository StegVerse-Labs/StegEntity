from pathlib import Path
from .errors import AdapterError

def resolve_under_root(root: Path, rel_path: str) -> Path:
    if not isinstance(rel_path, str) or not rel_path:
        raise AdapterError("empty_path")
    rel = Path(rel_path)
    if rel.is_absolute():
        raise AdapterError(f"absolute_path_forbidden:{rel_path}")
    if any(part in ("..", "") for part in rel.parts):
        raise AdapterError(f"unsafe_path_component:{rel_path}")
    target = (root / rel).resolve()
    root_resolved = root.resolve()
    try:
        target.relative_to(root_resolved)
    except ValueError:
        raise AdapterError(f"path_escapes_root:{rel_path}")
    return target

def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
