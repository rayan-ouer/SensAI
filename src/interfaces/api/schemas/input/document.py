from pydantic import BaseModel


class AddDocumentRequest(BaseModel):
    path: str
