# Restaurant Quick Search - Frontend Integration Guide

> **Smart Two-Step Search Flow: Fast Search + Detailed View**

This guide explains how to integrate the new **Quick Search** feature for restaurants, which provides a fast, cost-effective search experience using Google Custom Search API.

---

## 🎯 Overview

The restaurant search now uses a **two-step approach** for optimal user experience and cost-efficiency:

### Step 1: Quick Search (Initial Results)
- **Fast**: Returns results in < 2 seconds
- **Lightweight**: Only essential info (name, snippet, images, URL)
- **Cost-Effective**: Uses Google Custom Search API (free tier available)
- **Purpose**: Show initial search results to user

### Step 2: Detailed Search (On Click)
- **Comprehensive**: Full restaurant details with AI intelligence
- **Paid API**: Only called when user shows interest
- **Purpose**: Get complete restaurant information for saving

---

## 📊 User Flow

```
1. User types "sushi dubai" 
   └─> Call /quick-search 
       └─> Show 5 results with images (FAST)

2. User clicks on a result 
   └─> Call /search with specific restaurant name
       └─> Get full details (OpenAI/Gemini)

3. User saves restaurant
   └─> POST /saved with complete data
```

---

## 🔌 API Endpoints

### 1. Quick Search (Initial Search)

**Endpoint:** `POST /Binger/api/restaurants/quick-search`

**Purpose:** Fast initial search for dropdown/list view

**Request:**
```typescript
interface QuickSearchRequest {
  query: string;      // "sushi", "italian pasta", "fine dining"
  location: string;   // "Dubai", "New York", "Tokyo"
}
```

**Response:**
```typescript
interface QuickSearchResponse {
  results: QuickSearchResult[];
  total: number;
}

interface QuickSearchResult {
  id: string;          // Unique identifier
  name: string;        // Restaurant name
  snippet: string;     // Brief description
  url: string | null;  // Website or Google Maps URL
  images: string[];    // Array of image URLs (0-2 images)
  location: string;    // Location/city
}
```

**Example Request:**
```bash
curl -X POST "https://your-ngrok-url/Binger/api/restaurants/quick-search" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "sushi",
    "location": "Dubai"
  }'
```

**Example Response:**
```json
{
  "results": [
    {
      "id": "a1b2c3d4e5f6g7h8",
      "name": "Zuma Dubai",
      "snippet": "Contemporary Japanese cuisine in the heart of DIFC. Award-winning sushi and robata grill.",
      "url": "https://zumarestaurant.com",
      "images": [
        "https://example.com/zuma1.jpg",
        "https://example.com/zuma2.jpg"
      ],
      "location": "Dubai"
    },
    {
      "id": "h8g7f6e5d4c3b2a1",
      "name": "Nobu Dubai",
      "snippet": "Upscale Japanese-Peruvian fusion restaurant at Atlantis The Palm.",
      "url": "https://noburestaurants.com",
      "images": [
        "https://example.com/nobu1.jpg"
      ],
      "location": "Dubai"
    }
  ],
  "total": 2
}
```

---

### 2. Detailed Search (On Click)

**Endpoint:** `POST /Binger/api/restaurants/search`

**Purpose:** Get full restaurant details after user clicks on quick search result

**Request:**
```typescript
interface RestaurantSearchRequest {
  query: string;      // Use the EXACT restaurant name from quick search
  location: string;   // Same location
  mode?: number;      // 1=OpenAI, 2=Gemini, 3=Hybrid (default: 3)
}
```

**Response:**
```typescript
interface RestaurantSearchResponse {
  restaurants: RestaurantData[];
}

interface RestaurantData {
  id: string;
  restaurant_name: string;
  description: string | null;
  google_maps_url: string | null;
  website: string | null;
  menu_url: string | null;
  city: string | null;
  country: string | null;
  phone_number: string | null;
  hours: {
    monday: string | null;
    tuesday: string | null;
    // ... other days
    timezone: string | null;
  } | null;
  cuisine: string | null;
  type: string | null;
  drinks: {
    serves_alcohol: boolean;
    special_drinks: string[];
  } | null;
  diet_type: string | null;
  social_media: {
    instagram: string | null;
    facebook: string | null;
    twitter: string | null;
    tiktok: string | null;
    tripadvisor: string | null;
  } | null;
  known_for: string[];
  images: string[];
}
```

**Example Request:**
```bash
curl -X POST "https://your-ngrok-url/Binger/api/restaurants/search" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Zuma Dubai",
    "location": "Dubai",
    "mode": 3
  }'
```

---

## 🎨 Frontend Implementation

### React/React Native Example

```typescript
import { useState } from 'react';

interface QuickSearchResult {
  id: string;
  name: string;
  snippet: string;
  url: string | null;
  images: string[];
  location: string;
}

interface RestaurantData {
  id: string;
  restaurant_name: string;
  description: string | null;
  // ... all other fields
}

function RestaurantSearch() {
  const [quickResults, setQuickResults] = useState<QuickSearchResult[]>([]);
  const [selectedRestaurant, setSelectedRestaurant] = useState<RestaurantData | null>(null);
  const [loading, setLoading] = useState(false);

  // Step 1: Quick Search (as user types)
  const handleQuickSearch = async (query: string, location: string) => {
    if (query.length < 2) return;
    
    setLoading(true);
    try {
      const response = await fetch('https://your-ngrok-url/Binger/api/restaurants/quick-search', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${yourJwtToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query, location })
      });
      
      const data = await response.json();
      setQuickResults(data.results);
    } catch (error) {
      console.error('Quick search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  // Step 2: Get Full Details (when user clicks)
  const handleResultClick = async (result: QuickSearchResult) => {
    setLoading(true);
    try {
      const response = await fetch('https://your-ngrok-url/Binger/api/restaurants/search', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${yourJwtToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          query: result.name,  // Use exact name from quick search
          location: result.location,
          mode: 3
        })
      });
      
      const data = await response.json();
      if (data.restaurants && data.restaurants.length > 0) {
        setSelectedRestaurant(data.restaurants[0]);
        // Show detail modal/screen
      }
    } catch (error) {
      console.error('Detailed search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  // Step 3: Save Restaurant
  const handleSaveRestaurant = async (restaurant: RestaurantData) => {
    try {
      const response = await fetch('https://your-ngrok-url/Binger/api/restaurants/saved', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${yourJwtToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          restaurant_data: restaurant,
          visited: false,
          personal_rating: null,
          notes: "",
          tags: []
        })
      });
      
      if (response.status === 201) {
        alert('Restaurant saved successfully!');
      }
    } catch (error) {
      console.error('Save failed:', error);
    }
  };

  return (
    <div>
      {/* Search Input */}
      <input 
        type="text"
        placeholder="Search restaurants..."
        onChange={(e) => handleQuickSearch(e.target.value, "Dubai")}
      />

      {/* Quick Results List */}
      {loading && <p>Loading...</p>}
      <ul>
        {quickResults.map(result => (
          <li key={result.id} onClick={() => handleResultClick(result)}>
            {result.images[0] && <img src={result.images[0]} alt={result.name} />}
            <h3>{result.name}</h3>
            <p>{result.snippet}</p>
          </li>
        ))}
      </ul>

      {/* Detailed View Modal */}
      {selectedRestaurant && (
        <div className="modal">
          <h2>{selectedRestaurant.restaurant_name}</h2>
          <p>{selectedRestaurant.description}</p>
          {/* Show all details */}
          <button onClick={() => handleSaveRestaurant(selectedRestaurant)}>
            Save Restaurant
          </button>
        </div>
      )}
    </div>
  );
}
```

---

## 🎯 Best Practices

### 1. **Debouncing for Quick Search**
Don't call the API on every keystroke. Use debouncing:

```typescript
import { useDebouncedCallback } from 'use-debounce';

const debouncedSearch = useDebouncedCallback(
  (query: string, location: string) => {
    handleQuickSearch(query, location);
  },
  500  // Wait 500ms after user stops typing
);
```

### 2. **Location Selection**
Always require users to select a location (city) before searching:

```typescript
<select onChange={(e) => setLocation(e.target.value)}>
  <option value="Dubai">Dubai</option>
  <option value="New York">New York</option>
  <option value="Tokyo">Tokyo</option>
</select>
```

### 3. **Loading States**
Show different loading indicators for quick vs detailed search:

```typescript
{quickLoading && <Spinner size="small" />}
{detailLoading && <Spinner size="large" text="Fetching details..." />}
```

### 4. **Image Fallbacks**
Some quick results might have no images:

```typescript
<img 
  src={result.images[0] || '/placeholder-restaurant.jpg'} 
  alt={result.name}
  onError={(e) => e.currentTarget.src = '/placeholder-restaurant.jpg'}
/>
```

### 5. **Caching**
Cache quick search results to avoid redundant API calls:

```typescript
const searchCache = new Map<string, QuickSearchResult[]>();

const getCachedResults = (query: string, location: string) => {
  const key = `${query}_${location}`;
  return searchCache.get(key);
};
```

---

## 📱 Mobile-First UI Recommendations

### Quick Search Results UI:
```
┌─────────────────────────────────────┐
│  [Search: sushi in Dubai]           │
├─────────────────────────────────────┤
│  ┌─────┐  Zuma Dubai                │
│  │ IMG │  Contemporary Japanese      │
│  └─────┘  cuisine in DIFC...        │
├─────────────────────────────────────┤
│  ┌─────┐  Nobu Dubai                │
│  │ IMG │  Upscale Japanese-Peruvian │
│  └─────┘  fusion at Atlantis...     │
├─────────────────────────────────────┤
│  ┌─────┐  Tomo Dubai                │
│  │ IMG │  Modern Japanese dining     │
│  └─────┘  with sushi bar...         │
└─────────────────────────────────────┘
```

### Detail View (After Click):
```
┌─────────────────────────────────────┐
│              Zuma Dubai              │
│  ┌─────────────────────────────────┐│
│  │        [Image Gallery]          ││
│  └─────────────────────────────────┘│
│                                      │
│  📍 DIFC, Dubai                      │
│  🍣 Japanese • Fine Dining           │
│  ⭐ Known for: Sushi, Robata Grill  │
│                                      │
│  [Full Description...]              │
│                                      │
│  📞 +971 4 425 5660                  │
│  🌐 zumarestaurant.com               │
│  🗺️  View on Google Maps             │
│                                      │
│  Hours: Mon-Sun 12:00 PM - 12:00 AM │
│                                      │
│  [Save to My List] [Share]          │
└─────────────────────────────────────┘
```

---

## ⚡ Performance Tips

1. **Quick Search is Fast**: < 2 seconds response time
2. **Detailed Search is Slower**: 3-8 seconds (uses AI)
3. **Show Quick Results Immediately**: Don't wait for full details
4. **Progressive Loading**: Show images as they load
5. **Limit Results**: Quick search returns max 5 results

---

## 💰 Cost Analysis

| Action | API Used | Cost | Speed |
|--------|----------|------|-------|
| Quick Search | Google Custom Search | FREE (100/day) or $5/1000 | < 2 sec |
| Detailed Search | OpenAI/Gemini | ~$0.01/search | 3-8 sec |
| Save Restaurant | Database | FREE | < 1 sec |

**Optimization:** 
- If user searches 10 times but only clicks 2 results:
  - Without quick search: 10 × $0.01 = $0.10
  - With quick search: (10 × FREE) + (2 × $0.01) = $0.02
  - **Savings: 80%**

---

## 🔒 Authentication

All endpoints require JWT authentication:

```typescript
headers: {
  'Authorization': `Bearer ${jwtToken}`,
  'Content-Type': 'application/json'
}
```

Get JWT token from the auth endpoint first (see main integration guide).

---

## 🐛 Error Handling

### Common Errors:

**1. No Results Found:**
```json
{
  "results": [],
  "total": 0
}
```
**Solution:** Show "No restaurants found. Try a different search."

**2. Rate Limit (429):**
```json
{
  "detail": "Rate limit exceeded"
}
```
**Solution:** Show "Too many searches. Please wait a moment."

**3. Invalid Location:**
```json
{
  "detail": "Location must be at least 2 characters"
}
```
**Solution:** Validate location input before sending.

---

## 📝 Complete Example Flow

### 1. User searches "sushi" in "Dubai"
```typescript
POST /quick-search
{
  "query": "sushi",
  "location": "Dubai"
}

// Response: 5 results with images (FAST - 1 second)
```

### 2. User clicks on "Zuma Dubai"
```typescript
POST /search
{
  "query": "Zuma Dubai",
  "location": "Dubai",
  "mode": 3
}

// Response: Full restaurant details (3-5 seconds)
```

### 3. User saves restaurant
```typescript
POST /saved
{
  "restaurant_data": { /* full data from step 2 */ },
  "visited": false,
  "personal_rating": null,
  "notes": "",
  "tags": []
}

// Response: 201 Created
```

---

## 🎉 Summary

✅ **Use `/quick-search`** for initial search results (fast, free)  
✅ **Use `/search`** when user clicks (detailed, paid)  
✅ **Show images** from quick search immediately  
✅ **Cache results** to reduce API calls  
✅ **Debounce input** to avoid excessive searches  
✅ **Handle errors gracefully** with user-friendly messages  

---

## 📞 Support

If you have questions or need help:
1. Check the API documentation at `/Binger/docs`
2. Test endpoints using Swagger UI
3. Review error logs for debugging

---

**Happy Coding! 🚀**

