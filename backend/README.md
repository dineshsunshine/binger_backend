# Binger Backend API

A production-ready FastAPI backend for the Binger movie watchlist application with Google OAuth authentication.

## Features

- 🔐 **Google OAuth 2.0 Authentication** with JWT tokens
- 📝 **Watchlist Management** - Add, remove, update movies
- ⚙️ **User Settings** - Store and retrieve user preferences
- 🗄️ **Flexible Database** - SQLite for local dev, PostgreSQL for production
- 🌍 **ngrok Integration** - Public URL for local development
- 📚 **Auto-generated API Documentation** - Swagger UI and ReDoc

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL/SQLite** - Database (environment-dependent)
- **JWT** - Token-based authentication
- **Pydantic** - Data validation
- **ngrok** - Local development tunneling

## Quick Start

### 1. Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Update the following required variables:
- `GOOGLE_CLIENT_ID` - Your Google OAuth client ID
- `GOOGLE_CLIENT_SECRET` - Your Google OAuth client secret
- `JWT_SECRET_KEY` - Strong secret for JWT signing
- `NGROK_AUTH_TOKEN` - Your ngrok auth token (optional)
- `NGROK_DOMAIN` - Your ngrok custom domain (optional)

### 3. Run Local Development Server

```bash
python local_server.py
```

This will:
- Start the FastAPI server on port 8000
- Create an ngrok tunnel (if configured)
- Display the public URL for testing

### 4. Access the API

- **Local:** http://localhost:8000
- **Public:** https://your-domain.ngrok-free.dev (if ngrok is configured)
- **API Docs:** /docs
- **ReDoc:** /redoc
- **Health Check:** /health

## API Endpoints

### Authentication

#### `POST /api/auth/google`
Exchange Google OAuth authorization code for JWT token.

**Request:**
```json
{
  "code": "authorization_code_from_google"
}
```

**Response:**
```json
{
  "token": "jwt_token",
  "user": {
    "id": "user_id",
    "name": "User Name",
    "email": "user@example.com",
    "picture": "profile_picture_url"
  }
}
```

### User

#### `GET /api/me`
Get current user profile (requires authentication).

### Watchlist

#### `GET /api/watchlist`
Get all movies in user's watchlist.

#### `POST /api/watchlist`
Add a movie to watchlist.

**Request:** Movie object from frontend

#### `DELETE /api/watchlist/{movieId}`
Remove a movie from watchlist.

#### `PATCH /api/watchlist/{movieId}`
Update a movie (e.g., toggle watched status).

**Request:**
```json
{
  "watched": true
}
```

### Settings

#### `GET /api/settings`
Get user's app settings.

#### `PUT /api/settings`
Update user's app settings (upsert).

## Authentication Flow

1. Frontend initiates Google OAuth flow
2. User authenticates with Google
3. Frontend receives authorization code
4. Frontend sends code to `/api/auth/google`
5. Backend exchanges code for user info
6. Backend creates/updates user and returns JWT
7. Frontend stores JWT and uses it for subsequent requests

All protected endpoints require:
```
Authorization: Bearer <jwt_token>
```

## Database Models

### User
- id (UUID)
- google_id (unique)
- email (unique)
- name
- picture
- timestamps

### WatchlistItem
- id (UUID)
- user_id (FK)
- movie_id (e.g., "movie-550")
- movie_data (JSON - full Movie object)
- added_at
- Unique constraint: (user_id, movie_id)

### UserSetting
- id (UUID)
- user_id (FK, unique)
- settings_data (JSON - AppSettings object)
- timestamps

## Production Deployment

### Environment Variables

Set these on your cloud platform:

```bash
IS_PRODUCTION=true
DATABASE_URL=postgresql://user:password@host:port/dbname
GOOGLE_CLIENT_ID=your-production-client-id
GOOGLE_CLIENT_SECRET=your-production-client-secret
JWT_SECRET_KEY=your-strong-production-secret
CORS_ORIGINS=["https://your-frontend-domain.com"]
```

### Deploy to Render/Railway/Heroku

1. Create PostgreSQL database
2. Create web service from this repository
3. Set environment variables
4. Set start command: `python start_production.py`
5. Deploy!

## Development

### Project Structure

```
backend/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/      # API route handlers
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── watchlist.py
│   │   │   └── settings.py
│   │   └── router.py       # API router setup
│   ├── core/
│   │   ├── config.py       # Configuration
│   │   ├── database.py     # Database setup
│   │   └── auth.py         # Auth utilities
│   ├── models/             # SQLAlchemy models
│   │   ├── user.py
│   │   ├── watchlist.py
│   │   └── settings.py
│   ├── schemas/            # Pydantic schemas
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── watchlist.py
│   │   └── settings.py
│   └── main.py             # FastAPI app
├── local_server.py         # Development server
├── start_production.py     # Production server
├── requirements.txt        # Dependencies
└── .env                    # Environment variables
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Security Notes

- JWT tokens expire after 24 hours (configurable)
- All passwords and secrets should be environment variables
- Use HTTPS in production
- Keep dependencies updated
- Rotate JWT secret periodically

## Support

For issues or questions, please refer to the Backend_Requirements.md document.

## License

Private - Binger App

