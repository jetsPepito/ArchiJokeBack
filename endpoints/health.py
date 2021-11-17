from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def healthCheck():
    return "Running"


