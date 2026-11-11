"""Render the report to standalone HTML and to PDF.

PDF backends, in preference order:
  1. headless Chrome / Edge / Chromium already on the machine (best fidelity,
     no Python dependency). Set BROWSER_BIN to override the lookup.
  2. WeasyPrint, if installed (`pip install weasyprint`, needs pango/cairo).

If neither is available the function still writes the HTML and tells the user
plainly that the PDF was not produced — it never silently emits a broken file.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/snap/bin/chromium",
]

PRINT_CSS = """
@page { size: A4; margin: 16mm 14mm 18mm 14mm; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-size: 10.5pt; }
table { page-break-inside: avoid; break-inside: avoid; }
/* A caption immediately followed by its table must not be orphaned onto the
   previous page. render.py wraps such pairs in .keep-together. */
.keep-together { page-break-inside: avoid; break-inside: avoid; }
h1, h2, h3 { page-break-after: avoid; break-after: avoid; }
h2 { page-break-before: auto; }
thead { display: table-header-group; }
tr { page-break-inside: avoid; break-inside: avoid; }
/* Keep a horizontal rule with the section it introduces instead of stranding it
   at the foot of the previous page. */
hr { page-break-after: avoid; break-after: avoid; }
/* List markers should match body text, not inherit the link colour. */
li::marker { color: #111827; }
"""


def keep_tables_with_captions(html: str) -> str:
    """Wrap a caption paragraph plus its following table in one unbreakable block.

    Markdown emits `*Table N. ...*` as a paragraph directly before the `<table>`.
    Without this, a page break can leave the caption at the foot of one page and
    the table on the next.
    """
    import re as _re

    # Caption is emitted as <p><em>Table N. ...</em></p> and may contain inline tags,
    # so the body is matched non-greedily up to </p> rather than excluding "<".
    pattern = _re.compile(
        r"(<p>\s*<em>\s*Table\b.*?</em>\s*</p>)\s*(<table>.*?</table>)",
        _re.S | _re.I,
    )
    return pattern.sub(lambda m: f'<div class="keep-together">{m.group(1)}{m.group(2)}</div>', html)


def find_browser() -> str | None:
    override = os.environ.get("BROWSER_BIN")
    if override and Path(override).exists():
        return override
    for c in CHROME_CANDIDATES:
        if Path(c).exists() and os.access(c, os.X_OK):
            return c
    for name in ("google-chrome", "chromium", "chromium-browser", "microsoft-edge"):
        found = shutil.which(name)
        if found:
            return found
    return None


def html_to_pdf(html_path: Path, pdf_path: Path) -> tuple[bool, str]:
    """Returns (ok, message)."""
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    browser = find_browser()
    if browser:
        with tempfile.TemporaryDirectory() as td:
            cmd = [
                browser, "--headless", "--disable-gpu", "--no-sandbox",
                "--no-pdf-header-footer",
                f"--user-data-dir={td}",
                f"--print-to-pdf={pdf_path}",
                "--virtual-time-budget=8000",
                html_path.resolve().as_uri(),
            ]
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if pdf_path.exists() and pdf_path.stat().st_size > 1024:
            size = pdf_path.stat().st_size
            return True, f"PDF via {Path(browser).name} ({size/1024:.0f} KB)"
        return False, f"browser present but produced no PDF: {p.stderr[-400:]}"

    try:  # optional fallback
        from weasyprint import HTML  # type: ignore

        HTML(filename=str(html_path)).write_pdf(str(pdf_path))
        return True, "PDF via WeasyPrint"
    except Exception as exc:  # noqa: BLE001
        return False, (
            "No PDF backend available. Install Chrome/Chromium, set BROWSER_BIN, "
            f"or `pip install weasyprint`. ({type(exc).__name__}: {exc})"
        )


def inject_print_css(html: str) -> str:
    if "</head>" in html:
        return html.replace("</head>", f"<style>{PRINT_CSS}</style>\n</head>", 1)
    return f"<style>{PRINT_CSS}</style>\n" + html


def write_html(html: str, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(inject_print_css(keep_tables_with_captions(html)))
    return out