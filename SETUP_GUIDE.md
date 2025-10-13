# Binger Backend Setup Guide

Complete setup instructions for the Binger backend API.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Google Cloud Console account (for OAuth)
- ngrok account (optional, for local development with public URL)

## Step 1: Install Python Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Set Up Google OAuth

### 2.1 Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google+ API**
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Configure OAuth consent screen:
   - Add app name, user support email, developer email
   - Add scopes: `email`, `profile`, `openid`
   - Add test users (for development)
6. Create OAuth 2.0 Client ID:
   - Application type: **Web application**
   - Authorized JavaScript origins:
     - `http://localhost:3000`
     - `http://localhost:5173`
     - `https://your-ngrok-domain.ngrok-free.dev` (if using ngrok)
   - Authorized redirect URIs:
     - `http://localhost:3000/auth/callback`
     - `postmessage` (for Google Sign-In)
7. Download credentials (client ID and secret)

### 2.2 Configure Environment Variables

Create a `.env` file in the `backend` folder:

```bash
cp env.example .env
```

Edit `.env` and add your credentials:

```bash
# Google OAuth (from step 2.1)
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret

# JWT Secret (generate a strong random string)
JWT_SECRET_KEY=use-openssl-rand-hex-32-to-generate-this

# Database (default for local development)
IS_PRODUCTION=false
DATABASE_URL=sqlite:///./database.db

# CORS (add your frontend URLs)
CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# ngrok (optional - see step 3)
NGROK_AUTH_TOKEN=your-ngrok-token
NGROK_DOMAIN=your-custom-domain.ngrok-free.dev
```

### Generate JWT Secret

Use this command to generate a secure random secret:

```bash
# macOS/Linux:
openssl rand -hex 32

# Python (any OS):
python -c "import secrets; print(secrets.token_hex(32))"
```

## Step 3: Set Up ngrok (Optional)

ngrok provides a public URL for your local server, useful for testing with mobile devices or external webhooks.

### 3.1 Create ngrok Account

1. Go to [ngrok.com](https://ngrok.com/)
2. Sign up for free account
3. Get your auth token from dashboard

### 3.2 (Optional) Reserve Custom Domain

1. In ngrok dashboard, go to **Cloud Edge** → **Domains**
2. Create a free static domain (e.g., `your-app.ngrok-free.dev`)
3. Add to `.env` as `NGROK_DOMAIN`

### 3.3 Configure in .env

```bash
NGROK_AUTH_TOKEN=your_auth_token_here
NGROK_DOMAIN=your-custom-domain.ngrok-free.dev  # optional
```

## Step 4: Initialize Database

```bash
# Make sure you're in the backend directory with venv activated
python scripts/setup_database.py
```

This creates all necessary database tables.

## Step 5: Run the Server

### Local Development (without ngrok)

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access at: http://localhost:8000

### Local Development (with ngrok)

```bash
cd backend
python local_server.py
```

This will:
- Start the FastAPI server
- Create ngrok tunnel
- Display both local and public URLs

Example output:
```
============================================================
🚀 Binger Backend Server Started!
============================================================
📡 Local URL:    http://localhost:8000
🌍 Public URL:   https://your-domain.ngrok-free.dev
📚 API Docs:     https://your-domain.ngrok-free.dev/docs
📖 ReDoc:        https://your-domain.ngrok-free.dev/redoc
============================================================
```

## Step 6: Test the API

### Using Swagger UI

1. Open http://localhost:8000/docs (or your ngrok URL)
2. You'll see interactive API documentation
3. Test endpoints directly from the browser

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "service": "Binger API"}
```

## Step 7: Frontend Integration

Update your frontend configuration to use the backend URL:

```javascript
// For local development
const API_URL = "http://localhost:8000/api";

// For ngrok
const API_URL = "https://your-domain.ngrok-free.dev/api";
```

### Testing Google OAuth Flow

1. Frontend: User clicks "Sign in with Google"
2. Frontend: Gets authorization code from Google
3. Frontend: Sends code to `POST /api/auth/google`
4. Backend: Returns JWT token and user info
5. Frontend: Store token and use in Authorization header

Example authorization header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Production Deployment

### Option 1: Render

1. Create account at [render.com](https://render.com)
2. Create PostgreSQL database:
   - Note the internal/external database URL
3. Create Web Service:
   - Connect GitHub repository
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python start_production.py`
4. Add environment variables:
   ```
   IS_PRODUCTION=true
   DATABASE_URL=<postgres-url-from-render>
   GOOGLE_CLIENT_ID=<your-client-id>
   GOOGLE_CLIENT_SECRET=<your-client-secret>
   JWT_SECRET_KEY=<your-secret>
   CORS_ORIGINS=["https://your-frontend-domain.com"]
   ```
5. Deploy!

### Option 2: Railway

Similar to Render:
1. Create PostgreSQL database
2. Create service from GitHub
3. Set environment variables
4. Deploy

### Update Google OAuth for Production

Add production URLs to Google Cloud Console:
- Authorized JavaScript origins: `https://your-backend-domain.com`
- Authorized redirect URIs: Update accordingly

## Troubleshooting

### Database Issues

```bash
# Reset database (WARNING: deletes all data)
rm database.db
python scripts/setup_database.py
```

### Import Errors

Make sure virtual environment is activated:
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows
```

### CORS Errors

Add your frontend URL to `CORS_ORIGINS` in `.env`:
```bash
CORS_ORIGINS=["http://localhost:3000","https://your-frontend.com"]
```

### Google OAuth Errors

- Verify client ID and secret in `.env`
- Check authorized origins in Google Cloud Console
- Ensure redirect URIs match

### ngrok Issues

- Verify auth token is correct
- Check if domain is available (for custom domains)
- Try without custom domain first

## Development Tips

### Hot Reload

The development server auto-reloads on code changes.

### API Documentation

Always available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

### Database Inspection

```bash
# Install SQLite browser or use command line
sqlite3 database.db

# List tables
.tables

# View users
SELECT * FROM users;

# Exit
.quit
```

### Environment Variables Priority

1. `.env` file (local development)
2. System environment variables (production)

## Security Checklist

- ✅ Use strong JWT_SECRET_KEY (32+ random characters)
- ✅ Never commit `.env` file to git
- ✅ Use HTTPS in production
- ✅ Keep GOOGLE_CLIENT_SECRET private
- ✅ Rotate secrets periodically
- ✅ Use environment-specific OAuth credentials
- ✅ Enable CORS only for trusted domains

## Next Steps

1. Test all endpoints using Swagger UI
2. Integrate with your frontend application
3. Set up production deployment
4. Configure monitoring and logging
5. Set up automated backups (production)

## Support

Refer to:
- `README.md` - API documentation
- `Backend_Requirements.md` - Detailed requirements
- `Generic_Architecture.md` - Architecture patterns

Happy coding! 🚀

