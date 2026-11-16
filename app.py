import streamlit as st
import requests
from datetime import date

# Page configuration
st.set_page_config(page_title="Global Football LiveScore", page_icon="🌐", layout="wide")

st.title("Global Football LiveScore - Pro")
st.markdown("Welcome! This is the central server fetching live global matches automatically.")

today_str = date.today().strftime("%Y-%m-%d")

# Sidebar configuration
st.sidebar.title("World Leagues Filter")
continent_filter = st.sidebar.selectbox("Select Region:", [
    "All Global Matches",
    "European Top Leagues",
    "English Premier League",
    "Spanish La Liga",
    "Italian Serie A",
    "German Bundesliga",
    "African & Arab Leagues",
    "Other Leagues"
])

search_query = st.sidebar.text_input("Search for team or league:", "")

st.subheader(f"Today's Global Matches - {today_str}")

@st.cache_data(ttl=60)
def fetch_global_matches():
    api_url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={today_str}"
    try:
        api_response = requests.get(api_url)
        api_data = api_response.json()
        return api_data.get("events", [])
    except:
        return []

match_list = fetch_global_matches()

if match_list:
    filtered_matches = []
    for current_match in match_list:
        home_team_name = current_match.get("strHomeTeam", "")
        away_team_name = current_match.get("strAwayTeam", "")
        league_name = current_match.get("strLeague", "")
        
        if search_query.lower() in home_team_name.lower() or search_query.lower() in away_team_name.lower() or search_query.lower()
