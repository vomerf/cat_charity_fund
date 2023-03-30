from fastapi import APIRouter

from .endpoints import (
    router_charity_project, router_donation, user_router, google_api_router
)


main_router = APIRouter()

main_router.include_router(router_charity_project, prefix='/charity_project', tags=['Charity_Project'])
main_router.include_router(router_donation, prefix='/donation', tags=['Donation'])
main_router.include_router(user_router)
main_router.include_router(google_api_router, prefix='/google', tags=['Google'])