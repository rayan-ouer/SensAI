import re
import sys
import unicodedata
from typing import Iterator

from pypdf import PdfReader

from ..core.errors import FileReaderError
from ..core.interfaces import BaseLoader, Document


class PdfLoader(BaseLoader):
    """PDF files: one Document per page."""

    extensions = [".pdf"]

    def load(self) -> Iterator[Document]:
        try:
            reader = PdfReader(self.path)
        except Exception as exc:
            raise FileReaderError(self.path.name) from exc
        total_pages = len(reader.pages)
        self._print_progress(0, total_pages)
        try:
            for i, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                text = self._clean(text, page_number=i)
                self._print_progress(i, total_pages)
                if not text:
                    continue

                yield Document(
                    text=text,
                    source=self.path.name,
                    position=i,
                    kind="long_text",
                    meta={
                        "type": "pdf",
                        "page": i,
                    },
                )
        finally:
            print(file=sys.stderr)

    def _print_progress(self, completed_pages: int, total_pages: int) -> None:
        percentage = completed_pages / total_pages * 100 if total_pages else 0
        bar_width = 50
        filled_width = int(bar_width * percentage / 100)
        bar = "#" * filled_width + "-" * (bar_width - filled_width)
        print(
            f"\rChargement de {self.path.name} : [{bar}] {percentage:3.0f}% "
            f"({completed_pages}/{total_pages} pages)",
            end="",
            flush=True,
            file=sys.stderr,
        )

    @staticmethod
    def _clean(text: str, page_number: int) -> str:
        text = unicodedata.normalize("NFKC", text)
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = "".join(
            char for char in text if char == "\n" or char == "\t" or char.isprintable()
        )
        lines = []

        for line in text.split("\n"):
            line = line.strip()
            if not line:
                lines.append("")
                continue
            if line == str(page_number):
                continue
            line = re.sub(r"[ \t]+", " ", line)
            lines.append(line)
        text = "\n".join(lines)
        text = re.sub(r" +([,.;:!?])", r"\1", text)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()
