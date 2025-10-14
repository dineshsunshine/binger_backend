import json
import logging
from typing import List, Dict, Any, Optional
import requests
from ..core.config import settings

logger = logging.getLogger(__name__)


class FoursquareRestaurantService:
    """Service for searching restaurants using Foursquare Places API."""
    
    def __init__(self):
        """Initialize Foursquare API client."""
        self.api_key = settings.FOURSQUARE_API_KEY
        self.base_url = "https://api.foursquare.com/v3/places"
        self.headers = {
            "Authorization": self.api_key,
            "Accept": "application/json"
        }
    
    def search_restaurants(self, query: str, location: str) -> List[Dict[str, Any]]:
        """
        Search for restaurants using Foursquare Places API.
        
        Args:
            query: Restaurant search query (e.g., "Bla Bla", "sushi restaurants", "best Italian food")
            location: City or location to search in (e.g., "Dubai", "New York", "Tokyo")
        
        Returns:
            List of restaurant dictionaries matching the specified JSON structure
        
        Raises:
            Exception: If Foursquare API call fails
        """
        try:
            logger.info(f"Searching Foursquare for: '{query}' in {location}")
            
            # Foursquare search endpoint
            search_url = f"{self.base_url}/search"
            
            # Build search parameters
            params = {
                "query": query,
                "near": location,
                "categories": "13000",  # Food category ID in Foursquare
                "limit": 5,
                "fields": "name,location,tel,website,hours,rating,photos,categories,description,social_media,price,menu"
            }
            
            # Make API request
            response = requests.get(search_url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = data.get("results", [])
            
            logger.info(f"Foursquare returned {len(results)} results")
            
            # Transform Foursquare data to our restaurant schema
            restaurants = []
            for place in results:
                restaurant = self._transform_to_restaurant_schema(place, location)
                if restaurant:
                    restaurants.append(restaurant)
            
            return restaurants
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Foursquare API request failed: {str(e)}")
            raise Exception(f"Failed to search restaurants: {str(e)}")
        except Exception as e:
            logger.error(f"Error searching restaurants: {str(e)}")
            raise Exception(f"Failed to search restaurants: {str(e)}")
    
    def _transform_to_restaurant_schema(self, place: Dict[str, Any], search_location: str) -> Optional[Dict[str, Any]]:
        """Transform Foursquare place data to our restaurant schema."""
        try:
            # Extract basic info
            fsq_id = place.get("fsq_id", "")
            name = place.get("name", "Unknown Restaurant")
            
            # Location data
            location_data = place.get("location", {})
            address = location_data.get("formatted_address", "")
            city = location_data.get("locality", search_location)
            country = location_data.get("country", "")
            
            # Generate unique restaurant ID
            restaurant_id = f"{name.lower().replace(' ', '_')}_{city.lower().replace(' ', '_')}_{fsq_id[:8]}"
            
            # Description from categories or generic
            categories = place.get("categories", [])
            cuisine_types = [cat.get("name", "") for cat in categories if cat.get("name")]
            cuisine = ", ".join(cuisine_types[:3]) if cuisine_types else "Restaurant"
            
            description = place.get("description", f"{name} is a restaurant in {city} serving {cuisine}.")
            
            # Contact info
            tel = place.get("tel", None)
            website = place.get("website", None)
            
            # Hours
            hours_data = place.get("hours", {})
            hours = self._parse_hours(hours_data)
            
            # Photos
            photos = place.get("photos", [])
            image_urls = []
            for photo in photos[:2]:  # Get up to 2 photos
                prefix = photo.get("prefix", "")
                suffix = photo.get("suffix", "")
                if prefix and suffix:
                    # Construct image URL with reasonable size (500x500)
                    image_url = f"{prefix}500x500{suffix}"
                    image_urls.append(image_url)
            
            # Social media
            social_media_data = place.get("social_media", {})
            social_media = {
                "instagram": social_media_data.get("instagram", None),
                "facebook": social_media_data.get("facebook_id", None),
                "twitter": social_media_data.get("twitter", None),
                "tiktok": None,
                "tripadvisor": None
            }
            
            # Price level
            price_level = place.get("price", 2)  # Default to moderate
            
            # Rating
            rating = place.get("rating", None)
            
            # Menu URL
            menu_url = place.get("menu", None)
            
            # Google Maps URL
            lat = location_data.get("latitude")
            lng = location_data.get("longitude")
            google_maps_url = f"https://www.google.com/maps/search/?api=1&query={name.replace(' ', '+')}+{city.replace(' ', '+')}"
            if lat and lng:
                google_maps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
            
            # Known for (based on categories and rating)
            known_for = []
            if rating and rating >= 8:
                known_for.append("Highly rated by diners")
            if cuisine_types:
                known_for.append(f"Specializes in {cuisine_types[0]}")
            if len(photos) > 3:
                known_for.append("Instagram-worthy ambiance")
            if not known_for:
                known_for.append(f"Popular {cuisine} spot in {city}")
            
            # Restaurant type
            restaurant_type = "Restaurant"
            if any("fine dining" in cat.get("name", "").lower() for cat in categories):
                restaurant_type = "Fine Dining"
            elif any("casual" in cat.get("name", "").lower() for cat in categories):
                restaurant_type = "Casual Dining"
            elif any("cafe" in cat.get("name", "").lower() or "coffee" in cat.get("name", "").lower() for cat in categories):
                restaurant_type = "Café"
            elif any("bar" in cat.get("name", "").lower() for cat in categories):
                restaurant_type = "Bar & Grill"
            
            # Alcohol service (infer from categories)
            serves_alcohol = any("bar" in cat.get("name", "").lower() or "pub" in cat.get("name", "").lower() for cat in categories)
            
            # Diet type (default to mixed)
            diet_type = "mixed"
            if any("vegetarian" in cat.get("name", "").lower() for cat in categories):
                diet_type = "vegetarian"
            elif any("vegan" in cat.get("name", "").lower() for cat in categories):
                diet_type = "vegan"
            
            # Build final restaurant object
            restaurant = {
                "id": restaurant_id,
                "restaurant_name": name,
                "description": description,
                "google_maps_url": google_maps_url,
                "website": website,
                "menu_url": menu_url,
                "city": city,
                "country": country,
                "phone_number": tel,
                "hours": hours,
                "cuisine": cuisine,
                "type": restaurant_type,
                "drinks": {
                    "serves_alcohol": serves_alcohol,
                    "special_drinks": []
                },
                "diet_type": diet_type,
                "social_media": social_media,
                "known_for": known_for,
                "images": image_urls
            }
            
            return restaurant
            
        except Exception as e:
            logger.error(f"Error transforming Foursquare place data: {str(e)}")
            return None
    
    def _parse_hours(self, hours_data: Dict[str, Any]) -> Dict[str, str]:
        """Parse Foursquare hours data into our format."""
        default_hours = {
            "monday": "Hours not available",
            "tuesday": "Hours not available",
            "wednesday": "Hours not available",
            "thursday": "Hours not available",
            "friday": "Hours not available",
            "saturday": "Hours not available",
            "sunday": "Hours not available",
            "timezone": "UTC"
        }
        
        if not hours_data:
            return default_hours
        
        try:
            # Foursquare hours format: array of day objects with open/close times
            regular_hours = hours_data.get("regular", [])
            timezone = hours_data.get("timezone", "UTC")
            
            day_names = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            parsed_hours = {day: "Closed" for day in day_names}
            parsed_hours["timezone"] = timezone
            
            for day_data in regular_hours:
                day_num = day_data.get("day", 0)  # 1=Monday, 7=Sunday
                if 1 <= day_num <= 7:
                    day_name = day_names[day_num - 1]
                    open_time = day_data.get("open", "")
                    close_time = day_data.get("close", "")
                    
                    if open_time and close_time:
                        # Convert 24h format to 12h format (e.g., "0900" -> "9:00 am")
                        open_formatted = self._format_time(open_time)
                        close_formatted = self._format_time(close_time)
                        parsed_hours[day_name] = f"{open_formatted} - {close_formatted}"
            
            return parsed_hours
            
        except Exception as e:
            logger.error(f"Error parsing hours: {str(e)}")
            return default_hours
    
    def _format_time(self, time_str: str) -> str:
        """Format time from 24h format (e.g., '0900') to 12h format (e.g., '9:00 am')."""
        try:
            if len(time_str) == 4:
                hour = int(time_str[:2])
                minute = time_str[2:]
                
                am_pm = "am" if hour < 12 else "pm"
                if hour == 0:
                    hour = 12
                elif hour > 12:
                    hour -= 12
                
                return f"{hour}:{minute} {am_pm}"
            return time_str
        except:
            return time_str

