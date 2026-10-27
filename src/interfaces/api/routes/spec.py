##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## spec
##

from fastapi import APIRouter, Request

from interfaces.api.schemas.output.spec import SpecResponse
from tools.spec.spec import load_spec

spec_router = APIRouter(
    prefix="/spec",
    tags=["spec"],
)


@spec_router.get("", response_model=SpecResponse)
def get_spec(request: Request) -> SpecResponse:
    return SpecResponse(content=load_spec(request.app.state.config.spec_path))
