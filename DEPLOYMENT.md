# Deployment Guide for Binger Backend

This guide covers deploying the Binger backend to various cloud platforms.

## Table of Contents

- [Render Deployment](#render-deployment)
- [Railway Deployment](#railway-deployment)
- [Heroku Deployment](#heroku-deployment)
- [Docker Deployment](#docker-deployment)
- [Environment Variables](#environment-variables)

## Render Deployment

### Prerequisites
- GitHub repository with your backend code
- Render account (free tier available)

### Steps

#### 1. Create PostgreSQL Database

1. Log in to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **PostgreSQL**
3. Configure:
   - **Name**: `binger-db`
   - **Database**: `binger`
   - **User**: `binger`
   - **Region**: Choose closest to your users
   - **Plan**: Free (or paid for production)
4. Click **Create Database**
5. Copy the **Internal Database URL** (starts with `postgresql://`)

#### 2. Create Web Service

1. Click **New +** → **Web Service**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `binger-backend`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: `backend` (if backend is in subdirectory)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python start_production.py`
   - **Plan**: Free (or paid for production)

#### 3. Configure Environment Variables

In the **Environment** tab, add:

```
IS_PRODUCTION=true
DATABASE_URL=<internal-database-url-from-step-1>
GOOGLE_CLIENT_ID=<your-google-client-id>
GOOGLE_CLIENT_SECRET=<your-google-client-secret>
JWT_SECRET_KEY=<your-secret-key>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_HOURS=24
CORS_ORIGINS=["https://your-frontend.com","http://localhost:3000"]
```

#### 4. Deploy

1. Click **Create Web Service**
2. Wait for deployment to complete
3. Your API will be available at: `https://binger-backend.onrender.com`

#### 5. Update Google OAuth

Add Render URL to Google Cloud Console:
- **Authorized JavaScript origins**: `https://binger-backend.onrender.com`
- **Authorized redirect URIs**: Update accordingly

## Railway Deployment

### Prerequisites
- GitHub repository
- Railway account

### Steps

#### 1. Create Project

1. Go to [Railway](https://railway.app/)
2. Click **New Project** → **Deploy from GitHub repo**
3. Select your repository

#### 2. Add PostgreSQL

1. Click **New** → **Database** → **Add PostgreSQL**
2. Railway will automatically set `DATABASE_URL` environment variable

#### 3. Configure Service

1. Go to your backend service
2. **Settings** → **Environment Variables**
3. Add all required variables (see Environment Variables section)

#### 4. Configure Build

Railway auto-detects Python projects. If needed, customize:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python start_production.py`

#### 5. Deploy

Railway auto-deploys on git push to main branch.

## Heroku Deployment

### Prerequisites
- Heroku CLI installed
- Heroku account
- Git repository

### Steps

#### 1. Create Heroku App

```bash
cd backend
heroku login
heroku create binger-backend
```

#### 2. Add PostgreSQL

```bash
heroku addons:create heroku-postgresql:mini
```

This automatically sets `DATABASE_URL`.

#### 3. Set Environment Variables

```bash
heroku config:set IS_PRODUCTION=true
heroku config:set GOOGLE_CLIENT_ID=your-client-id
heroku config:set GOOGLE_CLIENT_SECRET=your-secret
heroku config:set JWT_SECRET_KEY=your-jwt-secret
heroku config:set JWT_ALGORITHM=HS256
heroku config:set 'CORS_ORIGINS=["https://your-frontend.com"]'
```

#### 4. Deploy

```bash
git push heroku main
```

Or use GitHub integration:
1. Go to Heroku Dashboard
2. **Deploy** tab → **GitHub**
3. Connect repository and enable auto-deploy

#### 5. Verify

```bash
heroku logs --tail
heroku open
```

## Docker Deployment

### Create Dockerfile

Create `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "start_production.py"]
```

### Create docker-compose.yml

For local testing with PostgreSQL:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: binger
      POSTGRES_USER: binger
      POSTGRES_PASSWORD: binger
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      IS_PRODUCTION: "true"
      DATABASE_URL: "postgresql://binger:binger@db:5432/binger"
      GOOGLE_CLIENT_ID: ${GOOGLE_CLIENT_ID}
      GOOGLE_CLIENT_SECRET: ${GOOGLE_CLIENT_SECRET}
      JWT_SECRET_KEY: ${JWT_SECRET_KEY}
    depends_on:
      - db

volumes:
  postgres_data:
```

### Run

```bash
docker-compose up --build
```

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `IS_PRODUCTION` | Production mode flag | `true` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `GOOGLE_CLIENT_ID` | Google OAuth client ID | `xxx.apps.googleusercontent.com` |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret | `GOCSPX-xxx` |
| `JWT_SECRET_KEY` | Secret for JWT signing | `random-32-char-string` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `JWT_ACCESS_TOKEN_EXPIRE_HOURS` | Token expiry | `24` |
| `CORS_ORIGINS` | Allowed origins | `["http://localhost:3000"]` |
| `DEBUG` | Debug mode | `false` |
| `PORT` | Server port | `8000` |

### Generate Secrets

```bash
# JWT Secret (32 bytes)
python -c "import secrets; print(secrets.token_hex(32))"

# Or use OpenSSL
openssl rand -hex 32
```

## Post-Deployment

### 1. Verify Health

```bash
curl https://your-backend-url.com/health
```

Expected: `{"status":"healthy","service":"Binger API"}`

### 2. Test API Documentation

Visit: `https://your-backend-url.com/docs`

### 3. Test Authentication

Use the Swagger UI to test:
1. POST `/api/auth/google` with a valid authorization code
2. Copy the returned JWT token
3. Use it to test protected endpoints

### 4. Update Frontend

Update your frontend to use the production API URL:

```javascript
const API_URL = "https://your-backend-url.com/api";
```

### 5. Monitor Logs

**Render:**
```
Dashboard → Service → Logs
```

**Railway:**
```
Dashboard → Service → Logs
```

**Heroku:**
```bash
heroku logs --tail
```

## Database Migrations

When you update database models:

1. **Test locally first** with SQLite
2. **Create migration script** if needed
3. **Backup production database**
4. **Run migrations** carefully

### Manual Migration Example

```python
# scripts/migrate_add_column.py
from app.core.database import engine
from sqlalchemy import text

def migrate():
    with engine.connect() as conn:
        # Check if column exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='new_field'
        """))
        
        if not result.fetchone():
            # Add column
            conn.execute(text("""
                ALTER TABLE users ADD COLUMN new_field VARCHAR(255)
            """))
            conn.commit()
            print("✅ Migration complete")
        else:
            print("✓ Column already exists")

if __name__ == "__main__":
    migrate()
```

## Rollback Strategy

### For Render/Railway

1. Go to **Deployments** tab
2. Find previous successful deployment
3. Click **Redeploy**

### For Heroku

```bash
# List releases
heroku releases

# Rollback to previous
heroku rollback v<version-number>
```

## Troubleshooting

### Database Connection Errors

- Verify `DATABASE_URL` is correctly set
- Check database is running
- Verify firewall rules (if using external DB)
- Check database credentials

### OAuth Errors

- Add production URL to Google Cloud Console
- Verify `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`
- Check authorized redirect URIs

### CORS Errors

- Add frontend URL to `CORS_ORIGINS`
- Format: `["https://frontend.com","http://localhost:3000"]`
- Ensure no trailing slashes

### 500 Errors

- Check application logs
- Verify all environment variables are set
- Test database connection
- Check for missing dependencies

## Security Checklist

- ✅ Use HTTPS in production (automatic on most platforms)
- ✅ Set strong `JWT_SECRET_KEY` (32+ characters)
- ✅ Never commit secrets to Git
- ✅ Use environment variables for all secrets
- ✅ Restrict CORS to trusted domains only
- ✅ Keep dependencies updated
- ✅ Enable database backups
- ✅ Use managed database service (don't manage yourself)
- ✅ Monitor logs for suspicious activity
- ✅ Set up error tracking (Sentry, etc.)

## Maintenance

### Regular Tasks

1. **Weekly**: Review error logs
2. **Monthly**: Update dependencies
3. **Quarterly**: Rotate secrets
4. **Always**: Test in development before deploying

### Updating Dependencies

```bash
# Update packages
pip install --upgrade -r requirements.txt

# Generate new requirements.txt
pip freeze > requirements.txt

# Test locally
# Deploy to production
```

## Support

For platform-specific issues:
- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app/)
- [Heroku Documentation](https://devcenter.heroku.com/)

## Cost Estimates

### Free Tier Limits

**Render Free:**
- Web service sleeps after 15 min inactivity
- 750 hours/month
- PostgreSQL: 90 days then deleted

**Railway Free:**
- $5 credit/month
- Sleeps after inactivity

**Heroku Free:**
- Discontinued (paid plans only)

### Recommended for Production

- **Render**: Starter plan ($7/month per service)
- **Railway**: Pay-as-you-go (typically $10-20/month)
- **Heroku**: Basic plan ($7/month per dyno)

## Next Steps

1. Deploy to chosen platform
2. Test all endpoints
3. Monitor logs for errors
4. Set up automated backups
5. Configure custom domain (optional)
6. Set up SSL certificate (usually automatic)
7. Integrate with frontend
8. Set up monitoring/alerting

Happy deploying! 🚀

