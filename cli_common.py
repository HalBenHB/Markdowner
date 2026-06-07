"""Shared interactive CLI helpers used by every runner and the orchestrator.

Keeping all the prompting / file-listing / output-writing logic here means the
standalone runners and ``main.py`` present an identical workflow.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

# Files / directories that should never appear as selectable inputs.
EXCLUDED_EXTS = {".py"}
EXCLUDED_NAMES = {"output", "tests", "__pycache__", "venv", ".venv", ".git", ".idea"}
OUTPUT_DIR = Path("output")


def print_header(text: str) -> None:
    """Print a consistent section banner."""
    line = "=" * len(text)
    print(f"\n{line}\n{text}\n{line}")


def list_input_files(directory: Path | str = ".") -> list[Path]:
    """Return top-level files in *directory* that make sense as conversion inputs.

    Excludes directories, ``*.py`` scripts, dotfiles and the bookkeeping
    folders listed in ``EXCLUDED_NAMES``.
    """
    directory = Path(directory)
    files: list[Path] = []
    for entry in directory.iterdir():
        if entry.is_dir():
            continue
        if entry.name.startswith("."):
            continue
        if entry.suffix.lower() in EXCLUDED_EXTS:
            continue
        if entry.name in EXCLUDED_NAMES:
            continue
        files.append(entry)
    return sorted(files, key=lambda p: p.name.lower())


def _parse_selection(raw: str, count: int) -> list[int]:
    """Parse a multi-select string like ``"1,3 5"`` into 0-based indices."""
    tokens = re.split(r"[,\s]+", raw.strip())
    indices: list[int] = []
    for token in tokens:
        if not token:
            continue
        if not token.isdigit():
            raise ValueError(f"'{token}' is not a number")
        num = int(token)
        if not (1 <= num <= count):
            raise ValueError(f"{num} is out of range (1-{count})")
        if num - 1 not in indices:
            indices.append(num - 1)
    if not indices:
        raise ValueError("no selection made")
    return indices


def select_files(files: list[Path]) -> list[Path]:
    """Prompt the user to pick one or more files by number (multi-select)."""
    if not files:
        print("No convertible files found in the working directory.")
        return []
    print_header("Files in working directory")
    for i, path in enumerate(files, start=1):
        print(f"  {i}. {path.name}")
    while True:
        raw = input("\nSelect file(s) by number (e.g. 1,3 5): ")
        try:
            indices = _parse_selection(raw, len(files))
        except ValueError as exc:
            print(f"  Invalid selection: {exc}. Try again.")
            continue
        return [files[i] for i in indices]


def select_from_menu(
    title: str,
    options: list[str],
    multi: bool = False,
    default: str | None = None,
) -> list[str] | str:
    """Numbered single/multi-select menu.

    Returns a list when ``multi`` is True, otherwise a single string.
    """
    print_header(title)
    for i, opt in enumerate(options, start=1):
        marker = "  (default)" if opt == default else ""
        print(f"  {i}. {opt}{marker}")

    if multi:
        prompt = "\nSelect option(s) by number"
        if default is not None:
            prompt += " (Enter for default)"
        while True:
            raw = input(f"{prompt}: ")
            if not raw.strip() and default is not None:
                return [default]
            try:
                indices = _parse_selection(raw, len(options))
            except ValueError as exc:
                print(f"  Invalid selection: {exc}. Try again.")
                continue
            return [options[i] for i in indices]

    # single-select
    prompt = "\nSelect one option by number"
    if default is not None:
        prompt += " (Enter for default)"
    while True:
        raw = input(f"{prompt}: ")
        if not raw.strip() and default is not None:
            return default
        try:
            indices = _parse_selection(raw, len(options))
        except ValueError as exc:
            print(f"  Invalid selection: {exc}. Try again.")
            continue
        if len(indices) != 1:
            print("  Please select exactly one option. Try again.")
            continue
        return options[indices[0]]


def ask_yes_no(prompt: str, default: bool = False) -> bool:
    """Ask a yes/no question; Enter accepts the default."""
    suffix = " [Y/n]: " if default else " [y/N]: "
    while True:
        raw = input(prompt + suffix).strip().lower()
        if not raw:
            return default
        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False
        print("  Please answer 'y' or 'n'.")


def ask_int(prompt: str, default: int) -> int:
    """Ask for an integer; Enter accepts the default."""
    while True:
        raw = input(f"{prompt} [{default}]: ").strip()
        if not raw:
            return default
        try:
            return int(raw)
        except ValueError:
            print("  Please enter a whole number.")


def ask_str(prompt: str, default: str = "") -> str:
    """Ask for a string; Enter accepts the default."""
    raw = input(f"{prompt} [{default}]: ").strip()
    return raw or default


def ask_choice(prompt: str, choices: list[str], default: str) -> str:
    """Ask the user to pick one value from *choices* (inline, not a menu)."""
    options = "/".join(choices)
    while True:
        raw = input(f"{prompt} ({options}) [{default}]: ").strip()
        if not raw:
            return default
        if raw in choices:
            return raw
        print(f"  Please choose one of: {options}.")


def ensure_output_dir() -> Path:
    """Create and return the ``output/`` directory."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    return OUTPUT_DIR


# Map logical output formats to file extensions.
_EXT_BY_FORMAT = {
    "md": "md",
    "html": "html",
    "json": "json",
    "text": "txt",
    "doctags": "doctags.txt",
}


def write_output(content, base_name: str, method: str, out_format: str) -> Path:
    """Write converted *content* to ``output/{base}_{method}.{ext}``.

    Handles ``str``, ``bytes`` and ``list``/``dict`` (json-serialised) content.
    """
    ensure_output_dir()
    ext = _EXT_BY_FORMAT.get(out_format, out_format)
    out_path = OUTPUT_DIR / f"{base_name}_{method}.{ext}"

    if isinstance(content, (list, dict)):
        out_path.write_text(json.dumps(content, indent=2, ensure_ascii=False), encoding="utf-8")
    elif isinstance(content, bytes):
        out_path.write_bytes(content)
    else:
        out_path.write_text(str(content), encoding="utf-8")
    return out_path
