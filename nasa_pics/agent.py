"""
NASA Info Grab specialist agent
"""
import sys
import os
import requests
from datetime import datetime
# Add the base directory to the Python path
sys.path.append('/content/swarm/examples/magic')
from swarm import Agent
from agents.nasa_info_grab.functions import validate_date, handle_api_response, get_apod_image, get_earth_imagery, get_mars_photos
from common.functions import case_resolved, escalate_to_human, reset_memory

def create_nasa_info_grab_agent(triage_agent):
    """
    Create a NASA Info Grab specialist agent
    """
    def transfer_to_triage():
        return triage_agent
        
    # Ensure function names are valid
    validate_date.__name__ = "validate_date"
    handle_api_response.__name__ = "handle_api_response"
    get_apod_image.__name__ = "get_apod_image"
    get_earth_imagery.__name__ = "get_earth_imagery" 
    get_mars_photos.__name__ = "get_mars_photos"
    case_resolved.__name__ = "case_resolved"
    escalate_to_human.__name__ = "escalate_to_human"
    transfer_to_triage.__name__ = "transfer_to_triage"
    
    # Create a properly named reset function
    def reset_nasa_info_grab():
        return reset_memory('nasa_info_grab')
    reset_nasa_info_grab.__name__ = "reset_nasa_info_grab"
    
    return Agent(
        name="NASA Info Grab Specialist",
        instructions="""You are a NASA Info Grab specialist. Your job is to help users retrieve NASA data and images using the NASA API. You can:
1. Get the Astronomy Picture of the Day (APOD) for any date
2. Get Earth imagery for specific coordinates 
3. Get Mars rover photos from different rovers and cameras

For any request:
1. Validate inputs using validate_date when needed
2. Use the appropriate function to fetch data
3. Handle the API response appropriately
4. If successful, mark case as resolved
5. If errors occur, escalate to human
6. For non-NASA requests, transfer back to triage

Available options with demo key:
- APOD: Get astronomy picture of the day (current or past dates)
- Earth imagery: Get satellite images of Earth locations
- Mars rover photos: Get photos from Curiosity, Opportunity, and Spirit rovers

IMPORTANT: You can ONLY perform NASA API related tasks using the provided functions.
For any other requests, transfer the user back to triage using transfer_to_triage.""",
        functions=[
            validate_date,
            handle_api_response,
            get_apod_image,
            get_earth_imagery,
            get_mars_photos,
            case_resolved,
            escalate_to_human,
            transfer_to_triage,
            reset_nasa_info_grab
        ]
    )