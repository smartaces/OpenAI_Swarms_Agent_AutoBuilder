"""
Content file for nasa_info_grab agent
"""
# Available NASA API endpoints and options
NASA_API_OPTIONS = {
    'APOD': {
        'endpoint': 'https://api.nasa.gov/planetary/apod',
        'description': 'Astronomy Picture of the Day',
        'params': {
            'date': 'YYYY-MM-DD',
            'start_date': 'YYYY-MM-DD',
            'end_date': 'YYYY-MM-DD',
            'count': 'int',
            'thumbs': 'bool'
        }
    },
    'EARTH': {
        'endpoint': 'https://api.nasa.gov/planetary/earth/imagery',
        'description': 'Satellite imagery of Earth',
        'params': {
            'lat': 'float',
            'lon': 'float',
            'date': 'YYYY-MM-DD',
            'dim': 'float'
        }
    },
    'MARS_PHOTOS': {
        'endpoint': 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos',
        'description': 'Mars Rover Photos',
        'params': {
            'sol': 'int',
            'earth_date': 'YYYY-MM-DD',
            'camera': 'string'  
        }
    }
}
# API configuration
API_CONFIG = {
    'demo_key': 'DEMO_KEY',
    'rate_limit': {
        'hourly': 30,
        'daily': 50
    }
}