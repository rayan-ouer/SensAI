from pathlib import Path

from .core.errors import LoaderError, UnsupportedFormat
from .core.interfaces import BaseLoader, Document
from .type_loaders import markdown_loader, text_loader, pdf_loader


class FileReader:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        if not self.path.is_file():
            raise LoaderError("File not found.", self.path)

    def __str__(self) -> str:
        return self.read()

    def get_ext(self) -> str:
        return self.path.suffix.lower()

    def get_parser(self) -> BaseLoader:
        parser = BaseLoader.for_path(self.path)
        if parser is None:
            raise UnsupportedFormat(self.path)
        return parser

    def documents(self) -> list[Document]:
        result = []
        try:
            result = list(self.get_parser().load())
        except LoaderError or UnsupportedFormat as e:
            print(e)
            return result

        return  result

    def read(self, sep: str = "\n\n") -> str:
        return sep.join(doc.text for doc in self.documents())


def read_file(path: str | Path) -> str:
    return FileReader(path).read()
