#!/usr/bin/env python3
"""Render runner-side GitHub source downloads into a local agent digest."""

from html import unescape
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

MAX_ITEMS = 15
TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")


def text(value: str) -> str:
    return SPACE_RE.sub(" ", unescape(TAG_RE.sub(" ", value or ""))).strip()


def child(item, names):
    for name in names:
        for node in item:
            if node.tag.rsplit("}", 1)[-1] == name:
                value = text("".join(node.itertext()))
                if value:
                    return value
    return ""


def feed(path: Path, title: str, url: str) -> list[str]:
    lines = [f"## {title}", "", f"Source: {url}", ""]
    if not path.exists():
        return lines + ["Snapshot unavailable.", ""]
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as error:
        return lines + [f"Snapshot unreadable: {error}", ""]

    items = [node for node in root.iter() if node.tag.rsplit("}", 1)[-1] in {"item", "entry"}]
    if not items:
        return lines + ["Snapshot contained no entries.", ""]
    for item in items[:MAX_ITEMS]:
        title_text = child(item, ("title",)) or "(untitled)"
        link = child(item, ("link", "id"))
        date = child(item, ("pubDate", "published", "updated"))
        summary = child(item, ("description", "summary", "content", "encoded"))
        lines.append(f"### {title_text}")
        if date:
            lines.append(f"- Published: {date}")
        if link:
            lines.append(f"- Link: {link}")
        if summary:
            lines.extend(["", summary[:400].rstrip() + ("..." if len(summary) > 400 else "")])
        lines.append("")
    return lines


def page(path: Path, title: str, url: str) -> list[str]:
    lines = [f"## {title}", "", f"Source: {url}", ""]
    if not path.exists():
        return lines + ["Snapshot unavailable.", ""]
    try:
        value = path.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        return lines + [f"Snapshot unreadable: {error}", ""]
    value = text(re.sub(r"<script\b.*?</script>|<style\b.*?</style>", " ", value, flags=re.I | re.S))
    return lines + [value[:4000], ""]


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} SOURCES_DIR", file=sys.stderr)
        return 2
    root = Path(sys.argv[1])
    output = root / "github-sources.md"
    sections = ["# GitHub source snapshot", "", "Downloaded before the agent session started.", ""]
    sections += feed(root / "github-blog.xml", "GitHub Blog", "https://github.blog/latest/")
    sections += feed(root / "github-changelog.xml", "GitHub Changelog", "https://github.blog/changelog/")
    sections += page(root / "awesome-copilot-workflows.html", "Awesome Copilot workflows", "https://awesome-copilot.github.com/workflows/")
    output.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
