"""
Application configuration using environment variables.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Binger API"
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    
    # Database
    IS_PRODUCTION: bool = False
    DATABASE_URL: Optional[str] = None
    
    # Authentication
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_HOURS: int = 24  # 24 hours
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 7 days
    
    # CORS
    CORS_ORIGINS: str = "*"  # Comma-separated origins or "*" for all
    
    # OpenAI (for restaurant search)
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o"  # or gpt-4o-mini for faster/cheaper responses
    
    # Google Gemini (for restaurant search with internet search)
    GEMINI_API_KEY: str
    
    # Google Custom Search (for restaurant images)
    GOOGLE_CUSTOM_SEARCH_API_KEY: str
    GOOGLE_CUSTOM_SEARCH_ENGINE_ID: str
    
    RESTAURANT_SEARCH_SYSTEM_PROMPT: str = """You are a restaurant information expert with real-time web search capabilities.

When given a restaurant search query and a location, use web search to find accurate, up-to-date information for restaurants ONLY in the specified location. Do NOT return restaurants from other cities or countries.

Return ONLY valid JSON (no markdown, no explanations, no code blocks).

Return an array of restaurants (up to 5 matches) in this exact structure:
{
  "restaurants": [
    {
      "id": "unique_identifier",
      "restaurant_name": "Full Restaurant Name",
      "description": "Detailed description",
      "google_maps_url": "https://www.google.com/maps/search/?api=1&query=...",
      "website": "https://...",
      "menu_url": "https://... or null",
      "city": "City Name",
      "country": "Country Name",
      "phone_number": "+XXX ... or null",
      "hours": {
        "monday": "HH:MM am/pm - HH:MM am/pm or Closed",
        "tuesday": "...",
        "wednesday": "...",
        "thursday": "...",
        "friday": "...",
        "saturday": "...",
        "sunday": "...",
        "timezone": "Timezone (e.g., Asia/Dubai)"
      },
      "cuisine": "Cuisine type(s)",
      "type": "Restaurant type (e.g., Fine Dining, Casual, Fast Food, etc.)",
      "drinks": {
        "serves_alcohol": true/false,
        "special_drinks": ["Specialty drink 1", "Specialty drink 2"]
      },
      "diet_type": "mixed/vegetarian/vegan/gluten-free/etc.",
      "social_media": {
        "instagram": "handle or null",
        "facebook": "url or null",
        "twitter": "handle or null",
        "tiktok": "handle or null",
        "tripadvisor": "url or null"
      },
      "known_for": ["Highlight 1", "Highlight 2", "Highlight 3"],
      "images": ["real_image_url_1", "real_image_url_2"]
    }
  ]
}

**CRITICAL INSTRUCTIONS FOR IMAGES:**
- You MUST find and return REAL, publicly accessible image URLs of the actual restaurant
- Search for images from: restaurant's official website, Google Maps photos, Instagram, food blogs, TripAdvisor, Zomato, etc.
- Return direct image URLs (ending in .jpg, .jpeg, .png, .webp) that show the restaurant, food, or interior
- If you cannot find real image URLs after searching, return an empty array [] 
- NEVER create fake/placeholder URLs like "https://restaurantname.com/images/gallery1.jpg"
- NEVER use example or dummy URLs
- Prefer high-quality photos of food, ambiance, or the restaurant exterior/interior

If no restaurants found, return: {"restaurants": []}
"""
    
    # ngrok (local development)
    NGROK_AUTH_TOKEN: Optional[str] = None
    NGROK_DOMAIN: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def database_url(self) -> str:
        """Get database URL based on environment."""
        if self.IS_PRODUCTION and self.DATABASE_URL:
            return self.DATABASE_URL
        return "sqlite:///./database.db"


settings = Settings()

