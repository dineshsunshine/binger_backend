# 🔗 Shareable Link Feature - Frontend Integration Guide

## Overview

The Binger backend supports shareable links that allow users to share their watchlist (movies) and/or saved restaurants with others via a public URL. This guide covers the shareable link API endpoints and implementation.

---

## ⚠️ Important Concepts

### Unified Shareable Links
- **One link per user:** Each user gets ONE shareable link that covers both movies and restaurants
- **Entity control:** Users can choose what to share using the `entity_types` parameter:
  - `["movies"]` - Only show movies
  - `["restaurants"]` - Only show restaurants  
  - `["movies", "restaurants"]` - Show both (default)
- **Persistent URL:** Once created, the shareable URL remains the same even if deactivated/reactivated
- **Public access:** Shareable link pages do NOT require authentication

### Link Behavior
- **First creation:** Generates a unique token and shareable URL
- **Re-creation:** If a user deletes and recreates a link, they get the **same URL** (not a new one)
- **Deactivation:** Disabling a link makes it temporarily inaccessible
- **Reactivation:** Re-enabling restores access to the same URL

---

## 🔑 Base URLs

- **Production:** `https://binger-backend.onrender.com/Binger/api`
- **Development:** `https://your-ngrok-url.ngrok-free.dev/Binger/api`

---

## 📍 API Endpoints

### 1. Create or Get Shareable Link

Create a new shareable link or retrieve an existing one. If a link exists (even if deactivated), it will be reactivated with the specified entity types.

**Endpoint:** `POST /shareable-link`  
**Auth Required:** Yes  
**Headers:**
```javascript
{
  "Authorization": "Bearer YOUR_JWT_TOKEN",
  "Content-Type": "application/json"
}
```

**Request Body:**
```json
{
  "entity_types": ["movies", "restaurants"]
}
```

**Parameters:**
- `entity_types` (optional): Array of strings specifying what to share
  - Options: `["movies"]`, `["restaurants"]`, or `["movies", "restaurants"]`
  - Default: `["movies", "restaurants"]`

**Request Example:**
```javascript
// Create link to share both movies and restaurants
const response = await fetch('https://binger-backend.onrender.com/Binger/api/shareable-link', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    entity_types: ["movies", "restaurants"]
  })
});

const data = await response.json();
console.log(data.shareable_url); // https://binger-backend.onrender.com/Binger/shared/watchlist/abc123...
```

**Response:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "token": "unique_token_string",
  "entity_types": ["movies", "restaurants"],
  "shareable_url": "https://binger-backend.onrender.com/Binger/shared/watchlist/unique_token_string",
  "is_active": true,
  "created_at": "2025-10-14T12:00:00Z",
  "updated_at": "2025-10-14T12:00:00Z"
}
```

**Response Fields:**
- `id`: Database ID of the shareable link
- `user_id`: ID of the user who owns the link
- `token`: Unique token used in the shareable URL
- `entity_types`: Array indicating what's shared (movies, restaurants, or both)
- `shareable_url`: Full public URL to share with others
- `is_active`: Whether the link is currently active
- `created_at`: When the link was first created
- `updated_at`: When the link was last modified

---

### 2. Get Shareable Link

Retrieve the current user's existing shareable link.

**Endpoint:** `GET /shareable-link`  
**Auth Required:** Yes

**Request Example:**
```javascript
const response = await fetch('https://binger-backend.onrender.com/Binger/api/shareable-link', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});

const data = await response.json();
```

**Success Response (200):**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "token": "unique_token_string",
  "entity_types": ["movies", "restaurants"],
  "shareable_url": "https://binger-backend.onrender.com/Binger/shared/watchlist/unique_token_string",
  "is_active": true,
  "created_at": "2025-10-14T12:00:00Z",
  "updated_at": "2025-10-14T12:00:00Z"
}
```

**Error Response (404):**
```json
{
  "detail": "No shareable link found"
}
```

---

### 3. Update Shareable Link Entity Types

Update what entities (movies, restaurants, or both) are shown on the shareable link.

**Endpoint:** `PUT /shareable-link`  
**Auth Required:** Yes

**Request Body:**
```json
{
  "entity_types": ["movies"]
}
```

**Request Example:**
```javascript
// Change to only share movies
const response = await fetch('https://binger-backend.onrender.com/Binger/api/shareable-link', {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    entity_types: ["movies"]
  })
});

const data = await response.json();
```

**Response:** Updated shareable link object (same structure as create/get)

**Use Cases:**
- User wants to share only movies (hide restaurants)
- User wants to share only restaurants (hide movies)
- User wants to share both

---

### 4. Delete Shareable Link

Deactivate (disable) the shareable link. The URL will return a 404 error until reactivated.

**Endpoint:** `DELETE /shareable-link`  
**Auth Required:** Yes

**Request Example:**
```javascript
await fetch('https://binger-backend.onrender.com/Binger/api/shareable-link', {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
```

**Success Response:** `204 No Content`

**Error Response (404):**
```json
{
  "detail": "No shareable link found"
}
```

**Note:** This does NOT permanently delete the link. If the user creates a link again (POST), they'll get the **same URL** back.

---

## 🌐 Public Shareable Page

The shareable link directs to a public, aesthetically pleasing page that displays the user's content.

**URL Format:**
```
https://binger-backend.onrender.com/Binger/shared/watchlist/{token}
```

**Features:**
- **No authentication required** - Anyone with the link can view
- **Responsive design** - Works on mobile, tablet, and desktop
- **Netflix-like UI** - Modern, sleek interface
- **Separate sections** - Movies and restaurants shown in different sections based on `entity_types`
- **Sorting & filtering** - For movies: All/Watched/To Watch, Recently Added, Release Year
- **Movie details** - Full movie information with posters, descriptions, cast, etc.
- **Restaurant details** - Full restaurant information with images, location, cuisine, etc.

**Example:**
```
https://binger-backend.onrender.com/Binger/shared/watchlist/abc123xyz
```

---

## 💡 Implementation Examples

### Complete Share Feature Component

```javascript
import React, { useState, useEffect } from 'react';

const ShareFeature = () => {
  const [shareableLink, setShareableLink] = useState(null);
  const [entityTypes, setEntityTypes] = useState(['movies', 'restaurants']);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  // Fetch existing shareable link on mount
  useEffect(() => {
    fetchShareableLink();
  }, []);

  const fetchShareableLink = async () => {
    try {
      const response = await fetch('https://binger-backend.onrender.com/Binger/api/shareable-link', {
        headers: {
          'Authorization': `Bearer ${getToken()}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setShareableLink(data);
        setEntityTypes(data.entity_types);
      }
    } catch (error) {
      console.error('Error fetching shareable link:', error);
    }
  };

  const createShareableLink = async () => {
    setLoading(true);
    try {
      const response = await fetch('https://binger-backend.onrender.com/Binger/api/shareable-link', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${getToken()}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          entity_types: entityTypes
        })
      });

      const data = await response.json();
      setShareableLink(data);
    } catch (error) {
      console.error('Error creating shareable link:', error);
    } finally {
      setLoading(false);
    }
  };

  const updateEntityTypes = async (newEntityTypes) => {
    setLoading(true);
    try {
      const response = await fetch('https://binger-backend.onrender.com/Binger/api/shareable-link', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${getToken()}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          entity_types: newEntityTypes
        })
      });

      const data = await response.json();
      setShareableLink(data);
      setEntityTypes(data.entity_types);
    } catch (error) {
      console.error('Error updating entity types:', error);
    } finally {
      setLoading(false);
    }
  };

  const deleteShareableLink = async () => {
    if (!confirm('Are you sure you want to disable your shareable link?')) return;

    setLoading(true);
    try {
      await fetch('https://binger-backend.onrender.com/Binger/api/shareable-link', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${getToken()}`
        }
      });

      setShareableLink(null);
    } catch (error) {
      console.error('Error deleting shareable link:', error);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(shareableLink.shareable_url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const toggleEntityType = (type) => {
    let newTypes;
    if (entityTypes.includes(type)) {
      // Remove if already included
      newTypes = entityTypes.filter(t => t !== type);
      // Ensure at least one is selected
      if (newTypes.length === 0) return;
    } else {
      // Add if not included
      newTypes = [...entityTypes, type];
    }

    if (shareableLink) {
      updateEntityTypes(newTypes);
    } else {
      setEntityTypes(newTypes);
    }
  };

  return (
    <div className="share-feature">
      <h2>Share Your Collection</h2>
      
      {/* Entity Type Selector */}
      <div className="entity-selector">
        <label>What do you want to share?</label>
        <div className="checkbox-group">
          <label>
            <input
              type="checkbox"
              checked={entityTypes.includes('movies')}
              onChange={() => toggleEntityType('movies')}
            />
            Movies
          </label>
          <label>
            <input
              type="checkbox"
              checked={entityTypes.includes('restaurants')}
              onChange={() => toggleEntityType('restaurants')}
            />
            Restaurants
          </label>
        </div>
      </div>

      {/* Shareable Link Display */}
      {shareableLink ? (
        <div className="link-display">
          <div className="link-status">
            <span className={shareableLink.is_active ? 'active' : 'inactive'}>
              {shareableLink.is_active ? 'Active' : 'Inactive'}
            </span>
          </div>
          
          <div className="link-url">
            <input
              type="text"
              value={shareableLink.shareable_url}
              readOnly
            />
            <button onClick={copyToClipboard}>
              {copied ? 'Copied!' : 'Copy'}
            </button>
          </div>

          <div className="link-actions">
            <button onClick={deleteShareableLink} disabled={loading}>
              Disable Link
            </button>
          </div>
        </div>
      ) : (
        <button
          onClick={createShareableLink}
          disabled={loading}
          className="create-button"
        >
          {loading ? 'Creating...' : 'Create Shareable Link'}
        </button>
      )}
    </div>
  );
};

// Helper function to get auth token
const getToken = () => {
  return localStorage.getItem('authToken');
};

export default ShareFeature;
```

---

## 🎨 UI/UX Recommendations

### Share Button Placement
- Add a "Share" button in the main navigation or profile section
- Show share icon (🔗) in the UI
- Make it easily discoverable

### Link Management Screen
```
┌─────────────────────────────────────┐
│  Share Your Collection             │
├─────────────────────────────────────┤
│                                     │
│  What do you want to share?         │
│  ☑ Movies  ☑ Restaurants           │
│                                     │
│  Your Shareable Link:               │
│  ┌──────────────────────────┐      │
│  │ https://binger.../abc123 │ Copy │
│  └──────────────────────────┘      │
│                                     │
│  Link is Active ●                   │
│                                     │
│  [Disable Link]                     │
└─────────────────────────────────────┘
```

### Share Options Modal
- **Copy Link:** Primary action
- **Share via:** WhatsApp, Twitter, Facebook, Email
- **QR Code:** Generate QR code for easy mobile sharing
- **Preview:** Button to open the public page in a new tab

---

## 🔒 Security & Privacy

### Important Notes
1. **Public Access:** Anyone with the link can view the content
2. **No Personal Info:** The public page does NOT show user email or sensitive information
3. **Token Security:** Tokens are cryptographically secure (16+ bytes)
4. **Revocable:** Users can disable links at any time
5. **Same URL:** Re-enabling gives the same URL (prevents link spam)

### Best Practices
- Warn users that the link is public and anyone can view it
- Show a preview of what will be shared before enabling
- Provide clear instructions on how to disable sharing
- Consider adding analytics (view count) in the future

---

## 📊 Error Handling

### Common Errors

**404 - No shareable link found:**
```javascript
// User hasn't created a link yet
// Show "Create Link" button
```

**401 - Unauthorized:**
```javascript
// Invalid or expired JWT token
// Redirect to login
```

**500 - Server error:**
```javascript
// Show error message with retry option
alert('Something went wrong. Please try again.');
```

---

## 🧪 Testing Checklist

- [ ] Create shareable link with movies only
- [ ] Create shareable link with restaurants only
- [ ] Create shareable link with both
- [ ] Update entity types after creation
- [ ] Copy link to clipboard
- [ ] Open public page in incognito/private mode (no auth)
- [ ] Verify correct content shows based on entity_types
- [ ] Delete link and verify 404 on public page
- [ ] Re-create link and verify same URL is returned
- [ ] Test on mobile, tablet, and desktop
- [ ] Test with empty watchlist/restaurant list

---

## 🌟 Advanced Features (Future)

Consider implementing these enhancements:

1. **View Analytics:** Show how many times the link was viewed
2. **Custom Slugs:** Allow users to customize their shareable URL
3. **Expiration Dates:** Set automatic expiration for links
4. **Password Protection:** Add optional password to access shared page
5. **Theme Customization:** Let users choose the public page theme
6. **Social Preview:** Generate Open Graph tags for better link previews

---

## 📞 Support

If you encounter issues with the shareable link feature:

1. Check that `entity_types` is a valid array
2. Ensure JWT token is valid and not expired
3. Verify the public URL is accessible without authentication
4. Check browser console for any CORS or network errors
5. Test in incognito mode to rule out caching issues

---

## 🔄 API Changelog

**Version 1.0 (Current)**
- Unified shareable links for movies and restaurants
- `entity_types` parameter for controlling what to share
- Persistent URLs across deletion/recreation
- Public, responsive HTML page for viewing shared content

---

**Need help?** Refer to the main integration guides:
- `FRONTEND_INTEGRATION_GUIDE.md` - Movie/watchlist features
- `RESTAURANT_INTEGRATION.md` - Restaurant features

