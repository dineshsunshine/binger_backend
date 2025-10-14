# 🔍 Multi-Mode Restaurant Search - Implementation Guide

## Overview

The Binger backend now supports **three different search modes** for restaurant discovery:

1. **Mode 1: OpenAI Only** - Intelligent AI search (may have placeholder images)
2. **Mode 2: Foursquare Only** - Real restaurant data with high-quality photos
3. **Mode 3: Hybrid (RECOMMENDED)** - Best of both worlds: AI intelligence + real photos

---

## ✅ What Was Implemented

### 1. **Foursquare Places API Integration**
- Created `FoursquareRestaurantService` class
- Integrated Foursquare Places API v3
- Transforms Foursquare data to match our restaurant schema
- Extracts real, high-quality restaurant photos

### 2. **Multi-Mode Search Endpoint**
- Updated `/restaurants/search` endpoint
- Added `mode` parameter (1, 2, or 3)
- Default: Mode 3 (Hybrid)
- Intelligent result merging for hybrid mode

### 3. **Hybrid Search Logic**
- Queries both OpenAI and Foursquare simultaneously
- Prioritizes Foursquare results (real photos)
- Supplements with OpenAI results for unique restaurants
- Removes duplicates using fuzzy name/location matching
- Returns top 5 combined results

### 4. **Configuration & Environment**
- Added `FOURSQUARE_API_KEY` to config
- Updated local `.env` file
- Updated `render.yaml` for production deployment
- Added `requests` library to requirements.txt

### 5. **Documentation**
- Updated `RESTAURANT_INTEGRATION.md` with mode comparison
- Added this guide for implementation reference

---

## 📊 Mode Comparison

| Feature | Mode 1 (OpenAI) | Mode 2 (Foursquare) | Mode 3 (Hybrid) |
|---------|-----------------|---------------------|-----------------|
| **Real Photos** | ❌ May be placeholders | ✅ High-quality | ✅ Foursquare photos prioritized |
| **Search Intelligence** | ✅ Very smart AI | ⚠️ Basic keyword | ✅ AI + Real data |
| **Speed** | ⚠️ 3-8 seconds | ✅ 1-2 seconds | ⚠️ 4-10 seconds |
| **Data Accuracy** | ✅ Good | ✅ Excellent | ✅ Best |
| **Unique Restaurants** | ✅ Finds obscure places | ⚠️ Foursquare DB only | ✅ Comprehensive |
| **Free Tier Limit** | ~100 requests/day | 50,000 requests/day | Combined |
| **Best For** | Specific restaurant search | Quick browsing | Overall experience |

---

## 🔧 API Usage

### Request Format

```javascript
const response = await fetch('https://binger-backend.onrender.com/Binger/api/restaurants/search', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: "Bla Bla",        // Restaurant name or search term
    location: "Dubai",       // City to search in
    mode: 3                  // 1=OpenAI, 2=Foursquare, 3=Hybrid
  })
});

const data = await response.json();
```

### Response Format

Same restaurant schema for all modes:

```json
{
  "restaurants": [
    {
      "id": "bla_bla_jbr_dubai_abc12345",
      "restaurant_name": "Bla Bla Dubai",
      "description": "An expansive all-day social destination...",
      "google_maps_url": "https://www.google.com/maps/...",
      "website": "https://blabladubai.ae/",
      "menu_url": "https://blabladubai.ae/menus/",
      "city": "Dubai",
      "country": "United Arab Emirates",
      "phone_number": "+971 4 584 4111",
      "hours": {
        "monday": "11:00 am - 12:00 am",
        "tuesday": "11:00 am - 12:00 am",
        // ... other days
        "timezone": "Asia/Dubai"
      },
      "cuisine": "International / Fusion",
      "type": "Beach Club / Restaurant",
      "drinks": {
        "serves_alcohol": true,
        "special_drinks": ["Signature cocktails"]
      },
      "diet_type": "mixed",
      "social_media": {
        "instagram": "blabladubai",
        "facebook": "...",
        "twitter": null,
        "tiktok": null,
        "tripadvisor": "..."
      },
      "known_for": [
        "21 themed bars under one roof",
        "Beach club with infinity pools"
      ],
      "images": [
        "https://fastly.4sqi.net/img/general/500x500/...",
        "https://fastly.4sqi.net/img/general/500x500/..."
      ]
    }
  ]
}
```

---

## 🎯 Hybrid Mode Logic

### How It Works

1. **Query both services in parallel**
   - OpenAI searches using intelligent AI
   - Foursquare searches using Places API

2. **Prioritize Foursquare results**
   - Start with Foursquare restaurants (real photos)
   - These are guaranteed to have accurate data

3. **Supplement with OpenAI results**
   - Check for duplicates using fuzzy matching
   - Add unique OpenAI results if they have real images
   - Include OpenAI results if we have < 3 total results

4. **Return top 5 combined results**
   - Best of both worlds
   - Maximum variety and accuracy

### Duplicate Detection

Restaurants are considered duplicates if:
- Name similarity > 70% (word overlap)
- Same city

Example:
- "Bla Bla Dubai" and "Bla Bla" in Dubai = Duplicate ✅
- "Troy Restaurant" and "Troy" in Dubai = Duplicate ✅
- "Troy" in Dubai and "Troy" in London = Not duplicate ❌

---

## 🔑 API Keys & Configuration

### Local Development (.env)

```bash
OPENAI_API_KEY=your_openai_api_key_here
FOURSQUARE_API_KEY=your_foursquare_api_key_here
```

✅ **Already configured in your local .env file!**

### Production (Render Dashboard)

**⚠️ IMPORTANT: Add the following environment variables to your Render dashboard:**

1. Go to: https://dashboard.render.com/web/binger-backend
2. Click "Environment" tab
3. Add the following (use the same values from your local .env):
   - **Key:** `OPENAI_API_KEY`  
     **Value:** `[Your OpenAI API Key]`
   
   - **Key:** `FOURSQUARE_API_KEY`  
     **Value:** `[Your Foursquare API Key]`

4. Click "Save Changes"
5. Render will automatically redeploy

---

## 📁 Files Changed

### New Files
- `backend/app/services/foursquare_service.py` - Foursquare API integration

### Modified Files
- `backend/app/core/config.py` - Added FOURSQUARE_API_KEY
- `backend/app/schemas/restaurant.py` - Added `mode` parameter
- `backend/app/api/v1/endpoints/restaurants.py` - Multi-mode search logic
- `backend/requirements.txt` - Added `requests` library
- `backend/.env` - Added Foursquare API key
- `render.yaml` - Added OPENAI_API_KEY and FOURSQUARE_API_KEY
- `RESTAURANT_INTEGRATION.md` - Updated documentation

---

## 🚀 Deployment Status

- ✅ **Local Development:** Ready (API key added to .env)
- ✅ **Code Committed:** Pushed to GitHub
- ⚠️ **Production:** Needs manual step (add API keys to Render dashboard)

---

## 🧪 Testing Recommendations

### Test Mode 1 (OpenAI Only)
```json
{
  "query": "Bla Bla",
  "location": "Dubai",
  "mode": 1
}
```
**Expected:** Results may have placeholder image URLs

### Test Mode 2 (Foursquare Only)
```json
{
  "query": "Bla Bla",
  "location": "Dubai",
  "mode": 2
}
```
**Expected:** Real photos, faster response

### Test Mode 3 (Hybrid - Default)
```json
{
  "query": "Bla Bla",
  "location": "Dubai",
  "mode": 3
}
```
**Expected:** Best results with real photos and comprehensive coverage

---

## 💡 Recommendations for Frontend

1. **Default to Mode 3 (Hybrid)** for best user experience
2. **Show loading state** - Hybrid mode can take 4-10 seconds
3. **Implement search mode selector** (optional):
   - "Smart Search" (Mode 3 - default)
   - "Quick Search" (Mode 2)
   - "AI Search" (Mode 1)
4. **Debounce search input** - Wait 500ms after user stops typing
5. **Handle errors gracefully** - Both services can occasionally fail
6. **Cache results** - Reduce API calls for repeated searches

---

## 📊 Rate Limits

- **OpenAI:** ~100-200 requests/day (free tier)
- **Foursquare:** 50,000 requests/day (free tier) ✅ Very generous
- **Hybrid:** Uses both, so counts against both limits

---

## 🎉 Summary

The multi-mode search gives you flexibility:
- **Speed vs Intelligence:** Choose Foursquare for speed, OpenAI for intelligence
- **Real Photos:** Foursquare guarantees real restaurant photos
- **Best Results:** Hybrid mode combines strengths of both
- **Fallback Safety:** Hybrid mode works even if one service fails

**Recommended for production:** Mode 3 (Hybrid) - enabled by default! 🚀

