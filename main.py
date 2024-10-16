import streamlit as st
import requests
import re

# Function to fetch country information from the REST Countries API
def get_country_info(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        country_data = response.json()[0]  # Get the first country result
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

    country_info = {
        'name': country_data['name']['common'],
        'capital': country_data.get('capital', ['No capital'])[0],
        'population': country_data.get('population', 'N/A'),
        'area': country_data.get('area', 'N/A'),
        'region': country_data.get('region', 'N/A'),
        'flag': country_data['flags']['png'],
        'languages': ', '.join(country_data['languages'].values()),
        'subregion': country_data.get('subregion', 'N/A')
    }

    return country_info

# Function to fetch Wikipedia information for a country
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
        articles = []

        for result in search_results:
            title = result['title']
            snippet = result['snippet']
            clean_snippet = re.sub('<.*?>', '', snippet)
            articles.append({
                'title': title,
                'snippet': clean_snippet,
                'url': f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
            })

        return articles

    except requests.exceptions.RequestException as e:
        return str(e)

# Function to handle light/dark mode toggle
def toggle_theme():
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

    theme = st.sidebar.selectbox("Select Theme", ["light", "dark"], index=0 if st.session_state.theme == "light" else 1)
    st.session_state.theme = theme

    # Set Streamlit theme accordingly
    st.write(f"Switching to {theme} mode")
    st.markdown(
        """
        <style>
        body {
            background-color: #111 !important;
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    ) if theme == "dark" else None

# Streamlit app
def main():
    st.title("FlagGlobe - Country Information")
    
    # Light/Dark Mode Toggle
    toggle_theme()

    action = st.sidebar.selectbox("Select Action", ["Get Country Info", "Take a Quiz", "Cultural Insights"], index=0)
    
    if action == "Get Country Info":
        country = st.text_input("Enter Country Name")
        if st.button("Get Info"):
            if country:
                country_info = get_country_info(country)

                if 'error' in country_info:
                    st.error(country_info['error'])
                else:
                    st.subheader(country_info['name'])
                    st.image(country_info['flag'], width=200)
                    st.write(f"**Capital**: {country_info['capital']}")
                    st.write(f"**Population**: {country_info['population']}")
                    st.write(f"**Region**: {country_info['region']}")
                    st.write(f"**Languages**: {country_info['languages']}")

                    # Wikipedia information
                    wikipedia_info = get_wikipedia_info(country_info['name'])
                    st.write("### Wikipedia Articles:")
                    for article in wikipedia_info:
                        st.write(f"[{article['title']}]({article['url']}) - {article['snippet']}")
            else:
                st.error("Please enter a country name.")
    
    elif action == "Take a Quiz":
        st.write("Quiz feature is not yet implemented.")
    
    elif action == "Cultural Insights":
        st.write("Cultural Insights feature is not yet implemented.")

if __name__ == "__main__":
    main()
