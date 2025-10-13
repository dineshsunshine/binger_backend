"""
Local development server with ngrok tunnel support.
"""
import os
import asyncio
from pyngrok import ngrok, conf
import uvicorn
from app.core.config import settings


def start_ngrok():
    """Start ngrok tunnel."""
    if settings.NGROK_AUTH_TOKEN:
        conf.get_default().auth_token = settings.NGROK_AUTH_TOKEN
    
    # Start ngrok tunnel
    if settings.NGROK_DOMAIN:
        # Use custom domain if configured
        public_url = ngrok.connect(8000, hostname=settings.NGROK_DOMAIN)
    else:
        # Use free ngrok URL
        public_url = ngrok.connect(8000)
    
    print("\n" + "="*60)
    print("🚀 Binger Backend Server Started!")
    print("="*60)
    print(f"📡 Local URL:    http://localhost:8000")
    print(f"🌍 Public URL:   {public_url}")
    print(f"📚 API Docs:     {public_url}/docs")
    print(f"📖 ReDoc:        {public_url}/redoc")
    print("="*60 + "\n")
    
    return public_url


async def main():
    """Main function to run server with ngrok."""
    # Start ngrok tunnel
    if settings.NGROK_AUTH_TOKEN:
        public_url = start_ngrok()
    else:
        print("\n" + "="*60)
        print("⚠️  Warning: No NGROK_AUTH_TOKEN found")
        print("Running without ngrok tunnel (local only)")
        print("="*60 + "\n")
    
    # Configure uvicorn
    config = uvicorn.Config(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
    
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        ngrok.kill()

