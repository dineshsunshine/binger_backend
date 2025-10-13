# Binger Backend

Production-ready FastAPI backend for the Binger movie watchlist application.

## Features

- 🔐 Google OAuth 2.0 Authentication with JWT
- 📝 Complete watchlist management (CRUD operations)
- ⚙️ User settings management
- 🗄️ SQLite (dev) / PostgreSQL (production)
- 🌐 CORS enabled
- 📚 Auto-generated API documentation

## Quick Start

### Development

1. **Install dependencies:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp backend/env.example backend/.env
   # Edit .env with your Google OAuth credentials
   ```

3. **Run server:**
   ```bash
   cd backend
   python scripts/setup_database.py  # First time only
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
   ```

4. **Access API:**
   - Local: http://localhost:8001/Binger/docs
   - ngrok: https://your-ngrok-url.ngrok-free.dev/Binger/docs

### Production (Render)

Deployed automatically from the `main` branch.

- **Production URL:** TBD (will be https://binger-backend.onrender.com)
- **API Docs:** https://binger-backend.onrender.com/Binger/docs

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | `xxx.apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret | `GOCSPX-xxx` |
| `JWT_SECRET_KEY` | Secret for JWT signing | 32+ char random string |
| `IS_PRODUCTION` | Production mode flag | `true` or `false` |
| `DATABASE_URL` | PostgreSQL URL (production) | `postgresql://...` |
| `CORS_ORIGINS` | Allowed origins | `*` or `https://domain1.com,https://domain2.com` |

## API Documentation

See [FRONTEND_INTEGRATION_GUIDE.md](FRONTEND_INTEGRATION_GUIDE.md) for complete API documentation.

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Production database
- **SQLite** - Development database
- **Pydantic** - Data validation
- **JWT** - Authentication tokens

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
└── .env                    # Environment variables (not in git)
```

## Deployment

### Render Deployment

1. Push code to GitHub
2. Connect repository to Render
3. Render will auto-deploy using `render.yaml`
4. Configure environment variables in Render dashboard

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## License

Private - Binger App

## Support

For API integration help, see [FRONTEND_INTEGRATION_GUIDE.md](FRONTEND_INTEGRATION_GUIDE.md)

