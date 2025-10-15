# 🍽️ Restaurant Feature - Frontend Integration Guide

## Overview

The Binger backend now supports restaurant search and management, powered by **Hybrid AI** (OpenAI GPT-4 + Google Gemini) with real restaurant images from Google Custom Search API. This guide covers all restaurant-related API endpoints.

---

## 🚀 NEW: Quick Search Feature

We now have a **fast, two-step search flow** for optimal user experience:

1. **Quick Search** (`/quick-search`) - Fast initial results using Google Custom Search API
   - ⚡ Returns results in < 2 seconds
   - 💰 Cost-effective (uses free Google Custom Search API)
   - 📦 Lightweight data (name, snippet, images, URL)
   - 🎯 Perfect for search dropdown/list view

2. **Detailed Search** (`/search`) - Full restaurant details with AI
   - 🧠 Comprehensive information from OpenAI/Gemini
   - 💵 Only called when user clicks on a result
   - 📊 Complete data for saving to user's list

**👉 See [RESTAURANT_QUICK_SEARCH_INTEGRATION.md](./RESTAURANT_QUICK_SEARCH_INTEGRATION.md) for the complete quick search guide!**

**Recommended Flow:**
```
User types → Quick Search (fast) → Show results → User clicks → Detailed Search (full data) → Save
```

This approach provides a **much better user experience** and is **80% more cost-efficient** than searching with AI on every keystroke!

---

## ⚠️ Important Notes

### AI Search Performance
- **Response Time:** Restaurant search can take **3-10 seconds** due to AI processing and image fetching
  - Hybrid AI search (OpenAI + Gemini): 4-10 seconds
  - Quick search (Google Custom Search only): < 2 seconds
- **User Experience:** Always show a loading state with a message like "Searching with AI..." or "Finding restaurants..."
- **Best Practice:** Use `/quick-search` for initial results, then `/search` when user clicks for full details
- **Error Handling:** AI services may occasionally fail or timeout - handle these gracefully with retry options

### Shareable Links
- Restaurant shareable links are **unified** with movie shareable links
- Use `/api/shareable-link` with `entity_types` parameter (not `/api/restaurants/shareable-link`)
- One link per user can show movies, restaurants, or both

### Restaurant Images & Data Sources ✨ **REAL PHOTOS!**
- **🎉 Google Custom Search API Integration!** All restaurant search results include **real, high-quality images** from the web
- **How It Works:** After AI finds restaurants, the backend automatically fetches real photos using Google Custom Search API
- **Image Sources:** Google Maps, restaurant websites, Instagram, food blogs, TripAdvisor, Zomato, Yelp, and more
- **Quality:** Professional, high-resolution photos of food, restaurant interiors, and exteriors
- **Search Approach:** Hybrid AI (OpenAI + Gemini) combined with real Google images for best results
- **Fallback:** If no images are found, the `images` array will be empty `[]`
- **Recommendation:** Always implement a fallback placeholder image in your UI for rare cases without photos

---

## 🔑 Base URLs

- **Production:** `https://binger-backend.onrender.com/Binger/api`
- **Development:** `https://your-ngrok-url.ngrok-free.dev/Binger/api`

---

## 📍 API Endpoints

### 1. Quick Search (RECOMMENDED for Fast Results)

Get fast, lightweight restaurant results for initial search UI.

**Endpoint:** `POST /restaurants/quick-search`  
**Auth Required:** Yes  
**Response Time:** < 2 seconds

**Request Body:**
```json
{
  "query": "sushi",
  "location": "Dubai"
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "zuma_dubai",
      "name": "Zuma Dubai",
      "snippet": "Contemporary Japanese restaurant...",
      "url": "https://...",
      "images": ["https://...", "https://..."],
      "location": "Dubai"
    }
  ],
  "total": 5
}
```

**👉 For complete quick search documentation, see [RESTAURANT_QUICK_SEARCH_INTEGRATION.md](./RESTAURANT_QUICK_SEARCH_INTEGRATION.md)**

**Use Case:** Perfect for search dropdowns, autocomplete, and initial results. When user clicks on a result, call the detailed search endpoint below.

---

### 2. Detailed Search (Hybrid AI: OpenAI + Gemini)

Search for restaurants using hybrid AI approach combining OpenAI and Google Gemini for comprehensive results.

**Endpoint:** `POST /restaurants/search`  
**Auth Required:** Yes  
**Response Time:** 3-10 seconds (AI processing + image fetching)

**Recommendation:** Use `/quick-search` first for fast results, then call `/search` when user clicks on a restaurant for full details.

**Request Body:**
```json
{
  "query": "Bla Bla",
  "location": "Dubai"
}
```

**Parameters:**
- `query` (required): Restaurant name or search query (e.g., "Bla Bla", "best sushi", "Italian restaurant")
- `location` (required): City or location to search in (e.g., "Dubai", "New York", "Tokyo")

**Request Example:**
```javascript
const response = await fetch('https://binger-backend.onrender.com/Binger/api/restaurants/search', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: "Bla Bla",
    location: "Dubai"
  })
});

const data = await response.json();
```

**What You Get:**
- ✅ Hybrid AI results from both OpenAI and Gemini
- ✅ Real, high-quality images from Google Custom Search API
- ✅ Comprehensive restaurant information
- ✅ 0-5 matching restaurants in the specified location

**Response:**
```json
{
  "restaurants": [
    {
      "id": "bla_bla_jbr_dubai",
      "restaurant_name": "Bla Bla Dubai",
      "description": "An expansive all-day social destination...",
      "google_maps_url": "https://www.google.com/maps/search/?api=1&query=...",
      "website": "https://blabladubai.ae/",
      "menu_url": "https://blabladubai.ae/menus/",
      "city": "Dubai",
      "country": "United Arab Emirates",
      "phone_number": "+971 4 584 4111",
      "hours": {
        "monday": "11:00 am – 12:00 am",
        "tuesday": "11:00 am – 12:00 am",
        "wednesday": "11:00 am – 12:00 am",
        "thursday": "11:00 am – 12:00 am",
        "friday": "11:00 am – 1:00 am",
        "saturday": "11:00 am – 1:00 am",
        "sunday": "11:00 am – 12:00 am",
        "timezone": "Asia/Dubai"
      },
      "cuisine": "International / Fusion",
      "type": "Beach Club / Restaurant / Nightlife Venue",
      "drinks": {
        "serves_alcohol": true,
        "special_drinks": ["Signature cocktails", "Full bar"]
      },
      "diet_type": "mixed (veg / non-veg / vegan / gluten-free options)",
      "social_media": {
        "instagram": "blabladubai",
        "facebook": "",
        "twitter": "",
        "tiktok": "",
        "tripadvisor": "https://www.tripadvisor.com/..."
      },
      "known_for": [
        "21 themed bars under one roof",
        "Beach club with infinity pools",
        "Live music & DJs"
      ],
      "images": [
        "https://...",
        "https://..."
      ]
    }
  ]
}
```

**Notes:**
- Returns 0-5 restaurants per search
- Empty array if no results found
- Search uses hybrid AI (OpenAI + Gemini) for comprehensive results
- Real images are fetched from Google Custom Search API automatically

---

### 3. Save a Restaurant

Add a restaurant to the user's saved list.

**Endpoint:** `POST /restaurants/saved`  
**Auth Required:** Yes

**Request:**
```javascript
const response = await fetch('https://binger-backend.onrender.com/Binger/api/restaurants/saved', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    restaurant_data: {
      id: "bla_bla_jbr_dubai",
      restaurant_name: "Bla Bla Dubai",
      // ... all restaurant fields from search result
    },
    visited: false,  // optional, default: false
    personal_rating: 4,  // optional, 1-5
    notes: "Want to try for anniversary",  // optional
    tags: ["Anniversary", "Special Occasion"]  // optional
  })
});

const data = await response.json();
```

**Response:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "restaurant_id": "bla_bla_jbr_dubai",
  "restaurant_data": { /* full restaurant object */ },
  "visited": false,
  "personal_rating": 4,
  "notes": "Want to try for anniversary",
  "tags": ["Anniversary", "Special Occasion"],
  "added_at": "2025-10-14T12:00:00Z",
  "updated_at": "2025-10-14T12:00:00Z"
}
```

**Error Responses:**
- `400 Bad Request` - Restaurant already saved
- `401 Unauthorized` - Invalid/missing token

---

### 4. Get Saved Restaurant IDs

Get a list of restaurant IDs that the user has already saved. Useful for checking which restaurants are already in the saved list.

**Endpoint:** `GET /restaurants/saved/ids`  
**Auth Required:** Yes

**Request:**
```javascript
const response = await fetch('https://binger-backend.onrender.com/Binger/api/restaurants/saved/ids', {
  headers: { 'Authorization': `Bearer ${token}` }
});

const data = await response.json();
// Returns: ["bla_bla_jbr_dubai", "kailash_parbat_mumbai", ...]
```

**Response:**
```json
[
  "bla_bla_jbr_dubai",
  "kailash_parbat_mumbai",
  "another_restaurant_id"
]
```

---

### 5. Get Saved Restaurants

Retrieve user's saved restaurants with optional filters and sorting.

**Endpoint:** `GET /restaurants/saved`  
**Auth Required:** Yes

**Query Parameters:**
- `sort_by` - `name`, `added_at`, `city`, `cuisine` (default: `added_at`)
- `order` - `asc`, `desc` (default: `desc`)
- `visited` - `true`, `false`, `all` (default: `all`)
- `city` - Filter by city name (e.g., `Dubai`)
- `cuisine` - Filter by cuisine type (e.g., `Japanese`)
- `country` - Filter by country name (e.g., `UAE`)

**Examples:**

```javascript
// Get all restaurants, most recently added first
const response = await fetch('https://binger-backend.onrender.com/Binger/api/restaurants/saved', {
  headers: { 'Authorization': `Bearer ${token}` }
});

// Get only visited restaurants in Dubai
const response = await fetch(
  'https://binger-backend.onrender.com/Binger/api/restaurants/saved?visited=true&city=Dubai',
  { headers: { 'Authorization': `Bearer ${token}` }}
);

// Get Japanese restaurants, sorted by name
const response = await fetch(
  'https://binger-backend.onrender.com/Binger/api/restaurants/saved?cuisine=Japanese&sort_by=name&order=asc',
  { headers: { 'Authorization': `Bearer ${token}` }}
);
```

**Response:**
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "restaurant_id": "bla_bla_jbr_dubai",
    "restaurant_data": { /* full restaurant object */ },
    "visited": false,
    "personal_rating": 4,
    "notes": "Want to try",
    "tags": ["Anniversary"],
    "added_at": "2025-10-14T12:00:00Z",
    "updated_at": "2025-10-14T12:00:00Z"
  }
]
```

---

### 6. Get Single Restaurant

Get details of a specific saved restaurant.

**Endpoint:** `GET /restaurants/saved/{restaurant_id}`  
**Auth Required:** Yes

**Request:**
```javascript
const response = await fetch(
  `https://binger-backend.onrender.com/Binger/api/restaurants/saved/${restaurantId}`,
  { headers: { 'Authorization': `Bearer ${token}` }}
);
```

**Response:** Same as single restaurant object above

**Error Responses:**
- `404 Not Found` - Restaurant not in saved list

---

### 7. Update Saved Restaurant

Update visit status, rating, notes, or tags.

**Endpoint:** `PUT /restaurants/saved/{restaurant_id}`  
**Auth Required:** Yes

**Request:**
```javascript
const response = await fetch(
  `https://binger-backend.onrender.com/Binger/api/restaurants/saved/${restaurantId}`,
  {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      visited: true,  // optional
      personal_rating: 5,  // optional, 1-5
      notes: "Loved it! Great ambiance",  // optional
      tags: ["Anniversary", "Highly Recommended"]  // optional
    })
  }
);
```

**Response:** Updated restaurant object

**Note:** All fields are optional - only send what you want to update

---

### 8. Delete Saved Restaurant

Remove a restaurant from saved list.

**Endpoint:** `DELETE /restaurants/saved/{restaurant_id}`  
**Auth Required:** Yes

**Request:**
```javascript
await fetch(
  `https://binger-backend.onrender.com/Binger/api/restaurants/saved/${restaurantId}`,
  {
    method: 'DELETE',
    headers: { 'Authorization': `Bearer ${token}` }
  }
);
```

**Response:** `204 No Content` (success)

---

## 🔗 Shareable Links (Unified for Movies & Restaurants)

> **Important:** Shareable links are now **unified** for both movies and restaurants. You use the same `/api/shareable-link` endpoint with an `entity_types` parameter to control what's shown (movies, restaurants, or both).

### 9. Create or Update Shareable Link

Generate a public shareable link for user's list. You can specify what to share: movies, restaurants, or both.

**Endpoint:** `POST /api/shareable-link`  
**Auth Required:** Yes

**Request Body:**
```json
{
  "entity_types": ["movies", "restaurants"]
}
```

Options for `entity_types`:
- `["movies"]` - Share only movies
- `["restaurants"]` - Share only restaurants  
- `["movies", "restaurants"]` - Share both (default)

**Request Example:**
```javascript
const response = await fetch(
  'https://binger-backend.onrender.com/Binger/api/shareable-link',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      entity_types: ["restaurants"]  // Or ["movies"] or ["movies", "restaurants"]
    })
  }
);

const data = await response.json();
```

**Response:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "token": "unique-token",
  "entity_types": ["restaurants"],
  "shareable_url": "https://binger-backend.onrender.com/Binger/shared/watchlist/unique-token",
  "is_active": true,
  "created_at": "2025-10-14T12:00:00Z",
  "updated_at": "2025-10-14T12:00:00Z"
}
```

**Key Points:**
- ✅ One link per user (shared for both movies and restaurants)
- ✅ Same URL returned if link already exists (even after delete/recreate)
- ✅ You can update `entity_types` anytime to change what's visible
- ✅ Public - no auth required to view
- ✅ The public page will show separate sections for movies and restaurants

---

### 10. Update What's Shared

Change which entities are shown in the shareable link without creating a new URL.

**Endpoint:** `PUT /api/shareable-link`  
**Auth Required:** Yes

**Request Example:**
```javascript
await fetch('https://binger-backend.onrender.com/Binger/api/shareable-link', {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    entity_types: ["movies", "restaurants"]  // Now show both
  })
});
```

---

### 11. Get Existing Shareable Link

**Endpoint:** `GET /api/shareable-link`  
**Auth Required:** Yes

Returns existing link with current `entity_types` or `null` if none exists.

**Response:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "token": "unique-token",
  "entity_types": ["movies", "restaurants"],
  "shareable_url": "https://binger-backend.onrender.com/Binger/shared/watchlist/unique-token",
  "is_active": true,
  "created_at": "2025-10-14T12:00:00Z",
  "updated_at": "2025-10-14T12:00:00Z"
}
```

---

### 12. Revoke Shareable Link

**Endpoint:** `DELETE /api/shareable-link`  
**Auth Required:** Yes

Deactivates the link (same URL will be restored if recreated later).

**Response:**
```json
{
  "message": "Shareable link revoked successfully. The same URL will be restored if you create a new link.",
  "success": true
}
```

---

## 🎨 UI/UX Recommendations

### Restaurant Search Flow

**Recommended Two-Step Flow:**
1. **Search Box** - Let users type restaurant names or queries
2. **Quick Search** - Show fast results (< 2 seconds) in dropdown
3. **User Clicks Result** - Trigger detailed search
4. **Loading State** - Show "Getting full details..." (3-10 seconds)
5. **Results Display** - Show complete restaurant info
6. **Save Button** - "+ Save" button on each result
7. **Empty State** - "No restaurants found. Try a different search."

**Alternative: Direct Full Search** (if skipping quick search):
1. **Search Box** - Let users type and submit
2. **Loading State** - Show "Searching with AI..." (3-10 seconds)
3. **Results Display** - Show 0-5 restaurants in cards
4. **Save Button** - "+ Save" button on each result
5. **Empty State** - "No restaurants found. Try a different search."

### Restaurant Card Design
Display key info:
- Restaurant name (bold, large)
- Cuisine type & city
- Star rating (if user rated it)
- Visited badge (if visited)
- Quick actions: View Details, Mark as Visited, Delete

### Restaurant Detail View
Full information including:
- All hours (expandable)
- Clickable links: Google Maps, Website, Menu
- Social media buttons
- Known for highlights
- Personal notes section
- Tags display
- Visit checkbox
- Rating (1-5 stars)

### Filters & Sorting
- Tabs: All / To Visit / Visited
- Sort dropdown: Recently Added, Name (A-Z), City, Cuisine
- Filter by: City, Cuisine, Country

---

## 📊 Data Fields Reference

### Required Fields (Always Present)
- `id` - Unique identifier
- `restaurant_name` - Name of restaurant

### Optional Fields
All other fields may be `null` or empty string. Always check before displaying:

```javascript
// Safe access example
const city = restaurant.restaurant_data.city || "Unknown City";
const website = restaurant.restaurant_data.website;

if (website) {
  // Show website link
}
```

---

## 🚨 Error Handling

```javascript
try {
  const response = await fetch(url, options);
  
  if (!response.ok) {
    if (response.status === 401) {
      // Redirect to login
    } else if (response.status === 400) {
      const error = await response.json();
      alert(error.detail);  // "Restaurant already saved"
    } else if (response.status === 404) {
      alert("Restaurant not found");
    } else {
      alert("Something went wrong. Please try again.");
    }
    return;
  }
  
  const data = await response.json();
  // Handle success
  
} catch (error) {
  console.error("Network error:", error);
  alert("Network error. Please check your connection.");
}
```

---

## 💡 Implementation Tips

### 1. Debounce Search Input
```javascript
// Wait 500ms after user stops typing before searching
const debouncedSearch = debounce((query) => {
  searchRestaurants(query);
}, 500);
```

### 2. Cache Search Results
Store recent searches to avoid duplicate AI calls:
```javascript
const searchCache = new Map();

async function searchRestaurants(query) {
  if (searchCache.has(query)) {
    return searchCache.get(query);
  }
  
  const results = await fetch(/*...*/);
  searchCache.set(query, results);
  return results;
}
```

### 3. Optimistic UI Updates
Update UI immediately, rollback if API fails:
```javascript
// Mark as visited immediately
setRestaurant(prev => ({ ...prev, visited: true }));

try {
  await updateRestaurant(id, { visited: true });
} catch (error) {
  // Rollback on error
  setRestaurant(prev => ({ ...prev, visited: false }));
}
```

---

## 🔄 State Management Example (React)

```javascript
// Context or Redux store
const RestaurantContext = {
  savedRestaurants: [],
  searchResults: [],
  isSearching: false,
  shareableLink: null
};

// Actions
async function searchRestaurants(query) {
  setIsSearching(true);
  try {
    const results = await api.searchRestaurants(query);
    setSearchResults(results.restaurants);
  } catch (error) {
    handleError(error);
  } finally {
    setIsSearching(false);
  }
}

async function saveRestaurant(restaurant) {
  try {
    const saved = await api.saveRestaurant(restaurant);
    setSavedRestaurants(prev => [saved, ...prev]);
    toast.success("Restaurant saved!");
  } catch (error) {
    if (error.status === 400) {
      toast.error("Already saved!");
    }
  }
}
```

---

## 🌐 Public Shareable Page

The shareable link (`/shared/restaurants/{token}`) displays:
- ✅ User's name (e.g., "Dinesh's Restaurants")
- ✅ All saved restaurants (public view)
- ✅ Filters: All, Visited, To Visit
- ✅ Sort options
- ✅ Beautiful, responsive UI
- ✅ No login required

---

## 📝 Notes

1. **Hybrid AI Search** - Results combine OpenAI and Gemini knowledge bases. Always handle empty results gracefully.
2. **Real Images** - All restaurant images are fetched from Google Custom Search API for authenticity.
3. **Personal Data** - `visited`, `personal_rating`, `notes`, and `tags` are user-specific and private.
4. **Restaurant IDs** - Generated by the AI models. Same restaurant might have slightly different IDs in different searches.
5. **Duplicate Prevention** - Backend prevents saving same `restaurant_id` twice per user.
6. **Search Performance** - Detailed search takes 3-10 seconds. Use quick search for better UX.

---

## 🎯 Quick Start Checklist

- [ ] Implement restaurant search UI
- [ ] Display search results in cards
- [ ] Add "Save" functionality
- [ ] Create saved restaurants list view
- [ ] Add filters and sorting
- [ ] Implement mark as visited
- [ ] Add rating system (1-5 stars)
- [ ] Create detail view with all info
- [ ] Add shareable link generation
- [ ] Handle all error states
- [ ] Add loading states

---

## 🆘 Support

For issues or questions:
- Check API docs: `https://binger-backend.onrender.com/Binger/docs`
- Logs: Check browser console and network tab
- Backend issues: Contact backend team

---

**Happy Coding! 🚀**

