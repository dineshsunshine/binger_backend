"""
Authentication endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import requests

from ....core.database import get_db
from ....core.config import settings
from ....core.auth import create_access_token
from ....models.user import User
from ....schemas.auth import GoogleAuthRequest, TokenResponse

router = APIRouter()


@router.post("/google", response_model=TokenResponse)
async def google_auth(auth_request: GoogleAuthRequest, db: Session = Depends(get_db)):
    """
    Handle Google OAuth authentication.
    Exchanges authorization code for tokens and creates/updates user.
    """
    try:
        # Exchange authorization code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": auth_request.code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": "postmessage",  # For mobile/web apps using Google Sign-In
            "grant_type": "authorization_code"
        }
        
        token_response = requests.post(token_url, data=token_data)
        
        if token_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to exchange authorization code"
            )
        
        tokens = token_response.json()
        id_token_str = tokens.get("id_token")
        
        # Verify and decode the ID token with clock skew tolerance
        # Allow 60 seconds of clock skew to handle timing differences
        idinfo = id_token.verify_oauth2_token(
            id_token_str,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=60
        )
        
        # Extract user information
        google_id = idinfo.get("sub")
        email = idinfo.get("email")
        name = idinfo.get("name")
        picture = idinfo.get("picture")
        
        if not google_id or not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user information from Google"
            )
        
        # Find or create user
        user = db.query(User).filter(User.google_id == google_id).first()
        
        if not user:
            # Create new user
            user = User(
                google_id=google_id,
                email=email,
                name=name,
                picture=picture
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            # Update existing user info
            user.name = name
            user.email = email
            user.picture = picture
            db.commit()
            db.refresh(user)
        
        # Create JWT token
        access_token = create_access_token(data={"sub": user.id})
        
        return TokenResponse(
            token=access_token,
            user={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "picture": user.picture
            }
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )

