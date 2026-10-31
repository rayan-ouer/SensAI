from pydantic import BaseModel


class AddDocumentResponse(BaseModel):
    source: str
    chunks: int
