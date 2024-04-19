import requests
from Api.config import logging_config
logging_config.setup_logging()
import logging

# Create a logger for this module
logger = logging.getLogger(__name__)

async def get_locations_by_pincode(pincode,location):
    logger.info("Entered get_locations_by_pincode")
    url = f"http://postalpincode.in/api/pincode/{pincode}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['Status'].lower() == 'success':
            post_offices = data['PostOffice']
            Areas = [office['Name'] for office in post_offices]
            Districts = list({office['District'] for office in post_offices})
            States = list({office['State'] for office in post_offices})
            return Areas, Districts, States
        else:
            logger.error("The pincode is not found.")
            return [location],[],[]
    except Exception as e:
        # Handle any errors that occur during the request or processing
        logger.error(f"An error occurred: {str(e)}") 
        return [location],[],[]

