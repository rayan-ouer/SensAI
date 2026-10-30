##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## model
##

from fastapi import APIRouter, Request

from interfaces.api.schemas.output.model import ModelsResponse
from interfaces.api.utils.models import available_models

model_router = APIRouter(
    prefix="/models",
    tags=["models"],
)


@model_router.get("", response_model=ModelsResponse)
def get_models(request: Request) -> ModelsResponse:
    return ModelsResponse(models=available_models(request.app.state.config), default=request.app.state.config.model)
