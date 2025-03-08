from fastapi import APIRouter

from app.api.routes import (
    available_match,
    businesses,
    items,
    items_service,
    padel_courts,
)

api_router = APIRouter()
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(businesses.router, prefix="/businesses", tags=["businesses"])
api_router.include_router(
    padel_courts.router, prefix="/padel-courts", tags=["padel-courts"]
)
api_router.include_router(
    items_service.router, prefix="/items-service", tags=["items-service"]
)
api_router.include_router(
    available_match.router,
    prefix="/businesses/{business_id}/padel-courts/{court_name}/available-matches",
    tags=["available-matches"],
)
