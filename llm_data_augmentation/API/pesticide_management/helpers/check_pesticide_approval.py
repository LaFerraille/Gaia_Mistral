import requests

def check_pesticide_approval(pesticide_name):
    """
    Checks if the specified pesticide is approved using the EU Pesticides Database API.

    Args:
    pesticide_name (str): The name of the pesticide to check.

    Returns:
    str: Approval status of the pesticide.
    """
    # Dynamically build the API URL with the pesticide_name variable
    api_url = f"https://api.datalake.sante.service.ec.europa.eu/sante/pesticides/active_substances?skip=0&take=100&substance_name={pesticide_name}&api-version=v1.0"
    
    headers = {
        'Cache-Control': 'no-cache',
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        print(f'response {response}')
        response.raise_for_status()  # Raises an HTTPError if the response is not 200
        data = response.json()
        
        if not data:
            return "No data found for the specified pesticide."
        
        # Assuming the first result is the most relevant
        first_result = data[0] if data else {}
        substance_status = first_result.get('substance_status', 'Unknown')
        return f"Pesticide '{pesticide_name}' status: {substance_status}"

    except requests.RequestException as e:
        return f"Error fetching pesticide approval status: {e}"