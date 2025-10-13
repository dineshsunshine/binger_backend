"""
Settings endpoints.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....core.auth import get_current_user
from ....models.user import User
from ....models.settings import UserSetting
from ....schemas.settings import AppSettings

router = APIRouter()

# Default settings to return if user has no settings
DEFAULT_SETTINGS = {}


@router.get("")
async def get_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's application settings.
    Returns default settings if user has no saved settings.
    """
    user_setting = db.query(UserSetting).filter(
        UserSetting.user_id == current_user.id
    ).first()
    
    if user_setting:
        return user_setting.settings_data
    else:
        return DEFAULT_SETTINGS


@router.put("")
async def update_settings(
    settings: AppSettings,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user's application settings.
    Creates new settings if they don't exist (upsert operation).
    """
    user_setting = db.query(UserSetting).filter(
        UserSetting.user_id == current_user.id
    ).first()
    
    settings_dict = settings.dict()
    
    if user_setting:
        # Update existing settings
        user_setting.settings_data = settings_dict
    else:
        # Create new settings
        user_setting = UserSetting(
            user_id=current_user.id,
            settings_data=settings_dict
        )
        db.add(user_setting)
    
    db.commit()
    db.refresh(user_setting)
    
    return user_setting.settings_data

