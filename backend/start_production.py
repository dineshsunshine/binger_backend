"""
Production server startup script.
"""
import os
import uvicorn
from app.main import app

if __name__ == "__main__":
    # Production configuration
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000)),
        log_level="info",
        access_log=True
    )

