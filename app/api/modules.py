from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def placeholder():
    return {"message": "Modules route coming soon"}
