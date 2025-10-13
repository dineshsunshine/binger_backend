# Binger Backend - Quick Start

Get your backend running in 5 minutes!

## Prerequisites

- Python 3.9+
- Google OAuth credentials ([Get them here](https://console.cloud.google.com/))

## 1. Install Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Configure Environment

```bash
# Copy example environment file
cp env.example .env
```

Edit `.env` and add your credentials:

```bash
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
JWT_SECRET_KEY=your-random-secret-key
```

**Generate JWT Secret:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 3. Initialize Database

```bash
python scripts/setup_database.py
```

## 4. Run Server

### Option A: Simple (Local Only)

```bash
python -m uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

### Option B: With ngrok (Public URL)

First, add ngrok credentials to `.env`:
```bash
NGROK_AUTH_TOKEN=your-token
```

Then run:
```bash
python local_server.py
```

## 5. Test API

Open http://localhost:8000/docs in your browser.

You'll see interactive API documentation. Try the health check:
- Click on `GET /health`
- Click "Try it out"
- Click "Execute"

## What's Next?

- 📖 Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed setup instructions
- 🚀 Read [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- 📚 Check [backend/README.md](backend/README.md) for API documentation

## API Endpoints

All endpoints are prefixed with `/api`:

### Authentication
- `POST /api/auth/google` - Exchange Google OAuth code for JWT

### User
- `GET /api/me` - Get current user (requires auth)

### Watchlist
- `GET /api/watchlist` - Get user's watchlist
- `POST /api/watchlist` - Add movie to watchlist
- `PATCH /api/watchlist/{movieId}` - Update movie (e.g., mark watched)
- `DELETE /api/watchlist/{movieId}` - Remove from watchlist

### Settings
- `GET /api/settings` - Get user settings
- `PUT /api/settings` - Update user settings

## Troubleshooting

**Import errors?**
```bash
source venv/bin/activate  # Activate virtual environment
```

**Database errors?**
```bash
rm database.db  # Delete old database
python scripts/setup_database.py  # Recreate
```

**OAuth errors?**
- Check Google credentials in `.env`
- Verify authorized origins in Google Cloud Console

## Project Structure

```
backend/
├── app/
│   ├── api/v1/endpoints/   # API routes
│   ├── core/               # Config, database, auth
│   ├── models/             # Database models
│   ├── schemas/            # Pydantic schemas
│   └── main.py             # FastAPI app
├── scripts/                # Utility scripts
├── requirements.txt        # Dependencies
└── .env                    # Your configuration
```

## Need Help?

- Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions
- Review [Backend_Requirements.md](Backend_Requirements.md) for API specifications
- See [Generic_Architecture.md](Generic_Architecture.md) for architecture details

Happy coding! 🎬

