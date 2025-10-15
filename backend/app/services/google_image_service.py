"""
Google Custom Search API service for fetching restaurant images and quick search.
"""
import logging
import requests
import hashlib
from typing import List, Dict, Any
from ..core.config import settings

logger = logging.getLogger(__name__)


class GoogleImageService:
    """Service for fetching restaurant images using Google Custom Search API."""
    
    def __init__(self):
        """Initialize Google Custom Search client."""
        self.api_key = settings.GOOGLE_CUSTOM_SEARCH_API_KEY
        self.search_engine_id = settings.GOOGLE_CUSTOM_SEARCH_ENGINE_ID
        self.base_url = "https://www.googleapis.com/customsearch/v1"
    
    def fetch_restaurant_images(self, restaurant_name: str, location: str, num_images: int = 3) -> List[str]:
        """
        Fetch restaurant images using Google Custom Search API.
        
        Args:
            restaurant_name: Name of the restaurant
            location: City/location of the restaurant
            num_images: Number of images to fetch (default: 3, max: 10)
        
        Returns:
            List of image URLs
        """
        try:
            # Construct search query
            query = f"{restaurant_name} {location} restaurant food"
            
            # API parameters
            params = {
                "key": self.api_key,
                "cx": self.search_engine_id,
                "searchType": "image",
                "q": query,
                "num": min(num_images, 10),  # Google Custom Search max is 10
                "safe": "active"  # Filter explicit content
            }
            
            logger.info(f"Fetching images for: {query}")
            
            # Make API request
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract image URLs
            images = []
            if "items" in data:
                for item in data["items"]:
                    if "link" in item:
                        images.append(item["link"])
            
            logger.info(f"Found {len(images)} images for {restaurant_name}")
            return images[:num_images]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching images from Google Custom Search: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in Google Image Service: {str(e)}")
            return []
    
    def fetch_images_for_restaurants(self, restaurants: List[dict], force_refetch: bool = False) -> List[dict]:
        """
        Fetch images for a list of restaurants and update their image fields.
        
        Args:
            restaurants: List of restaurant dictionaries
            force_refetch: If True, always fetch fresh images from Google (ignore existing images)
                          This is used for detailed search to ensure real images.
        
        Returns:
            Updated list of restaurants with images
        """
        for restaurant in restaurants:
            try:
                # If force_refetch is True, skip validation and always fetch from Google
                should_fetch = force_refetch
                
                # If not forcing refetch, check if we can reuse existing images
                if not force_refetch:
                    existing_images = restaurant.get("images", [])
                    if existing_images and len(existing_images) > 0:
                        # Filter out placeholder or invalid URLs
                        valid_images = [
                            img for img in existing_images
                            if img 
                            and not img.endswith("placeholder.jpg")
                            and "example.com" not in img.lower()
                            and "/gallery" not in img.lower()  # AI often creates fake gallery URLs
                            and "/images/" not in img.lower()  # AI creates generic /images/ paths
                        ]
                        if valid_images:
                            logger.debug(f"Reusing {len(valid_images)} existing valid images")
                            restaurant["images"] = valid_images
                            continue  # Skip fetching, use existing
                    # If no valid images, we need to fetch
                    should_fetch = True
                
                # Fetch new images from Google Custom Search
                if should_fetch:
                    restaurant_name = restaurant.get("restaurant_name", "")
                    location = restaurant.get("city", "")
                    
                    if restaurant_name and location:
                        logger.info(f"Fetching fresh images for: {restaurant_name}, {location}")
                        images = self.fetch_restaurant_images(restaurant_name, location, num_images=3)
                        restaurant["images"] = images
                    else:
                        logger.warning(f"Missing name or location, cannot fetch images")
                        restaurant["images"] = []
                    
            except Exception as e:
                logger.error(f"Error processing images for restaurant: {str(e)}")
                restaurant["images"] = []
        
        return restaurants
    
    def quick_search_restaurants(self, query: str, location: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Fast restaurant search using Google Custom Search API.
        Returns lightweight results with name, snippet, URL, and images.
        
        Args:
            query: Restaurant name or search query
            location: City or location to search in
            num_results: Number of results to return (default: 5, max: 10)
        
        Returns:
            List of quick search results with basic info and images
        """
        try:
            # Construct search query (contextual to restaurants)
            search_query = f"{query} restaurant {location}"
            
            # API parameters for web search (NOT image search)
            params = {
                "key": self.api_key,
                "cx": self.search_engine_id,
                "q": search_query,
                "num": min(num_results, 10),  # Google Custom Search max is 10
                "safe": "active"
            }
            
            logger.info(f"Quick searching restaurants: {search_query}")
            
            # Make API request
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract results
            results = []
            if "items" in data:
                for item in data["items"]:
                    # Generate unique ID from title and location
                    name = item.get("title", "Unknown Restaurant")
                    # Clean name (remove common suffixes)
                    name = name.split(" - ")[0].strip()
                    name = name.split(" | ")[0].strip()
                    
                    # Generate ID
                    unique_string = f"{name}_{location}".lower().replace(" ", "_")
                    result_id = hashlib.md5(unique_string.encode()).hexdigest()[:16]
                    
                    # Extract snippet
                    snippet = item.get("snippet", "")
                    
                    # Extract URL
                    url = item.get("link", "")
                    
                    # Fetch images for this restaurant
                    images = self.fetch_restaurant_images(name, location, num_images=2)
                    
                    results.append({
                        "id": result_id,
                        "name": name,
                        "snippet": snippet,
                        "url": url,
                        "images": images,
                        "location": location
                    })
            
            logger.info(f"Found {len(results)} quick search results")
            return results[:num_results]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error in quick search from Google Custom Search: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in quick search: {str(e)}")
            return []

