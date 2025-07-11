from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def placeholder():
    return {"message": "lessons route coming soon"}
