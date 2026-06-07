"""Standalone runner for pymupdf4llm (PDF only).

pymupdf4llm ships two code paths: a modern *layout* path (active by default when
``pymupdf.layout`` is importable) and a *legacy* RAG path. They expose different
knobs, so we branch on ``pymupdf4llm._use_layout`` and only prompt for options
that actually take effect. OCR defaults OFF.
"""

from __future__ import annotations

from pathlib import Path

import cli_common as cli

METHOD = "pymupdf4llm"

SUPPORTED_EXTS = {".pdf"}

OUTPUT_FORMATS = ["md", "json", "text"]


def _use_layout() -> bool:
    import pymupdf4llm

    return bool(getattr(pymupdf4llm, "_use_layout", False))


def prompt_options() -> dict:
    """Collect pymupdf4llm options, branching on the active code path."""
    cli.print_header("pymupdf4llm advanced features")
    options: dict = {}

    if _use_layout():
        options["header"] = cli.ask_yes_no("Keep headers?", default=True)
        options["footer"] = cli.ask_yes_no("Keep footers?", default=True)
        options["ignore_code"] = cli.ask_yes_no(
            "Ignore monospaced/code blocks?", default=False
        )
        options["page_chunks"] = cli.ask_yes_no(
            "Return per-page chunks (output as JSON)?", default=False
        )
        options["use_ocr"] = cli.ask_yes_no(
            "Enable OCR (slow; needs an OCR engine)?", default=False
        )
        if options["use_ocr"]:
            options["force_ocr"] = cli.ask_yes_no("Force OCR on every page?", default=False)
            options["ocr_language"] = cli.ask_str("OCR language code", "eng")
        options["write_images"] = cli.ask_yes_no(
            "Write embedded images to output/images?", default=False
        )
        if options["write_images"]:
            options["image_format"] = cli.ask_choice(
                "Image format", ["png", "jpg", "webp"], "png"
            )
    else:
        options["table_strategy"] = cli.ask_choice(
            "Table detection strategy",
            ["lines_strict", "lines", "cells"],
            "lines_strict",
        )
        options["margins"] = cli.ask_int("Margin to crop (points)", 0)
        options["ignore_images"] = cli.ask_yes_no("Ignore images?", default=False)
        options["ignore_graphics"] = cli.ask_yes_no("Ignore vector graphics?", default=False)
        options["ignore_code"] = cli.ask_yes_no(
            "Ignore monospaced/code blocks?", default=False
        )
        options["page_chunks"] = cli.ask_yes_no(
            "Return per-page chunks (output as JSON)?", default=False
        )
        options["write_images"] = cli.ask_yes_no(
            "Write embedded images to output/images?", default=False
        )
        if options["write_images"]:
            options["image_format"] = cli.ask_choice(
                "Image format", ["png", "jpg", "webp"], "png"
            )
    return options


def convert(path: Path, options: dict, out_format: str = "md"):
    """Convert *path* and return content in the requested format."""
    import pymupdf4llm

    kwargs = dict(options)
    if _use_layout():
        # The layout path defaults use_ocr=True; keep OCR off unless asked for.
        kwargs.setdefault("use_ocr", False)
    if kwargs.get("write_images"):
        image_dir = cli.ensure_output_dir() / "images"
        image_dir.mkdir(exist_ok=True)
        kwargs["image_path"] = str(image_dir)

    if out_format == "md":
        return pymupdf4llm.to_markdown(str(path), **kwargs)
    if out_format == "json":
        return pymupdf4llm.to_json(str(path), **kwargs)
    if out_format == "text":
        return pymupdf4llm.to_text(str(path), **kwargs)
    raise ValueError(f"Unsupported output format for pymupdf4llm: {out_format}")


def main() -> None:
    cli.print_header("pymupdf4llm -> Markdown")
    files = cli.select_files(cli.list_input_files("."))
    if not files:
        return
    out_format = cli.select_from_menu(
        "Output format", OUTPUT_FORMATS, multi=False, default="md"
    )
    options = prompt_options()

    for path in files:
        if path.suffix.lower() not in SUPPORTED_EXTS:
            print(f"  Skipping {path.name}: pymupdf4llm only supports .pdf.")
            continue
        print(f"\nConverting {path.name} ...")
        try:
            content = convert(path, options, out_format)
        except Exception as exc:
            print(f"  Failed: {exc}")
            continue
        out_path = cli.write_output(content, path.stem, METHOD, out_format)
        print(f"  Wrote {out_path}")


if __name__ == "__main__":
    main()
