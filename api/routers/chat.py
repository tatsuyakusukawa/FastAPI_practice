from fastapi import APIRouter

router = APIRouter()


@router.get("/chat")
async def hello():
    return {"messege":"hello"}



