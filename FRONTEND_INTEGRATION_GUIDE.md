# Binger Backend API Integration Guide

## API Base URL
- **Development:** `https://zestfully-chalky-nikia.ngrok-free.dev/Binger`
- **Production:** `https://binger-backend.onrender.com/Binger`

## API Documentation

### Development
- **Swagger UI:** `https://zestfully-chalky-nikia.ngrok-free.dev/Binger/docs`
- **ReDoc:** `https://zestfully-chalky-nikia.ngrok-free.dev/Binger/redoc`

### Production  
- **Swagger UI:** `https://binger-backend.onrender.com/Binger/docs`
- **ReDoc:** `https://binger-backend.onrender.com/Binger/redoc`

---

## Authentication Flow

### 1. Google OAuth Integration

**Endpoint:** `POST /Binger/api/auth/google`

**Frontend Steps:**
1. User clicks "Sign in with Google"
2. Use Google OAuth library to get authorization code
3. Send the code to our backend
4. Backend returns JWT token and user info
5. Store JWT token securely (localStorage or httpOnly cookie)
6. Include JWT in all subsequent API requests

**Request:**
```javascript
const response = await fetch('https://zestfully-chalky-nikia.ngrok-free.dev/Binger/api/auth/google', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    code: authorizationCodeFromGoogle
  })
});

const data = await response.json();
// data = { token: "jwt_token", user: { id, name, email, picture } }
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "uuid",
    "name": "John Doe",
    "email": "john@example.com",
    "picture": "https://..."
  }
}
```

**Store the token and use in all authenticated requests:**
```javascript
localStorage.setItem('bingerToken', data.token);
```

---

## API Endpoints

### User Profile

**Get Current User**
- **Endpoint:** `GET /Binger/api/me`
- **Auth Required:** Yes
- **Response:** User object

```javascript
const response = await fetch('https://zestfully-chalky-nikia.ngrok-free.dev/Binger/api/me', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

**Response:**
```json
{
  "id": "uuid",
  "name": "John Doe",
  "email": "john@example.com",
  "picture": "https://..."
}
```

---

### Watchlist Management

#### Get All Watchlist Items
- **Endpoint:** `GET /Binger/api/watchlist`
- **Auth Required:** Yes
- **Response:** Array of Movie objects

```javascript
const response = await fetch('https://zestfully-chalky-nikia.ngrok-free.dev/Binger/api/watchlist', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
const movies = await response.json();
// movies = [{ id, title, ... }, ...]
```

**Response:**
```json
[
  {
    "id": "movie-550",
    "title": "Fight Club",
    "overview": "...",
    "poster_path": "...",
    "release_date": "1999-10-15",
    "watched": false
  }
]
```

#### Add Movie to Watchlist
- **Endpoint:** `POST /Binger/api/watchlist`
- **Auth Required:** Yes
- **Request Body:** Movie object from TMDb/frontend
- **Response:** Created movie object (201 Created)

```javascript
const response = await fetch('https://zestfully-chalky-nikia.ngrok-free.dev/Binger/api/watchlist', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    id: "movie-550",
    title: "Fight Club",
    overview: "A ticking-time-bomb insomniac...",
    poster_path: "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
    release_date: "1999-10-15",
    vote_average: 8.4,
    // ... any other movie data from TMDb
  })
});
```

**Note:** The backend prevents duplicate movies. If the movie already exists, you'll get a 400 error.

#### Update Movie (Toggle Watched Status)
- **Endpoint:** `PATCH /Binger/api/watchlist/{movieId}`
- **Auth Required:** Yes
- **Request Body:** Fields to update
- **Response:** Updated movie object (200 OK)

```javascript
const response = await fetch(`https://zestfully-chalky-nikia.ngrok-free.dev/Binger/api/watchlist/movie-550`, {
  method: 'PATCH',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    watched: true
  })
});
```

**Request Body:**
```json
{
  "watched": true
}
```

#### Remove Movie from Watchlist
- **Endpoint:** `DELETE /Binger/api/watchlist/{movieId}`
- **Auth Required:** Yes
- **Response:** 204 No Content

```javascript
await fetch(`https://zestfully-chalky-nikia.ngrok-free.dev/Binger/api/watchlist/movie-550`, {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

---

### User Settings

#### Get User Settings
- **Endpoint:** `GET /Binger/api/settings`
- **Auth Required:** Yes
- **Response:** Settings object (or default {} if none saved)

```javascript
const response = await fetch('https://zestfully-chalky-nikia.ngrok-free.dev/Binger/api/settings', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
const settings = await response.json();
```

**Response:**
```json
{
  "theme": "dark",
  "notifications": true,
  "language": "en"
}
```

#### Update User Settings
- **Endpoint:** `PUT /Binger/api/settings`
- **Auth Required:** Yes
- **Request Body:** Complete settings object
- **Response:** Saved settings object (200 OK)

```javascript
const response = await fetch('https://zestfully-chalky-nikia.ngrok-free.dev/Binger/api/settings', {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    theme: 'dark',
    notifications: true,
    language: 'en'
    // ... any settings fields
  })
});
```

---

## Error Handling

All endpoints return standard HTTP status codes:

- **200 OK** - Success
- **201 Created** - Resource created
- **204 No Content** - Success with no response body
- **400 Bad Request** - Invalid request data
- **401 Unauthorized** - Missing or invalid token
- **403 Forbidden** - Valid token but insufficient permissions
- **404 Not Found** - Resource not found
- **500 Internal Server Error** - Server error

**Error Response Format:**
```json
{
  "detail": "Error message here"
}
```

**Example Error Handling:**
```javascript
try {
  const response = await fetch(url, options);
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Something went wrong');
  }
  
  return await response.json();
} catch (error) {
  console.error('API Error:', error.message);
  // Handle error in UI
}
```

---

## Complete Example: React Implementation

```javascript
// auth.js
export async function signInWithGoogle() {
  // 1. Get Google auth code (using @react-oauth/google or similar)
  const googleCode = await getGoogleAuthCode();
  
  // 2. Exchange code for JWT
  const response = await fetch('https://zestfully-chalky-nikia.ngrok-free.dev/Binger/api/auth/google', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code: googleCode })
  });
  
  if (!response.ok) {
    throw new Error('Authentication failed');
  }
  
  const { token, user } = await response.json();
  localStorage.setItem('bingerToken', token);
  return user;
}

// api.js
const API_BASE = 'https://zestfully-chalky-nikia.ngrok-free.dev/Binger/api';

function getAuthHeaders() {
  const token = localStorage.getItem('bingerToken');
  return {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  };
}

export async function getWatchlist() {
  const response = await fetch(`${API_BASE}/watchlist`, {
    headers: getAuthHeaders()
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch watchlist');
  }
  
  return await response.json();
}

export async function addToWatchlist(movie) {
  const response = await fetch(`${API_BASE}/watchlist`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(movie)
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }
  
  return await response.json();
}

export async function toggleWatched(movieId, watched) {
  const response = await fetch(`${API_BASE}/watchlist/${movieId}`, {
    method: 'PATCH',
    headers: getAuthHeaders(),
    body: JSON.stringify({ watched })
  });
  
  if (!response.ok) {
    throw new Error('Failed to update movie');
  }
  
  return await response.json();
}

export async function removeFromWatchlist(movieId) {
  const response = await fetch(`${API_BASE}/watchlist/${movieId}`, {
    method: 'DELETE',
    headers: getAuthHeaders()
  });
  
  if (!response.ok) {
    throw new Error('Failed to remove movie');
  }
}

export async function getUserSettings() {
  const response = await fetch(`${API_BASE}/settings`, {
    headers: getAuthHeaders()
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch settings');
  }
  
  return await response.json();
}

export async function updateUserSettings(settings) {
  const response = await fetch(`${API_BASE}/settings`, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(settings)
  });
  
  if (!response.ok) {
    throw new Error('Failed to update settings');
  }
  
  return await response.json();
}
```

---

## Important Notes

1. **All authenticated endpoints require the Authorization header:**
   ```
   Authorization: Bearer <jwt_token>
   ```

2. **JWT tokens expire after 24 hours** - implement token refresh or re-authentication

3. **Movie IDs format:** Use format like `"movie-550"` or `"tv-1396"` (prefix + TMDb ID)

4. **CORS is enabled** for common frontend development ports

5. **Duplicate prevention:** Backend prevents adding the same movie twice to watchlist

6. **Data flexibility:** You can store any movie data structure - backend stores it as-is in JSON format

7. **ngrok warning page:** When accessing the development API from browser, you might see an ngrok warning page first - just click "Visit Site" to proceed

---

## Google OAuth Setup

### Required Configuration

**Google Client ID:**
```
862851161074-94fsq17r1325t789ckf61nd3oadtbfjd.apps.googleusercontent.com
```

**Authorized JavaScript Origins:**
- `https://zestfully-chalky-nikia.ngrok-free.dev`
- Your frontend domain (when deployed)

**Authorized Redirect URIs:**
- `postmessage` (for mobile/SPA)
- `https://zestfully-chalky-nikia.ngrok-free.dev/Binger/api/auth/google`

---

## Testing

### Test Endpoints Interactively
Visit: **https://zestfully-chalky-nikia.ngrok-free.dev/Binger/docs**

The Swagger UI allows you to:
- See all available endpoints
- View request/response schemas
- Test endpoints directly from browser
- Get example responses

### Health Check
```bash
curl https://zestfully-chalky-nikia.ngrok-free.dev/Binger/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Binger API"
}
```

---

## Environment Variables (for frontend .env)

**Development:**
```env
VITE_API_BASE_URL=https://zestfully-chalky-nikia.ngrok-free.dev/Binger/api
VITE_GOOGLE_CLIENT_ID=862851161074-94fsq17r1325t789ckf61nd3oadtbfjd.apps.googleusercontent.com
```

**Production:**
```env
# Production URL will be configured when backend is deployed
VITE_API_BASE_URL=https://your-production-domain.com/Binger/api
VITE_GOOGLE_CLIENT_ID=862851161074-94fsq17r1325t789ckf61nd3oadtbfjd.apps.googleusercontent.com
```

---

## Shareable Watchlist Feature 🔗

### Overview
Users can create a unique, public shareable link to their watchlist. Anyone with the link can view the watchlist without logging in on a beautifully designed, Netflix-style page.

**Key Features:**
- ✅ One unique link per user
- ✅ Public access (no login required)
- ✅ Beautiful Netflix-inspired UI
- ✅ Filtering (All, Watched, To Watch)
- ✅ Revokable anytime

### Create or Get Shareable Link

**Endpoint:** `POST /Binger/api/shareable-link`  
**Auth Required:** Yes

```javascript
const response = await fetch('https://binger-backend.onrender.com/Binger/api/shareable-link', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});

const data = await response.json();
// data.shareable_url - The URL to share with friends
```

**Response:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "token": "unique-token",
  "shareable_url": "https://binger-backend.onrender.com/Binger/shared/watchlist/unique-token",
  "is_active": true,
  "created_at": "2025-10-13T12:00:00Z"
}
```

### Get Existing Link

**Endpoint:** `GET /Binger/api/shareable-link`  
**Auth Required:** Yes

```javascript
const response = await fetch('https://binger-backend.onrender.com/Binger/api/shareable-link', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const data = await response.json();
// Returns link data or null if no link exists
```

### Delete Shareable Link

**Endpoint:** `DELETE /Binger/api/shareable-link`  
**Auth Required:** Yes

```javascript
await fetch('https://binger-backend.onrender.com/Binger/api/shareable-link', {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

**📚 For detailed integration guide, see:** `SHAREABLE_WATCHLIST_INTEGRATION.md`

---

## Support & Documentation

- **Interactive API Docs:** `/Binger/docs`
- **Alternative Docs:** `/Binger/redoc`
- **Health Check:** `/Binger/health`

For backend issues or questions, contact the backend team.

---

**Happy coding! 🎬🚀**

