import re

MAX_CHUNK_CHARS = 800
OVERLAP = 80

PARAGRAPH = re.compile(r"\n\s*\n")
SENTENCE = re.compile(r"(?<=[.!?])\s+|(?<=[。！？])")