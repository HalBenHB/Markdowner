"""Orchestrator: convert selected file(s) with one or more methods at once.

Reuses the same runner modules (and shared CLI helpers) so the workflow matches
the standalone runners. Focus is PDF -> Markdown, but the other export formats
exposed by docling / pymupdf4llm are available too.
"""

from __future__ import annotations

import cli_common as cli
import run_docling
import run_markitdown
import run_pymupdf4llm

# Generic registry so the conversion loop stays method-agnostic.
METHODS = {
    "markitdown": run_markitdown,
    "docling": run_docling,
    "pymupdf4llm": run_pymupdf4llm,
}


def main() -> None:
    cli.print_header("Markdowner")

    files = cli.select_files(cli.list_input_files("."))
    if not files:
        return

    method_names = cli.select_from_menu(
        "Conversion methods", list(METHODS), multi=True, default="markitdown"
    )

    # Per-method: choose output format, then optionally customise advanced options.
    formats: dict[str, str] = {}
    options: dict[str, dict] = {}
    for name in method_names:
        module = METHODS[name]
        if len(module.OUTPUT_FORMATS) == 1:
            formats[name] = module.OUTPUT_FORMATS[0]
        else:
            formats[name] = cli.select_from_menu(
                f"Output format for {name}", module.OUTPUT_FORMATS, multi=False, default="md"
            )
        if cli.ask_yes_no(f"Customize advanced features for {name}?", default=False):
            options[name] = module.prompt_options()
        else:
            options[name] = {}

    cli.print_header("Converting")
    produced: list[str] = []
    skipped: list[str] = []

    for path in files:
        for name in method_names:
            module = METHODS[name]
            if path.suffix.lower() not in module.SUPPORTED_EXTS:
                msg = f"{path.name} via {name} (unsupported extension)"
                print(f"  Skipped {msg}")
                skipped.append(msg)
                continue
            print(f"  Converting {path.name} via {name} ...")
            try:
                content = module.convert(path, options[name], formats[name])
            except Exception as exc:
                msg = f"{path.name} via {name}: {exc}"
                print(f"    Failed: {exc}")
                skipped.append(msg)
                continue
            out_path = cli.write_output(content, path.stem, name, formats[name])
            print(f"    Wrote {out_path}")
            produced.append(str(out_path))

    cli.print_header("Summary")
    print(f"Produced {len(produced)} file(s):")
    for p in produced:
        print(f"  + {p}")
    if skipped:
        print(f"\nSkipped/failed {len(skipped)}:")
        for s in skipped:
            print(f"  - {s}")


if __name__ == "__main__":
    main()
