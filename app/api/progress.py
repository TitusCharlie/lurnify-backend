from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def placeholder():
    return {"message": "Progress route coming soon"}
