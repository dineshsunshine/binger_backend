# Binger App: Backend API Specification

## 1. Overview

This document outlines the requirements for the backend API that will power the Binger application. The backend will be responsible for user authentication, managing user-specific watchlists, and storing user settings. The frontend will handle all interactions with third-party movie data APIs (TMDb, Gemini, OpenAI), but the backend will store the resulting `Movie` objects and user preferences.

## 2. Authentication

The application will use **Google OAuth 2.0** for user authentication, with **JSON Web Tokens (JWT)** for session management.

### Authentication Flow:

1.  **Frontend**: User clicks "Sign in with Google". The frontend initiates the Google OAuth flow.
2.  **Frontend -> Google**: The user authenticates with Google and grants permission.
3.  **Google -> Frontend**: Google returns an `authorization code` to the frontend.
4.  **Frontend -> Backend**: The frontend sends this `authorization code` to our backend.
5.  **Backend -> Google**: The backend exchanges the `authorization code` for an `access token` and `profile information` from Google.
6.  **Backend**: The backend finds a user in the database with the corresponding Google ID or creates a new user if one doesn't exist.
7.  **Backend**: A JWT is generated containing the user's ID (`userId`).
8.  **Backend -> Frontend**: The backend sends this JWT back to the frontend.
9.  **Frontend**: The frontend stores the JWT (e.g., in an HttpOnly cookie or secure storage) and uses it for all subsequent authenticated API requests.

### Endpoints:

#### `POST /api/auth/google`

-   Handles the server-side part of the Google OAuth flow.
-   **Request Body**:
    ```json
    {
      "code": "string" // The authorization code from Google
    }
    ```
-   **Success Response (200 OK)**:
    ```json
    {
      "token": "string", // The JWT
      "user": {
        "id": "string",
        "name": "string",
        "email": "string",
        "picture": "string" // URL
      }
    }
    ```
-   **Error Response (400/500)**: Standard error JSON.

### JWT Security:

-   The JWT should be signed with a strong secret key.
-   It should have a reasonable expiration time (e.g., 1 hour for an access token, 7 days for a refresh token).
-   All API endpoints below (except for the auth endpoint) must be protected and require a valid JWT in the `Authorization: Bearer <token>` header.

## 3. API Endpoints

All endpoints should be prefixed with `/api`.

### User

#### `GET /api/me`

-   Retrieves the profile of the currently authenticated user.
-   **Requires Authentication**: Yes
-   **Success Response (200 OK)**:
    ```json
    {
      "id": "string",
      "name": "string",
      "email": "string",
      "picture": "string"
    }
    ```

### Watchlist

The `Movie` object structure is defined in the frontend `types.ts` file. The backend should store this object as is, likely as a JSONB field or a structured document.

#### `GET /api/watchlist`

-   Retrieves the entire watchlist for the authenticated user.
-   **Requires Authentication**: Yes
-   **Success Response (200 OK)**:
    -   An array of `Movie` objects.
    ```json
    [
      { "id": "...", "title": "...", ... },
      { "id": "...", "title": "...", ... }
    ]
    ```

#### `POST /api/watchlist`

-   Adds a new movie to the user's watchlist. The system should prevent adding duplicate movie IDs for the same user.
-   **Requires Authentication**: Yes
-   **Request Body**: A single `Movie` object.
-   **Success Response (201 Created)**: The created `Movie` object.

#### `DELETE /api/watchlist/:movieId`

-   Removes a movie from the user's watchlist.
-   **Requires Authentication**: Yes
-   **URL Parameters**:
    -   `movieId`: The unique ID of the movie to remove (e.g., `tv-1396`).
-   **Success Response (204 No Content)**.

#### `PATCH /api/watchlist/:movieId`

-   Updates a specific movie on the watchlist. The primary use case is toggling the `watched` status.
-   **Requires Authentication**: Yes
-   **URL Parameters**:
    -   `movieId`: The ID of the movie to update.
-   **Request Body**:
    ```json
    {
      "watched": true
    }
    ```
-   **Success Response (200 OK)**: The fully updated `Movie` object.

### Settings

The `AppSettings` object structure is defined in the frontend `types.ts` file.

#### `GET /api/settings`

-   Retrieves the settings for the authenticated user. If a user has no settings saved, return the default settings.
-   **Requires Authentication**: Yes
-   **Success Response (200 OK)**: An `AppSettings` object.

#### `PUT /api/settings`

-   Updates the settings for the authenticated user. This should be an "upsert" operation (update if exists, create if not).
-   **Requires Authentication**: Yes
-   **Request Body**: An `AppSettings` object.
-   **Success Response (200 OK)**: The saved `AppSettings` object.

## 4. Database Models

### `User`

-   `id`: string (Primary Key, e.g., UUID)
-   `googleId`: string (Unique)
-   `email`: string (Unique)
-   `name`: string
-   `picture`: string (URL)
-   `createdAt`: timestamp
-   `updatedAt`: timestamp

### `WatchlistItem`

-   `id`: string (Primary Key, e.g., UUID)
-   `userId`: string (Foreign Key to `User.id`)
-   `movieId`: string (e.g., "movie-550")
-   `movieData`: JSONB or Document (stores the full `Movie` object from the frontend)
-   `addedAt`: timestamp (for sorting by "Most Recent")
-   **Composite Unique Key**: (`userId`, `movieId`) to prevent duplicates.

### `UserSetting`

-   `id`: string (Primary Key, e.g., UUID)
-   `userId`: string (Foreign Key to `User.id`, Unique)
-   `settingsData`: JSONB or Document (stores the `AppSettings` object)
-   `createdAt`: timestamp
-   `updatedAt`: timestamp
