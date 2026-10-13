import re

from ..core.interfaces import BaseLoader, Document

HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


def _split_sections(text: str) -> list[tuple[list[str], str]]:
    """Cut markdown sections into a list of tuples (section name, content)."""
    sections = []
    titles = []
    buf = []
    in_code = False

    def close():
        body = "\n".join(buf).strip()
        if body:
            sections.append((list(titles), body))
        buf.clear()

    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
        m = None if in_code else HEADING.match(line)
        if m:
            close()
            level = len(m.group(1))
            titles[:] = titles[: level - 1] + [m.group(2).strip()]
        buf.append(line)
    close()
    return sections


class MarkdownLoader(BaseLoader):
    """Markdown : cut on titles."""

    extensions = (".md", ".markdown")

    def _read_text_file(self) -> str:
        raw = self.path.read_bytes()
        for enc in ("utf-8-sig", "utf-16"):
            try:
                return raw.decode(enc)
            except UnicodeDecodeError:
                continue
        return raw.decode("latin-1", errors="replace")

    def load(self):
        text = self._read_text_file()
        for i, (titles, body) in enumerate(_split_sections(text), start=1):
            yield Document(
                text=body,
                source=self.path.name,
                position=i,
                meta={"type": "md", "section": " > ".join(titles)},
            )
