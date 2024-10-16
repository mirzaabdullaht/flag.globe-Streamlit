import streamlit as st
import requests
import re

# Helper functions to get country info and Wikipedia articles
def get_country_info(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        country_data = response.json()[0]
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

# Placeholder message for quiz
def show_quiz_placeholder():
    st.write("Quiz feature is not yet implemented.")

# Placeholder message for cultural insights
def show_cultural_insights_placeholder():
    st.write("Cultural Insights feature is not yet implemented.")

# Sidebar: Theme Toggle (Light/Dark Mode)
st.sidebar.title("Theme Settings")
theme_mode = st.sidebar.radio("Select Mode", ["Light Mode", "Dark Mode"])

# Apply dark or light mode based on selection
if theme_mode == "Dark Mode":
    st.markdown(
        """
        <style>
            body {
                background-color: #333333;
                color: white;
            }
        </style>
        """, unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
            body {
                background-color: white;
                color: black;
            }
        </style>
        """, unsafe_allow_html=True
    )

# Main UI elements
st.title("FlagGlobe - Learn about Countries")
st.write("Explore information about countries around the world!")

# Dropdown for selecting an action
action = st.selectbox("Select an action", ["", "Get Country Info", "Compare Two Countries", "Take a Quiz", "Cultural Insights"])

# Get Country Info section
if action == "Get Country Info":
    country = st.text_input("Enter Country Name:")
    if st.button("Get Info"):
        if country:
            country_info = get_country_info(country)
            if 'error' in country_info:
                st.error(country_info['error'])
            else:
                st.image(country_info['flag'], caption=f"Flag of {country_info['name']}")
                st.write(f"**Country Name:** {country_info['name']}")
                st.write(f"**Capital:** {country_info['capital']}")
                st.write(f"**Population:** {country_info['population']}")
                st.write(f"**Region:** {country_info['region']}")
                st.write(f"**Languages:** {country_info['languages']}")
        else:
            st.warning("Please enter a country name.")

# Compare Two Countries section
elif action == "Compare Two Countries":
    country1 = st.text_input("Enter First Country Name:")
    country2 = st.text_input("Enter Second Country Name:")
    if st.button("Compare"):
        if country1 and country2:
            country_info_1 = get_country_info(country1)
            country_info_2 = get_country_info(country2)
            if 'error' in country_info_1:
                st.error(country_info_1['error'])
            elif 'error' in country_info_2:
                st.error(country_info_2['error'])
            else:
                col1, col2 = st.columns(2)

                with col1:
                    st.image(country_info_1['flag'], caption=f"Flag of {country_info_1['name']}")
                    st.write(f"**Capital:** {country_info_1['capital']}")
                    st.write(f"**Population:** {country_info_1['population']}")
                    st.write(f"**Region:** {country_info_1['region']}")
                    st.write(f"**Languages:** {country_info_1['languages']}")

                with col2:
                    st.image(country_info_2['flag'], caption=f"Flag of {country_info_2['name']}")
                    st.write(f"**Capital:** {country_info_2['capital']}")
                    st.write(f"**Population:** {country_info_2['population']}")
                    st.write(f"**Region:** {country_info_2['region']}")
                    st.write(f"**Languages:** {country_info_2['languages']}")
        else:
            st.warning("Please enter both country names.")

# Quiz section (Placeholder)
elif action == "Take a Quiz":
    show_quiz_placeholder()

# Cultural Insights section (Placeholder)
elif action == "Cultural Insights":
    show_cultural_insights_placeholder()


