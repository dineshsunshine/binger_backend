import json
import logging
from typing import List, Dict, Any
import google.generativeai as genai
from ..core.config import settings

logger = logging.getLogger(__name__)


class GeminiRestaurantService:
    """
    Service for searching restaurants using Google Gemini Flash 2.5.
    
    Note: This uses the standard Gemini API (with API key), which does not support 
    real-time Google Search grounding. For real-time web search, Vertex AI would be required.
    Gemini will use its training data to provide restaurant suggestions.
    """
    
    def __init__(self):
        """Initialize Gemini client with API key."""
        genai.configure(api_key=settings.GEMINI_API_KEY)
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
        Search for restaurants using Gemini Flash 2.5.
        
        Note: Uses Gemini's training data, not real-time web search (which requires Vertex AI).
        
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
            
            # Construct search prompt
            search_prompt = f"""
You are a restaurant search assistant. Find restaurants matching the following criteria using your knowledge:

Restaurant Query: "{query}"
Location: {location}

**IMPORTANT INSTRUCTIONS:**
1. Find restaurants in {location} that match the query "{query}"
2. Return up to {limit} real restaurants that exist (or are known to have existed) in {location}
3. For each restaurant, provide:
   - Accurate restaurant details based on your knowledge
   - Contact information if known
   - Operating hours if known
   - Image URLs (use publicly known URLs, or leave empty [] if you don't know real URLs)
   
**CRITICAL - IMAGE URLS:**
- Only include image URLs if you know real, publicly accessible URLs
- Do NOT create fake or placeholder URLs
- It's okay to return empty array [] if you don't know real image URLs
- Prefer official website URLs or well-known image hosting services

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
            
            # Call Gemini to generate restaurant suggestions
            # Note: Without Vertex AI, we don't have real-time web search
            # Gemini will use its training data to provide suggestions
            response = self.model.generate_content(search_prompt)
            
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

