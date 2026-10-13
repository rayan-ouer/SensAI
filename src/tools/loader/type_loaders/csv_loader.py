from ..core.interfaces import BaseLoader, Document

DELIMITERS = (",", ";", "\t", "|")


def _format_csv_line_infos(line: list[str], categories: list[str]) -> str:
    return ", ".join(
        f"{categories[i]}: {line[i]}" for i in range(min(len(categories), len(line)))
    )


class CsvLoader(BaseLoader):
    """Load csv into records"""

    extensions = [".csv"]

    def _row_counts(self, lines: list[str], delim: str) -> list[int]:
        counts = []
        current = 0
        in_quotes = False
        for line in lines:
            for ch in line:
                if ch == '"':
                    in_quotes = not in_quotes
                elif ch == delim and not in_quotes:
                    current += 1
            if not in_quotes:
                counts.append(current)
                current = 0
        return counts

    def _detect_delimiter(self, lines: list[str], sample: int = 50) -> str:
        lines = [line for line in lines if line.strip()][:sample]
        best = ","
        best_key = (0.0, 0)
        for delim in DELIMITERS:
            counts = self._row_counts(lines, delim)
            if not counts:
                continue
            freq = {}
            for count in counts:
                freq[count] = freq.get(count, 0) + 1
            n_seps, n_rows = max(freq.items(), key=lambda kv: (kv[1], kv[0]))
            if n_seps == 0:
                continue
            key = (n_rows / len(counts), n_seps)
            if key > best_key:
                best = delim
                best_key = key
        return best

    def _read_csv_file(self) -> tuple[str, list[str]]:
        raw = self.path.read_bytes()
        text = ""

        for enc in ("utf-8-sig", "utf-16"):
            try:
                text = raw.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            text = raw.decode("latin-1", errors="replace")
        lines = text.splitlines()
        if not lines:
            return "", []
        return lines[0], lines[1:]

    def load(self):
        header, lines = self._read_csv_file()
        if not header or not lines:
            return
        sep = self._detect_delimiter(lines)
        categories = header.split(sep)
        for i, line in enumerate(lines, start=2):
            if not line.strip():
                continue
            values = line.split(sep)
            yield Document(
                text=_format_csv_line_infos(values, categories),
                source=self.path.name,
                meta={
                    "type": self.path.suffix.lstrip("."),
                    "line": i,
                },
            )
