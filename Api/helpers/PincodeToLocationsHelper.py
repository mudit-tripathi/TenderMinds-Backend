import requests

async def get_locations_by_pincode(pincode,location):
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
            # Return an error message if the request was not successful
            return location
    except Exception as e:
        # Handle any errors that occur during the request or processing
        return f"An error occurred: {str(e)}"

