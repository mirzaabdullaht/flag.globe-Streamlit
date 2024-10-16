import streamlit as st
import requests
import re

# Fetch country information from REST Countries API
def get_country_info(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        country_data = response.json()[0]
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

    return {
        'name': country_data['name']['common'],
        'capital': country_data.get('capital', ['No capital'])[0],
        'population': country_data.get('population', 'N/A'),
        'area': country_data.get('area', 'N/A'),
        'region': country_data.get('region', 'N/A'),
        'flag': country_data['flags']['png'],
        'languages': ', '.join(country_data['languages'].values()),
        'subregion': country_data.get('subregion', 'N/A')
    }

# Fetch Wikipedia info related to the country
def get_wikipedia_info(country_name):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'search',
        'srsearch': country_name,
        'utf8': '',
        'formatversion': '2'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        search_results = data.get('query', {}).get('search', [])
        articles = [{
            'title': result['title'],
            'snippet': re.sub('<.*?>', '', result['snippet']),
            'url': f"https://en.wikipedia.org/wiki/{result['title'].replace(' ', '_')}"
        } for result in search_results]
        return articles
    except requests.exceptions.RequestException as e:
        return []

# Streamlit App Layout and Functionality
st.title('FlagGlobe - Country Information')
st.markdown("""
Welcome to **FlagGlobe**! Learn about different countries by simply selecting an option.
""")

# Sidebar options for actions
st.sidebar.title("Choose Action")
action = st.sidebar.selectbox("Select Action", ["Get Country Info", "Compare Two Countries", "Cultural Insights", "Quiz"])

if action == "Get Country Info":
    country = st.text_input("Enter Country Name")
    if st.button("Get Info"):
        if country:
            country_info = get_country_info(country)
            if 'error' in country_info:
                st.error(country_info['error'])
            else:
                st.image(country_info['flag'], width=100)
                st.write(f"**Country:** {country_info['name']}")
                st.write(f"**Capital:** {country_info['capital']}")
                st.write(f"**Population:** {country_info['population']}")
                st.write(f"**Region:** {country_info['region']}")
                st.write(f"**Subregion:** {country_info['subregion']}")
                st.write(f"**Languages:** {country_info['languages']}")

                # Display related Wikipedia articles
                st.write("### Wikipedia Articles")
                wikipedia_info = get_wikipedia_info(country_info['name'])
                for article in wikipedia_info:
                    st.write(f"[{article['title']}]({article['url']}) - {article['snippet']}")
        else:
            st.warning("Please enter a country name.")

elif action == "Compare Two Countries":
    country1 = st.text_input("Enter First Country Name")
    country2 = st.text_input("Enter Second Country Name")
    if st.button("Compare"):
        if country1 and country2:
            country_info_1 = get_country_info(country1)
            country_info_2 = get_country_info(country2)
            
            if 'error' in country_info_1 or 'error' in country_info_2:
                st.error(f"Error fetching info: {country_info_1.get('error', '')} {country_info_2.get('error', '')}")
            else:
                # Display comparison side by side
                col1, col2 = st.columns(2)
                
                with col1:
                    st.image(country_info_1['flag'], width=100)
                    st.write(f"**Country:** {country_info_1['name']}")
                    st.write(f"**Capital:** {country_info_1['capital']}")
                    st.write(f"**Population:** {country_info_1['population']}")
                    st.write(f"**Region:** {country_info_1['region']}")
                    st.write(f"**Languages:** {country_info_1['languages']}")
                    
                with col2:
                    st.image(country_info_2['flag'], width=100)
                    st.write(f"**Country:** {country_info_2['name']}")
                    st.write(f"**Capital:** {country_info_2['capital']}")
                    st.write(f"**Population:** {country_info_2['population']}")
                    st.write(f"**Region:** {country_info_2['region']}")
                    st.write(f"**Languages:** {country_info_2['languages']}")

        else:
            st.warning("Please enter both country names.")

elif action == "Cultural Insights":
    st.write("Cultural Insights feature is not yet implemented.")

elif action == "Quiz":
    st.write("Quiz feature is not yet implemented.")
