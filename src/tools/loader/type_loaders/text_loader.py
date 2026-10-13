from collections.abc import Iterator

from ..core.interfaces import BaseLoader, Document


class TextLoader(BaseLoader):
    """Text files/ Markdowns: 1 document/file"""

    extensions = [".txt"]

    def _read_text_file(self) -> str:
        raw = self.path.read_bytes()
        for enc in ("utf-8-sig", "utf-16"):
            try:
                return raw.decode(enc)
            except UnicodeDecodeError:
                continue
        return raw.decode("latin-1", errors="replace")

    def load(self) -> Iterator[Document]:
        text = self._read_text_file()
        for i, line in enumerate(text.splitlines(), start=1):
            if line:
                yield Document(
                    text=line.strip(),
                    source=self.path.name,
                    meta={
                        "type": self.path.suffix.lstrip("."),
                        "line": i,
                    },
                )
