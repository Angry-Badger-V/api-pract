from fastapi import APIRouter, Depends
from src.dependencies.auth import get_current_user
from src.services import users as user_service

router = APIRouter(
    prefix="/api/user",
    tags=["Users"]
)

@router.get("/me/events")
def get_my_events(user_id: int=Depends(get_current_user)):
    events = user_service.get_user_events(user_id)
    return {"events": events}
