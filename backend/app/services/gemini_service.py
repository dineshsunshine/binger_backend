import json
import logging
from typing import List, Dict, Any
import google.generativeai as genai
from ..core.config import settings

logger = logging.getLogger(__name__)


class GeminiRestaurantService:
    """Service for searching restaurants using Google Gemini Flash 2.5 with internet search (grounding)."""
    
    def __init__(self):
        """Initialize Gemini client with API key."""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Using Gemini 2.0 Flash which has built-in grounding capabilities
        # No need to explicitly configure tools in the model initialization
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
        )
    
    def search_restaurants(self, query: str, location: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for restaurants using Gemini Flash 2.5 with internet search.
        
        Args:
            query: Restaurant name or search query
            location: City or location to search in
            limit: Maximum number of results to return (default: 5)
        
        Returns:
            List of restaurant dictionaries matching the specified JSON structure
        
        Raises:
            Exception: If Gemini API call fails or returns invalid JSON
        """
        try:
            logger.info(f"Searching with Gemini: '{query}' in {location}")
            
            # Construct search prompt with grounding instruction
            search_prompt = f"""
You are a restaurant search assistant with real-time internet access. Search the web for restaurants matching the following criteria:

Restaurant Query: "{query}"
Location: {location}

**IMPORTANT INSTRUCTIONS:**
1. Use real-time web search to find ONLY restaurants in {location}
2. Return ONLY restaurants that actually exist in {location}
3. Find up to {limit} restaurants that match the query
4. For each restaurant, find:
   - Real, publicly accessible image URLs (from Google Maps, official websites, Instagram, food blogs)
   - Accurate contact information and details
   - Operating hours if available
   
**CRITICAL - IMAGE URLS:**
- You MUST find REAL image URLs that are publicly accessible
- Look for images from: Google Maps photos, restaurant websites, Instagram, food blogs, review sites
- Return direct image URLs (ending in .jpg, .jpeg, .png, .webp)
- If you cannot find real images, return empty array []
- NEVER create fake or placeholder URLs

Return the results in this exact JSON structure:
{{
  "restaurants": [
    {{
      "id": "unique_identifier_based_on_restaurant_name_and_city",
      "restaurant_name": "Full Restaurant Name",
      "description": "Detailed description of the restaurant",
      "google_maps_url": "https://www.google.com/maps/search/?api=1&query=restaurant+name+city",
      "website": "https://... or null",
      "menu_url": "https://... or null",
      "city": "{location}",
      "country": "Country name",
      "phone_number": "+XXX... or null",
      "hours": {{
        "monday": "HH:MM am/pm - HH:MM am/pm or Closed",
        "tuesday": "...",
        "wednesday": "...",
        "thursday": "...",
        "friday": "...",
        "saturday": "...",
        "sunday": "...",
        "timezone": "Timezone (e.g., Asia/Dubai)"
      }},
      "cuisine": "Cuisine type(s)",
      "type": "Restaurant type (e.g., Fine Dining, Casual, etc.)",
      "drinks": {{
        "serves_alcohol": true/false,
        "special_drinks": ["Drink 1", "Drink 2"]
      }},
      "diet_type": "mixed/vegetarian/vegan/etc.",
      "social_media": {{
        "instagram": "handle or null",
        "facebook": "url or null",
        "twitter": "handle or null",
        "tiktok": "handle or null",
        "tripadvisor": "url or null"
      }},
      "known_for": ["Highlight 1", "Highlight 2", "Highlight 3"],
      "images": ["real_image_url_1", "real_image_url_2"]
    }}
  ]
}}

If no restaurants found, return: {{"restaurants": []}}

Search now and return only valid JSON.
"""
            
            # Call Gemini with Google Search grounding (internet search)
            # Gemini 2.0 Flash supports grounding via google_search_retrieval tool
            # Configure the tool with dynamic retrieval mode for real-time search
            from google.generativeai.types import Tool, GoogleSearchRetrieval
            
            google_search_tool = Tool(google_search_retrieval=GoogleSearchRetrieval())
            
            response = self.model.generate_content(
                search_prompt,
                tools=[google_search_tool]  # Enable real-time Google Search
            )
            
            # Extract response text
            response_text = response.text.strip()
            logger.debug(f"Gemini response: {response_text[:500]}...")
            
            # Parse JSON response
            try:
                # Remove markdown code blocks if present
                if response_text.startswith("```json"):
                    response_text = response_text.split("```json")[1].split("```")[0].strip()
                elif response_text.startswith("```"):
                    response_text = response_text.split("```")[1].split("```")[0].strip()
                
                result = json.loads(response_text)
                restaurants = result.get("restaurants", [])
                
                if not isinstance(restaurants, list):
                    logger.error("Response 'restaurants' field is not a list")
                    return []
                
                logger.info(f"Found {len(restaurants)} restaurants via Gemini")
                return restaurants[:limit]  # Ensure we don't exceed limit
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.error(f"Raw response: {response_text}")
                raise Exception(f"Invalid JSON response from Gemini: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error searching restaurants with Gemini: {str(e)}")
            raise Exception(f"Failed to search restaurants with Gemini: {str(e)}")

