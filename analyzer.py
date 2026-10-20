"""Static analysis helpers for finding unused imports in Python source."""

import ast
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple


SKIP_DIRS = {".git", ".hg", ".svn", "__pycache__", ".venv", "venv", "env",
             "node_modules", ".tox", ".mypy_cache", ".pytest_cache", "build",
             "dist", ".eggs"}


def _is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIRS or part.startswith(".") for part in path.parts)


def collect_imports(tree: ast.AST) -> List[Tuple[str, int, str]]:
    """Return list of (bound_name, lineno, origin) for every import."""
    imported: List[Tuple[str, int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                bound = alias.asname if alias.asname else alias.name.split(".")[0]
                imported.append((bound, node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                if alias.name == "*":
                    continue
                bound = alias.asname if alias.asname else alias.name
                imported.append((bound, node.lineno, f"{module}.{alias.name}".strip(".")))
    return imported


def collect_used_names(tree: ast.AST) -> set:
    """Return the set of names referenced anywhere in the module."""
    used: set = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)
    # Names protected by __all__ count as used.
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    if isinstance(node.value, (ast.List, ast.Tuple, ast.Set)):
                        for elt in node.value.elts:
                            if isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                                used.add(elt.value)
    return used


def analyze_source(source: str, filename: str = "<string>") -> Tuple[List[Dict[str, Any]], List[str]]:
    """Analyze source text. Returns (unused_list, errors)."""
    try:
        tree = ast.parse(source, filename=filename)
    except SyntaxError as exc:
        return [], [f"SyntaxError: {exc}"]
    imported = collect_imports(tree)
    used = collect_used_names(tree)
    unused: List[Dict[str, Any]] = []
    seen = set()
    for bound, lineno, origin in imported:
        if bound in used:
            continue
        key = (bound, lineno)
        if key in seen:
            continue
        seen.add(key)
        unused.append({"name": bound, "line": lineno, "module": origin})
    return unused, []


def analyze_file(path) -> Tuple[Optional[List[Dict[str, Any]]], List[str]]:
    """Analyze a file path. Returns (unused_list or None on error, errors)."""
    p = Path(path)
    try:
        source = p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return None, [f"read error: {exc}"]
    unused, errors = analyze_source(source, filename=str(p))
    return unused, errors


def iter_python_files(paths) -> List[Path]:
    """Expand paths into a sorted list of .py files."""
    result: List[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_file():
            if path.suffix == ".py":
                result.append(path)
        elif path.is_dir():
            for f in path.rglob("*.py"):
                if _is_skipped(f):
                    continue
                result.append(f)
    # de-duplicate while preserving order
    seen = set()
    out = []
    for f in result:
        if f in seen:
            continue
        seen.add(f)
        out.append(f)
    return sorted(out)
