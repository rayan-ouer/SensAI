from fastapi import APIRouter, Request

monitoring_router = APIRouter(prefix="/monitoring", tags=["monitoring"])


@monitoring_router.get("/summary")
def monitoring_summary(request: Request) -> dict:
    return request.app.state.monitor.store.get_summary()
