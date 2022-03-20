from fastapi import APIRouter

router = APIRouter()


@router.get("/me", tags=["users"])
async def read_user():
    return {"username": "fakecurrentuser"}
