from fastapi import APIRouter, HTTPException, Request

from interfaces.api.schemas.input.document import AddDocumentRequest
from interfaces.api.schemas.output.document import AddDocumentResponse
from tools.rag.ingest import DOCUMENT_ERRORS, add_document

document_router = APIRouter(
    prefix="/documents",
    tags=["documents"],
)

@document_router.post("", response_model=AddDocumentResponse)
def create_document(body: AddDocumentRequest, request: Request) -> AddDocumentResponse:
    try:
        added = add_document(body.path, request.app.state.vector_store, request.app.state.embedder)
    except DOCUMENT_ERRORS as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return AddDocumentResponse(source=added.source, chunks=added.chunks)
