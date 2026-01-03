import googlemaps
from datetime import datetime
import json
from typing import List, Dict

class HolidayPlanner:
    def __init__(self, api_key: str):
        self.gmaps = googlemaps.Client(key=api_key)
        
    def get_city_input(self) -> str:
        """Get the desired city from user input"""
        city = input("Please enter the city you would like to visit: ")
        return city
    
    def search_places_by_category(self, city: str, category: str) -> List[Dict]:
        """Search places in the specified city by category"""
        places_result = self.gmaps.places(
            query=f"{category} in {city}",
            type=category.lower().replace(" ", "_")
        )
        
        return places_result.get('results', [])[:5]  # Return top 5 results
    
    def optimize_route(self, places: List[Dict]) -> List[Dict]:
        """Optimize the route between multiple destinations"""
        if not places:
            return []
            
        waypoints = [(place['geometry']['location']['lat'], 
                      place['geometry']['location']['lng']) 
                     for place in places]
        
        # Use Google Maps Directions API to optimize the route
        result = self.gmaps.directions(
            origin=waypoints[0],
            destination=waypoints[-1],
            waypoints=waypoints[1:-1],
            optimize_waypoints=True,
            mode="driving",
            departure_time=datetime.now()
        )
        
        return result

    def create_itinerary(self, city: str):
        """Create an optimized itinerary for the city"""
        categories = {
            "Historical Sights": "tourist_attraction",
            "Restaurants": "restaurant",
            "Local Markets": "market"
        }
        
        print(f"\nCreating itinerary for {city}...")
        all_places = {}
        
        for category_name, category_type in categories.items():
            print(f"\nSearching for {category_name}...")
            places = self.search_places_by_category(city, category_type)
            all_places[category_name] = places
            
            print(f"Top {len(places)} {category_name}:")
            for place in places:
                print(f"- {place['name']}")
                print(f"  Address: {place['formatted_address']}")
                print(f"  Rating: {place.get('rating', 'N/A')}/5.0")
        
        # Create optimized route
        all_destinations = []
        for places in all_places.values():
            all_destinations.extend(places)
            
        optimized_route = self.optimize_route(all_destinations)
        
        return all_places, optimized_route

def main():
    # Replace with your Google Maps API key
    API_KEY = "YOUR_API_KEY_HERE"
    
    planner = HolidayPlanner(API_KEY)
    
    # Get city input
    city = planner.get_city_input()
    
    # Create itinerary
    places, route = planner.create_itinerary(city)
    
    # Save results to a JSON file
    with open('itinerary.json', 'w') as f:
        json.dump({
            'city': city,
            'places': places,
            'route': route
        }, f, indent=4)
    
    print("\nItinerary has been created and saved to 'itinerary.json'")
    print("You can view the route by opening the JSON file in a Google Maps viewer")

if __name__ == "__main__":
    main()