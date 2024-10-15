import streamlit as st
import requests
import re

# Helper function to get country info from REST Countries API
def get_country_info(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        country_data = response.json()[0]  # Get the first country result

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
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

# Helper function to get country info from Wikipedia API
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
            clean_snippet = re.sub('<.*?>', '', snippet)  # Remove HTML tags
            articles.append({
                'title': title,
                'snippet': clean_snippet,
                'url': f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
            })

        return articles
    except requests.exceptions.RequestException as e:
        return str(e)

# Streamlit UI
st.title("FlagGlobe 🌍")
st.write("Enter a country name or flag emoji to get started!")

# Create a dropdown for selecting functionality
action = st.selectbox("Choose an action:", ["Get Country Info", "Compare Countries", "Take a Quiz", "Cultural Insights"])

# Get Country Info
if action == "Get Country Info":
    country_name = st.text_input("Enter a country name or flag emoji:")

    if country_name:
        country_info = get_country_info(country_name)

        if 'error' in country_info:
            st.error(f"Error: {country_info['error']}")
        else:
            st.subheader(f"Country: {country_info['name']}")
            st.image(country_info['flag'], caption=f"Flag of {country_info['name']}")
            st.write(f"**Capital**: {country_info['capital']}")
            st.write(f"**Population**: {country_info['population']}")
            st.write(f"**Region**: {country_info['region']}")
            st.write(f"**Subregion**: {country_info['subregion']}")
            st.write(f"**Languages**: {country_info['languages']}")

            # Wikipedia info
            wikipedia_info = get_wikipedia_info(country_info['name'])
            st.subheader("Wikipedia Articles:")
            for article in wikipedia_info:
                st.write(f"[{article['title']}]({article['url']})")
                st.write(article['snippet'])

# Compare Countries
elif action == "Compare Countries":
    country1 = st.text_input("Enter the first country name:")
    country2 = st.text_input("Enter the second country name:")

    if country1 and country2:
        country_info_1 = get_country_info(country1)
        country_info_2 = get_country_info(country2)

        if 'error' in country_info_1 or 'error' in country_info_2:
            st.error(f"Error in fetching country data.")
        else:
            st.subheader(f"Comparison: {country_info_1['name']} vs {country_info_2['name']}")

            # First country info
            st.write(f"**{country_info_1['name']}**")
            st.image(country_info_1['flag'], caption=f"Flag of {country_info_1['name']}")
            st.write(f"**Capital**: {country_info_1['capital']}")
            st.write(f"**Population**: {country_info_1['population']}")
            st.write(f"**Region**: {country_info_1['region']}")
            st.write(f"**Languages**: {country_info_1['languages']}")

            # Second country info
            st.write(f"**{country_info_2['name']}**")
            st.image(country_info_2['flag'], caption=f"Flag of {country_info_2['name']}")
            st.write(f"**Capital**: {country_info_2['capital']}")
            st.write(f"**Population**: {country_info_2['population']}")
            st.write(f"**Region**: {country_info_2['region']}")
            st.write(f"**Languages**: {country_info_2['languages']}")

# Quiz Section
elif action == "Take a Quiz":
    quiz_data = [
        {"question": "What is the capital of France?", "options": ["Paris", "Rome", "Berlin"], "answer": "Paris"},
        {"question": "Which country is known as the Land of the Rising Sun?", "options": ["Japan", "China", "Korea"], "answer": "Japan"},
    ]

    for question in quiz_data:
        st.write(question["question"])
        option = st.radio("Choose your answer:", question["options"], key=question["question"])
        if st.button(f"Submit {question['question']}"):
            if option == question['answer']:
                st.success("Correct!")
            else:
                st.error("Wrong answer.")

# Cultural Insights
elif action == "Cultural Insights":
    country_name = st.text_input("Enter a country name to get cultural insights:")

    if country_name:
        # Dummy data for insights
        insights = {
            'traditions': ["Traditional Dance", "Cultural Festival"],
            'foods': ["Local Dish 1", "Local Dish 2"],
            'facts': ["Interesting Fact 1", "Interesting Fact 2"]
        }
        st.subheader(f"Cultural Insights for {country_name}")
        st.write(f"**Traditions**: {', '.join(insights['traditions'])}")
        st.write(f"**Foods**: {', '.join(insights['foods'])}")
        st.write(f"**Facts**: {', '.join(insights['facts'])}")

