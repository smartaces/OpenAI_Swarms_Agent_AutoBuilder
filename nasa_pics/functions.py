"""
Functions for the nasa_info_grab agent
"""
import sys
import os
import requests
from datetime import datetime, date
import json
# Functions:
# - get_apod_image
# - get_earth_imagery
# - get_mars_photos
# - validate_date
# - handle_api_response
def validate_date(date_str):
    """
    Validate date string format YYYY-MM-DD
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
def handle_api_response(response):
    """
    Handle API response and errors
    """
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        return {"error": "API rate limit exceeded. Please try again later."}
    else:
        return {"error": f"API request failed with status code {response.status_code}"}
def get_apod_image(date_str=None, count=None):
    """
    Get Astronomy Picture of the Day
    """
    base_url = 'https://api.nasa.gov/planetary/apod'
    params = {'api_key': 'DEMO_KEY'}
    if date_str:
        if not validate_date(date_str):
            return {"error": "Invalid date format. Use YYYY-MM-DD"}
        params['date'] = date_str
    if count:
        try:
            count = int(count)
            params['count'] = count
        except ValueError:
            return {"error": "Count must be an integer"}
    try:
        response = requests.get(base_url, params=params)
        return handle_api_response(response)
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
def get_earth_imagery(lat, lon, date_str=None):
    """
    Get satellite imagery of Earth location
    """
    base_url = 'https://api.nasa.gov/planetary/earth/imagery'
    params = {
        'api_key': 'DEMO_KEY',
        'lat': lat,
        'lon': lon
    }
    if date_str:
        if not validate_date(date_str):
            return {"error": "Invalid date format. Use YYYY-MM-DD"}
        params['date'] = date_str
    try:
        response = requests.get(base_url, params=params)
        return handle_api_response(response)
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
def get_mars_photos(sol=None, earth_date=None, camera=None):
    """
    Get Mars Rover photos
    """
    base_url = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
    params = {'api_key': 'DEMO_KEY'}
    if sol is not None:
        try:
            params['sol'] = int(sol)
        except ValueError:
            return {"error": "Sol must be an integer"}
    if earth_date:
        if not validate_date(earth_date):
            return {"error": "Invalid date format. Use YYYY-MM-DD"}
        params['earth_date'] = earth_date
    if camera:
        params['camera'] = camera
    try:
        response = requests.get(base_url, params=params)
        return handle_api_response(response)
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}