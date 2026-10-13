class EmbeddingError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self) -> str:
        return f"Embedding error: {self.message}"
