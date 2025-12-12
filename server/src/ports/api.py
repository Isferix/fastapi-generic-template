from fastapi import APIRouter

# from ..settings import get_settings

# settings = get_settings()

api = APIRouter()


@api.get("/health")
async def health_check():
    return {"status": "ok"}


# @api.get("/settings")
# async def get_current_settings():
#     return dict(settings)
