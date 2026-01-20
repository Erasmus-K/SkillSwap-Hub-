"""
Google OAuth routes for Calendar API authentication
"""
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from ...services.google_calendar import google_calendar_service

router = APIRouter()

REDIRECT_URI = "http://localhost:8000/auth/google/callback"

@router.get("/google/authorize")
def google_authorize():
    """
    Initiate Google OAuth flow
    Redirects user to Google's authorization page
    """
    try:
        auth_url = google_calendar_service.get_authorization_url(REDIRECT_URI)
        return {"authorization_url": auth_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get authorization URL: {str(e)}")

@router.get("/google/callback")
def google_callback(code: str = None, error: str = None):
    """
    Handle Google OAuth callback
    Exchanges authorization code for access token
    """
    if error:
        raise HTTPException(status_code=400, detail=f"Authorization failed: {error}")
    
    if not code:
        raise HTTPException(status_code=400, detail="No authorization code provided")
    
    try:
        token_data = google_calendar_service.exchange_code_for_token(code, REDIRECT_URI)
        return {
            "message": "Google Calendar connected successfully!",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to exchange code: {str(e)}")

@router.get("/google/status")
def google_status():
    """
    Check if Google Calendar is connected
    """
    is_connected = google_calendar_service.load_credentials()
    return {
        "connected": is_connected,
        "message": "Google Calendar is connected" if is_connected else "Google Calendar is not connected"
    }
