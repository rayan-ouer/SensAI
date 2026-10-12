from pathlib import Path

from .interfaces import BaseLoader

class LoaderError(Exception):
    def __init__(self, message: str, path: Path):
        self.path = path
        self.message = message

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"

class UnsupportedFormat(Exception):
    def __init__(self, path: Path):
        self.path = path

    def __str__(self) -> str:
        return (f"{self.path.suffix.lower()}: Unsupported format.\n"
                f"(supported : {', '.join(BaseLoader.available_formats())})")

class FileReaderError(Exception):
    def __init__(self, path: Path):
        self.path = path
    def __str__(self) -> str:
        return f"{self.path.name}: Invalid file.\n"