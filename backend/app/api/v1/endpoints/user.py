"""
User endpoints.
"""
from fastapi import APIRouter, Depends
from ....core.auth import get_current_user
from ....models.user import User
from ....schemas.user import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.
    """
    return UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        picture=current_user.picture
    )

