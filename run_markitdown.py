"""Standalone runner for Microsoft's markitdown.

markitdown only emits Markdown. Its richer features (OCR, formula extraction,
LLM image captioning) require Azure Document Intelligence or an LLM API key with
credentials, so locally the only meaningful knob is ``enable_plugins``.
"""

from __future__ import annotations

from pathlib import Path

import cli_common as cli

METHOD = "markitdown"

SUPPORTED_EXTS = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".xls", ".html", ".htm", ".csv",
    ".json", ".jsonl", ".xml", ".epub", ".msg", ".ipynb", ".txt", ".md",
    ".markdown", ".rss", ".atom", ".zip", ".wav", ".mp3", ".m4a", ".mp4",
    ".jpg", ".jpeg", ".png",
}

OUTPUT_FORMATS = ["md"]


def prompt_options() -> dict:
    """Collect the (minimal, local) markitdown options from the user."""
    cli.print_header("markitdown advanced features")
    print(
        "Note: OCR, formula extraction and image captioning need Azure / LLM\n"
        "credentials and are not wired up here."
    )
    return {
        "enable_plugins": cli.ask_yes_no("Enable third-party plugins?", default=False),
    }


def convert(path: Path, options: dict, out_format: str = "md") -> str:
    """Convert *path* to Markdown and return the text."""
    from markitdown import MarkItDown

    md = MarkItDown(enable_plugins=options.get("enable_plugins", False))
    result = md.convert(str(path))
    return result.markdown


def main() -> None:
    cli.print_header("markitdown -> Markdown")
    files = cli.select_files(cli.list_input_files("."))
    if not files:
        return
    options = prompt_options()

    for path in files:
        if path.suffix.lower() not in SUPPORTED_EXTS:
            print(f"  Skipping {path.name}: unsupported by markitdown.")
            continue
        print(f"\nConverting {path.name} ...")
        try:
            content = convert(path, options, "md")
        except Exception as exc:  # surface library errors without aborting the batch
            print(f"  Failed: {exc}")
            continue
        out_path = cli.write_output(content, path.stem, METHOD, "md")
        print(f"  Wrote {out_path}")


if __name__ == "__main__":
    main()
