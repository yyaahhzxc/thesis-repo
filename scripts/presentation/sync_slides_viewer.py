"""Syncs docs/PRESENTATION_SLIDES_MOCK_DEFENSE.md into docs/slides_viewer.html's fallback block
so that slides_viewer.html works both via HTTP fetch() and direct file:// double-click."""
from pathlib import Path
import re

ROOT = next((p for p in Path(__file__).resolve().parents if (p / ".git").exists() or (p / "README.md").exists()), Path(__file__).resolve().parents[2])
MD_PATH = ROOT / "docs" / "presentation" / "PRESENTATION_SLIDES_MOCK_DEFENSE.md" if (ROOT / "docs" / "presentation" / "PRESENTATION_SLIDES_MOCK_DEFENSE.md").exists() else ROOT / "docs" / "PRESENTATION_SLIDES_MOCK_DEFENSE.md"
HTML_PATH = ROOT / "docs" / "presentation" / "slides_viewer.html" if (ROOT / "docs" / "presentation" / "slides_viewer.html").exists() else ROOT / "docs" / "slides_viewer.html"


def sync() -> None:
    md_text = MD_PATH.read_text(encoding="utf-8")
    html_text = HTML_PATH.read_text(encoding="utf-8")
    pattern = re.compile(
        r'(<script id="fallback-md" type="text/markdown">\n)(.*?)(\n  </script>)',
        re.DOTALL,
    )
    updated_html, count = pattern.subn(
        lambda m: f"{m.group(1)}{md_text.rstrip()}{m.group(3)}",
        html_text,
        count=1,
    )
    if count == 0:
        raise RuntimeError("Could not find <script id='fallback-md'> in slides_viewer.html")
    HTML_PATH.write_text(updated_html, encoding="utf-8")
    print(f"Synced {MD_PATH.name} -> {HTML_PATH.name}")


if __name__ == "__main__":
    sync()

