import streamlit as st
import requests
import re

# Function to get country information from REST Countries API
def get_country_info(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        country_data = response.json()[0]  # Get the first country result

        # Extract relevant information
        country_info = {
            'name': country_data['name']['common'],
            'capital': country_data.get('capital', ['No capital'])[0],
            'population': country_data.get('population', 'N/A'),
            'region': country_data.get('region', 'N/A'),
            'flag': country_data['flags']['png']
        }

        return country_info

    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

# Function to get additional information from Wikipedia API
def get_wikipedia_info(country_name):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': country_name,  # Search for the country name
        'utf8': '',
        'formatversion': '2'
    }

    try:
        # Send the request to the Wikipedia API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Check for request errors

        # Parse the JSON response
        data = response.json()

        # Get the first search result's snippet
        search_results = data.get('query', {}).get('search', [])
        if search_results:
            snippet = search_results[0]['snippet']  # Get the snippet from the first search result

            # Use regex to remove any HTML tags (like <span>, <b>, etc.)
            clean_snippet = re.sub('<.*?>', '', snippet)  # Remove HTML tags

            return clean_snippet  # Return the cleaned snippet
        else:
            return "No additional information available."

    except requests.exceptions.RequestException as e:
        return str(e)

# Streamlit UI setup
st.title("FlagGlobe 🌍")
st.write("Enter a flag emoji or country name to learn more about the country!")

# User input
country_input = st.text_input("Country Name or Flag Emoji", "")

# When the user submits input
if country_input:
    # Get country info
    country_info = get_country_info(country_input)
    
    # If error occurs, show error message
    if 'error' in country_info:
        st.error(f"Error: {country_info['error']}")
    else:
        # Display the country info
        st.subheader(f"Country: {country_info['name']}")
        st.write(f"**Capital**: {country_info['capital']}")
        st.write(f"**Population**: {country_info['population']}")
        st.write(f"**Region**: {country_info['region']}")
        st.image(country_info['flag'], caption=f"Flag of {country_info['name']}")

        # Get and display Wikipedia info
        wikipedia_info = get_wikipedia_info(country_info['name'])
        st.write(f"**Wikipedia Info**: {wikipedia_info}")
