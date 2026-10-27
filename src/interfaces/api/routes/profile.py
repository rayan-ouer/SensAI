##
## EPITECH PROJECT, 2026
## SensAI
## File description:
## profile
##

from fastapi import APIRouter, Request

from interfaces.api.schemas.output.profile import ProfileResponse, ProfilesResponse

profile_router = APIRouter(
    prefix="/profiles",
    tags=["profiles"],
)


@profile_router.get("", response_model=ProfilesResponse)
def get_profiles(request: Request) -> ProfilesResponse:
    profiles = [
        ProfileResponse(key=key, name=profile.name, role=profile.role)
        for key, profile in request.app.state.profiles.items()
    ]
    return ProfilesResponse(profiles=profiles, default=request.app.state.config.default_profile)
