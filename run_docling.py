"""Standalone runner for docling.

docling has the richest configuration: OCR engine control, TableFormer table
recognition (FAST vs ACCURATE), formula/code enrichment and several export
formats. OCR defaults OFF since the target PDFs are digital text.
"""

from __future__ import annotations

import json
from pathlib import Path

import cli_common as cli

METHOD = "docling"

SUPPORTED_EXTS = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".html", ".htm", ".md", ".csv",
    ".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".webp", ".adoc", ".xml",
}

OUTPUT_FORMATS = ["md", "html", "json", "text", "doctags"]


def prompt_options() -> dict:
    """Collect docling pipeline options from the user."""
    cli.print_header("docling advanced features")
    options: dict = {}

    options["do_ocr"] = cli.ask_yes_no("Enable OCR (slow; for scanned pages)?", default=False)
    if options["do_ocr"]:
        options["force_full_page_ocr"] = cli.ask_yes_no(
            "Force full-page OCR (re-OCR everything)?", default=False
        )
        options["ocr_lang"] = [
            s.strip()
            for s in cli.ask_str("OCR language code(s), comma-separated", "eng").split(",")
            if s.strip()
        ]

    options["do_table_structure"] = cli.ask_yes_no(
        "Recognize table structure?", default=True
    )
    if options["do_table_structure"]:
        options["table_mode"] = cli.ask_choice(
            "TableFormer mode", ["accurate", "fast"], "accurate"
        )
        options["do_cell_matching"] = cli.ask_yes_no(
            "Match table cells to source text?", default=True
        )

    options["do_formula_enrichment"] = cli.ask_yes_no(
        "Enable formula enrichment?", default=False
    )
    options["do_code_enrichment"] = cli.ask_yes_no(
        "Enable code enrichment?", default=False
    )
    options["generate_picture_images"] = cli.ask_yes_no(
        "Extract embedded picture images?", default=False
    )
    return options


def _build_pipeline_options(options: dict):
    from docling.datamodel.pipeline_options import (
        EasyOcrOptions,
        PdfPipelineOptions,
        TableFormerMode,
    )

    opts = PdfPipelineOptions()
    opts.do_ocr = options.get("do_ocr", False)
    if opts.do_ocr:
        opts.ocr_options = EasyOcrOptions(
            lang=options.get("ocr_lang", ["eng"]),
            force_full_page_ocr=options.get("force_full_page_ocr", False),
        )

    opts.do_table_structure = options.get("do_table_structure", True)
    if opts.do_table_structure:
        mode = options.get("table_mode", "accurate")
        opts.table_structure_options.mode = (
            TableFormerMode.FAST if mode == "fast" else TableFormerMode.ACCURATE
        )
        opts.table_structure_options.do_cell_matching = options.get(
            "do_cell_matching", True
        )

    opts.do_formula_enrichment = options.get("do_formula_enrichment", False)
    opts.do_code_enrichment = options.get("do_code_enrichment", False)
    opts.generate_picture_images = options.get("generate_picture_images", False)
    return opts


def convert(path: Path, options: dict, out_format: str = "md"):
    """Convert *path* and return content in the requested export format."""
    from docling.datamodel.base_models import InputFormat
    from docling.document_converter import DocumentConverter, PdfFormatOption

    pipeline_options = _build_pipeline_options(options)
    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    doc = converter.convert(str(path)).document

    if out_format == "md":
        return doc.export_to_markdown()
    if out_format == "html":
        return doc.export_to_html()
    if out_format == "json":
        return json.dumps(doc.export_to_dict(), indent=2, ensure_ascii=False)
    if out_format == "text":
        return doc.export_to_text()
    if out_format == "doctags":
        return doc.export_to_doctags()
    raise ValueError(f"Unsupported output format for docling: {out_format}")


def main() -> None:
    cli.print_header("docling -> Markdown")
    files = cli.select_files(cli.list_input_files("."))
    if not files:
        return
    out_format = cli.select_from_menu(
        "Output format", OUTPUT_FORMATS, multi=False, default="md"
    )
    options = prompt_options()

    for path in files:
        if path.suffix.lower() not in SUPPORTED_EXTS:
            print(f"  Skipping {path.name}: unsupported by docling.")
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
