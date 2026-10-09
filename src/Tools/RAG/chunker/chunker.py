from chunker_params import *
from src.Tools.loader.core.interfaces import Document
from interfaces import Chunk

class Chunker:

    def __init__(self, documents: list[Document], max_chunk_chars: int = MAX_CHUNK_CHARS, overlap: int = OVERLAP):
        self.documents = documents
        self.max_chunk_chars = max_chunk_chars
        self.overlap = overlap

    def _split_paragraphs(self, text: str) -> list[str]:
        return [p.strip() for p in PARAGRAPH.split(text) if p.strip()]


    def _split_sentences(self, text: str) -> list[str]:
        return [s.strip() for s in SENTENCE.split(text) if s and s.strip()]

    def _overlap_tail(self, previous: str, overlap: int) -> str:
        if overlap <= 0 or len(previous) <= overlap:
            return ""
        tail = previous[-overlap:]
        cut = tail.find(" ")
        return tail[cut + 1:] if cut != -1 else tail

    def _group(self, units: list[str], sep: str) -> list[str]:
        out, buf = [], ""
        for u in units:
            if buf and len(buf) + len(sep) + len(u) > self.max_chunk_chars:
                out.append(buf)
                buf = u
            else:
                buf = f"{buf}{sep}{u}" if buf else u
        if buf:
            out.append(buf)
        return out

    def _hard_split(self, text: str) -> list[str]:
        out, buf = [], ""
        for word in text.split(" "):
            if buf and len(buf) + 1 + len(word) > self.max_chunk_chars:
                out.append(buf)
                buf = word
            else:
                buf = f"{buf} {word}" if buf else word
        if buf:
            out.append(buf)
        return out

    def _split_text(self, text: str) -> list[str]:
        pieces: list[str] = []
        for para in self._split_paragraphs(text):
            if len(para) <= self.max_chunk_chars:
                pieces.append(para)
                continue
            sentences: list[str] = []
            for s in self._split_sentences(para):
                sentences.extend([s] if len(s) <= self.max_chunk_chars else self._hard_split(s))
            pieces.extend(self._group(sentences, " "))
        return self._group(pieces, "\n\n")


    def _chunk_docuement(self, doc: Document) -> list[Chunk]:
        text = doc.text.strip()
        if not text:
            return []
        if doc.kind == "record":
            parts = [text]
        else:
            raw = self._split_text(text)
            parts = [raw[0]] + [
                f"{self._overlap_tail(raw[i - 1], self.overlap)} {raw[i]}".strip()
                for i in range(1, len(raw))
            ]
            section = doc.meta.get("section")
            if section:
                parts = [p if i == 0 else f"[{section}] {p}" for i, p in enumerate(parts)]
        return [Chunk(text=p, source=doc.source, position=doc.position,
                      chunk_index=i, meta=dict(doc.meta)) for i, p in enumerate(parts)]


    def chunk(self) -> list[Chunk]:
        return [c for d in self.documents for c in self._chunk_docuement(d)]
