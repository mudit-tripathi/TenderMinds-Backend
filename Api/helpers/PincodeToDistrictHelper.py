import requests

def get_district_by_pincode(pincode):
    url = f"http://postalpincode.in/api/pincode/{pincode}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data['Status'].lower() == 'success':
            # Extract the list of post offices
            post_offices = data['PostOffice']
            # Extract the district(s) from the post offices and remove duplicates
            districts = {office['District'] for office in post_offices}
            return list(districts)
        else:
            return "Null"
    except Exception as e:
        return f"An error occurred: {str(e)}"