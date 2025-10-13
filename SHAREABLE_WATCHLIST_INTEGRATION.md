# Shareable Watchlist Feature - Frontend Integration Guide

## Overview

This feature allows users to create a unique, public shareable link to their watchlist. The link can be shared with friends who can view the watchlist without logging in on a beautifully designed, Netflix-style page.

---

## Key Features

✅ **One Link Per User** - Each user can have only one unique shareable link  
✅ **Public Access** - No login required to view shared watchlists  
✅ **Beautiful UI** - Netflix-inspired design with bold aesthetics  
✅ **Filtering** - View All, Watched, or To Watch movies  
✅ **Stats Display** - Shows total movies, watched count, and to-watch count  
✅ **Revokable** - Users can delete their shareable link anytime  

---

## API Endpoints

### Base URLs
- **Development:** `https://zestfully-chalky-nikia.ngrok-free.dev/Binger/api`
- **Production:** `https://binger-backend.onrender.com/Binger/api`

---

## 1. Create or Get Shareable Link

**Endpoint:** `POST /api/shareable-link`  
**Auth Required:** Yes (Bearer token)  
**Description:** Creates a new shareable link or returns existing one if already created

**Request:**
```javascript
const response = await fetch(`${API_BASE_URL}/shareable-link`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${userToken}`,
    'Content-Type': 'application/json'
  }
});

const data = await response.json();
```

**Response (200 OK):**
```json
{
  "id": "uuid-here",
  "user_id": "user-uuid",
  "token": "unique-token-string",
  "shareable_url": "https://binger-backend.onrender.com/Binger/shared/watchlist/unique-token-string",
  "is_active": true,
  "created_at": "2025-10-13T12:00:00Z"
}
```

**Key Fields:**
- `shareable_url` - The complete URL to share with friends
- `token` - Unique token for this user's watchlist
- `is_active` - Whether the link is active (always true for existing links)

---

## 2. Get Existing Shareable Link

**Endpoint:** `GET /api/shareable-link`  
**Auth Required:** Yes (Bearer token)  
**Description:** Retrieves the user's existing shareable link, or returns null if none exists

**Request:**
```javascript
const response = await fetch(`${API_BASE_URL}/shareable-link`, {
  headers: {
    'Authorization': `Bearer ${userToken}`
  }
});

const data = await response.json();
// Returns same structure as CREATE, or null if no link exists
```

**Response (200 OK):**
```json
{
  "id": "uuid-here",
  "user_id": "user-uuid",
  "token": "unique-token-string",
  "shareable_url": "https://binger-backend.onrender.com/Binger/shared/watchlist/unique-token-string",
  "is_active": true,
  "created_at": "2025-10-13T12:00:00Z"
}
```

**Or if no link exists:**
```json
null
```

---

## 3. Delete Shareable Link

**Endpoint:** `DELETE /api/shareable-link`  
**Auth Required:** Yes (Bearer token)  
**Description:** Deletes/revokes the user's shareable link. The link will no longer work.

**Request:**
```javascript
const response = await fetch(`${API_BASE_URL}/shareable-link`, {
  method: 'DELETE',
  headers: {
    'Authorization': `Bearer ${userToken}`
  }
});

const data = await response.json();
```

**Response (200 OK):**
```json
{
  "message": "Shareable link deleted successfully",
  "success": true
}
```

**Error Response (404):**
```json
{
  "detail": "No shareable link found"
}
```

---

## Frontend Implementation Guide

### Step 1: Check if User Has a Shareable Link

When the user opens the "Share Watchlist" feature:

```javascript
async function checkShareableLink() {
  try {
    const response = await fetch(`${API_BASE_URL}/shareable-link`, {
      headers: {
        'Authorization': `Bearer ${userToken}`
      }
    });
    
    const data = await response.json();
    
    if (data === null) {
      // No link exists - show "Create Link" button
      return null;
    } else {
      // Link exists - show the link and "Delete Link" button
      return data;
    }
  } catch (error) {
    console.error('Error checking shareable link:', error);
    return null;
  }
}
```

### Step 2: Create a Shareable Link

When user clicks "Create Link":

```javascript
async function createShareableLink() {
  try {
    const response = await fetch(`${API_BASE_URL}/shareable-link`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${userToken}`,
        'Content-Type': 'application/json'
      }
    });
    
    const data = await response.json();
    
    // Show the shareable URL to user
    const shareableUrl = data.shareable_url;
    
    // Display it in UI with copy button
    displayShareableLink(shareableUrl);
    
    return data;
  } catch (error) {
    console.error('Error creating shareable link:', error);
  }
}
```

### Step 3: Delete a Shareable Link

When user clicks "Delete Link" or "Revoke Access":

```javascript
async function deleteShareableLink() {
  try {
    const response = await fetch(`${API_BASE_URL}/shareable-link`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${userToken}`
      }
    });
    
    const data = await response.json();
    
    if (data.success) {
      // Link deleted - update UI to show "Create Link" button
      console.log(data.message);
      // Hide the link display
      hideShareableLink();
    }
  } catch (error) {
    console.error('Error deleting shareable link:', error);
  }
}
```

---

## UI/UX Recommendations

### Suggested User Flow:

1. **User navigates to "Share Watchlist" section in their profile/settings**

2. **If no link exists:**
   - Show message: "Share your watchlist with friends!"
   - Show button: "Create Shareable Link"
   
3. **If link exists:**
   - Display the shareable URL in a text box (read-only)
   - Show "Copy Link" button (copies to clipboard)
   - Show "Open Link" button (opens in new tab for preview)
   - Show "Delete Link" button (with confirmation dialog)
   - Show creation date: "Created on: [date]"

4. **After creating link:**
   - Show success message with confetti/animation
   - Display the URL with copy functionality
   - Optionally: Show share buttons for social media

5. **After deleting link:**
   - Show confirmation: "Link deleted successfully"
   - Hide the URL display
   - Return to "Create Link" state

### Example UI Structure:

```
┌─────────────────────────────────────────────┐
│  Share Your Watchlist                       │
├─────────────────────────────────────────────┤
│                                             │
│  Your watchlist is currently: [Private]    │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │ Create Shareable Link                │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  Share your movie collection with friends! │
│                                             │
└─────────────────────────────────────────────┘

After creating:

┌─────────────────────────────────────────────┐
│  Share Your Watchlist                       │
├─────────────────────────────────────────────┤
│                                             │
│  Your watchlist is currently: [Public]     │
│                                             │
│  Shareable Link:                            │
│  ┌──────────────────────────────────────┐  │
│  │ https://binger-backend.onrender...   │  │
│  └──────────────────────────────────────┘  │
│                                             │
│  ┌────────┐  ┌────────┐  ┌────────────┐   │
│  │ Copy   │  │ Open   │  │ Delete Link│   │
│  └────────┘  └────────┘  └────────────┘   │
│                                             │
│  Created: Oct 13, 2025                     │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Copy to Clipboard Example

```javascript
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    // Show success toast/notification
    showToast('Link copied to clipboard!');
  }).catch(err => {
    console.error('Failed to copy:', err);
    // Fallback for older browsers
    fallbackCopyTextToClipboard(text);
  });
}

function fallbackCopyTextToClipboard(text) {
  const textArea = document.createElement('textarea');
  textArea.value = text;
  document.body.appendChild(textArea);
  textArea.select();
  try {
    document.execCommand('copy');
    showToast('Link copied to clipboard!');
  } catch (err) {
    console.error('Fallback: Could not copy text:', err);
  }
  document.body.removeChild(textArea);
}
```

---

## Important Notes

### 1. One Link Per User
- Each user can only have ONE active shareable link at a time
- Creating a new link while one exists will return the existing link
- To get a new token, user must first delete the existing link

### 2. Public Access
- Anyone with the link can view the watchlist
- No authentication required for viewing
- The page is beautifully designed and mobile-responsive

### 3. Real-time Updates
- When user updates their watchlist, the shared page reflects changes immediately
- No need to regenerate the link

### 4. Link Format
```
Development: https://zestfully-chalky-nikia.ngrok-free.dev/Binger/shared/watchlist/{token}
Production:  https://binger-backend.onrender.com/Binger/shared/watchlist/{token}
```

### 5. Security
- Tokens are cryptographically secure (16-byte URL-safe strings)
- Links can be revoked anytime by deleting them
- Deleted links return 404 page

---

## The Public Watchlist Page

When someone visits the shareable link, they see:

### Features:
- 🎬 **Hero Section** with user's name: "[Name]'s Watchlist"
- 📊 **Stats Bar** showing Total Movies, Watched, To Watch
- 🎯 **Filter Buttons** - All, Watched, To Watch
- 🎨 **Netflix-style Grid** of movie posters
- ✨ **Hover Effects** with smooth animations
- ✅ **Watched Badge** on completed movies
- ⭐ **Ratings Display** for each movie
- 📱 **Mobile Responsive** design

### Design Highlights:
- Bold, modern aesthetics
- Red (#E50914) Netflix-inspired color scheme
- Beautiful gradient backgrounds
- Smooth transitions and hover effects
- Clean typography with Bebas Neue and Inter fonts
- Dark theme for movie posters

---

## Testing

### Test Flow:

1. **Create Link:**
   ```bash
   curl -X POST ${API_BASE_URL}/shareable-link \
     -H "Authorization: Bearer ${TOKEN}"
   ```

2. **Get Link:**
   ```bash
   curl ${API_BASE_URL}/shareable-link \
     -H "Authorization: Bearer ${TOKEN}"
   ```

3. **Visit Public Page:**
   ```
   Open: https://your-domain/Binger/shared/watchlist/{token}
   ```

4. **Delete Link:**
   ```bash
   curl -X DELETE ${API_BASE_URL}/shareable-link \
     -H "Authorization: Bearer ${TOKEN}"
   ```

5. **Verify Deletion:**
   ```
   Visit link again - should show 404 page
   ```

---

## Error Handling

### Common Errors:

**401 Unauthorized:**
```json
{
  "detail": "Not authenticated"
}
```
→ User token is missing or invalid

**404 Not Found:**
```json
{
  "detail": "No shareable link found"
}
```
→ Trying to delete a link that doesn't exist

**Public Page 404:**
- Link doesn't exist or has been deleted
- Shows beautiful 404 page with Binger branding

---

## Example Complete Implementation

```javascript
class ShareableLinkManager {
  constructor(apiBaseUrl, authToken) {
    this.apiBaseUrl = apiBaseUrl;
    this.authToken = authToken;
  }

  async checkLink() {
    const response = await fetch(`${this.apiBaseUrl}/shareable-link`, {
      headers: { 'Authorization': `Bearer ${this.authToken}` }
    });
    return await response.json();
  }

  async createLink() {
    const response = await fetch(`${this.apiBaseUrl}/shareable-link`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.authToken}`,
        'Content-Type': 'application/json'
      }
    });
    return await response.json();
  }

  async deleteLink() {
    const response = await fetch(`${this.apiBaseUrl}/shareable-link`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${this.authToken}` }
    });
    return await response.json();
  }

  copyToClipboard(url) {
    navigator.clipboard.writeText(url)
      .then(() => alert('Link copied!'))
      .catch(err => console.error('Copy failed:', err));
  }

  openInNewTab(url) {
    window.open(url, '_blank');
  }
}

// Usage
const manager = new ShareableLinkManager(API_BASE_URL, userToken);

// Check existing link
const existingLink = await manager.checkLink();
if (existingLink) {
  console.log('Shareable URL:', existingLink.shareable_url);
} else {
  // Create new link
  const newLink = await manager.createLink();
  console.log('Created URL:', newLink.shareable_url);
}
```

---

## Questions?

For API documentation, visit:
- **Swagger UI:** `https://binger-backend.onrender.com/Binger/docs`
- **ReDoc:** `https://binger-backend.onrender.com/Binger/redoc`

The shareable link endpoints are under the **"shareable"** tag in the API docs.

---

**Happy sharing! 🎬✨**

