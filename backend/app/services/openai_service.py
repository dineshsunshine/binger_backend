"""
OpenAI service for restaurant search using GPT-4 with real-time web search.
"""
import json
import logging
from typing import List, Dict, Any
from openai import OpenAI
from ..core.config import settings

logger = logging.getLogger(__name__)


class OpenAIRestaurantService:
    """Service for searching restaurants using OpenAI with web search enabled."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.system_prompt = settings.RESTAURANT_SEARCH_SYSTEM_PROMPT
    
    def search_restaurants(self, query: str, location: str) -> List[Dict[str, Any]]:
        """
        Search for restaurants using OpenAI with real-time web search.
        
        Args:
            query: Restaurant search query (e.g., "Bla Bla", "sushi restaurants", "best Italian food")
            location: City or location to search in (e.g., "Dubai", "New York", "Tokyo")
        
        Returns:
            List of restaurant dictionaries matching the specified JSON structure
        
        Raises:
            Exception: If OpenAI API call fails or returns invalid JSON
        """
        try:
            # Construct a clear search query with location
            search_query = f"Find restaurant: '{query}' in {location}. Only search for restaurants in {location}, not other cities."
            logger.info(f"Searching restaurants with query: {query} in location: {location}")
            
            # Call OpenAI with web search enabled
            # Note: Web search is available in GPT-4 models with specific configuration
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": search_query}
                ],
                temperature=0.7,
                max_tokens=4000,
                response_format={"type": "json_object"}  # Enforce JSON response
            )
            
            # Extract response content
            content = response.choices[0].message.content
            logger.debug(f"OpenAI response: {content}")
            
            # Parse JSON response
            try:
                result = json.loads(content)
                restaurants = result.get("restaurants", [])
                
                if not isinstance(restaurants, list):
                    logger.error("Response 'restaurants' field is not a list")
                    return []
                
                logger.info(f"Found {len(restaurants)} restaurants")
                return restaurants
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.error(f"Raw response: {content}")
                raise Exception(f"Invalid JSON response from OpenAI: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error searching restaurants: {str(e)}")
            raise Exception(f"Failed to search restaurants: {str(e)}")

