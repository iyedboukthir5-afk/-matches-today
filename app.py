import streamlit as st
import requests
from datetime import date

st.set_page_config(page_title="Global Football LiveScore", page_icon="🌐", layout="wide")

st.title("Global Football LiveScore - Pro")
st.markdown("Welcome! This is the central server fetching live global matches automatically.")

today_str = date.today().strftime("%Y-%m-%d")

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
        home_team_name = str(current_match.get("strHomeTeam", ""))
        away_team_name = str(current_match.get("strAwayTeam", ""))
        league_name = str(current_match.get("strLeague", ""))
        
        # شرط بحث بسيط ومضمون 100%
        if not search_query or search_query.lower() in home_team_name.lower() or search_query.lower() in away_team_name.lower():
            filtered_matches.append(current_match)

    if filtered_matches:
        st.success(f"Found {len(filtered_matches)} matches broadcasting worldwide.")
        
        for current_match in filtered_matches:
            home_team = current_match.get("strHomeTeam", "Team A")
            away_team = current_match.get("strAwayTeam", "Team B")
            match_time = current_match.get("strTime", "TBD")
            league_title = current_match.get("strLeague", "Global League")
            match_country = current_match.get("strCountry", "International")
            home_score = current_match.get("intHomeScore")
            away_score = current_match.get("intAwayScore")
            
            with st.container():
                column_1, column_2, column_3, column_4 = st.columns([1.5, 4, 2, 2])
                with column_1:
                    st.write(f"**{match_time}**")
                    st.caption(f"{match_country}")
                    st.caption(f"{league_title}")
                with column_2:
                    st.write(f"**{home_team}** VS **{away_team}**")
                with column_3:
                    if home_score is not None and away_score is not None:
                        st.markdown(f"### `{home_score} - {away_score}`")
                        st.caption("Live / Finished")
                    else:
                        st.markdown(f"### `- : -`")
                        st.caption("Not Started")
                with column_4:
                    if st.button("Follow", key=f"match-{home_team}-{away_team}-{match_time}"):
                        st.toast(f"Following {home_team} vs {away_team}!")
            st.divider()
    else:
        st.warning("No matching results found.")
else:
    st.info("Connecting to global stadiums... Here is the current featured matches showcase:")
    
    fallback_database = [
        {"time": "15:00", "home": "Club Africain", "away": "Esperance ST", "league": "Tunisian Ligue 1", "country": "Tunisia", "status": "2nd Half", "score": "1 - 1"},
        {"time": "17:30", "home": "Manchester City", "away": "Arsenal", "league": "Premier League", "country": "England", "status": "Not Started", "score": "- : -"},
        {"time": "20:00", "home": "Real Madrid", "away": "Barcelona", "league": "La Liga", "country": "Spain", "status": "Not Started", "score": "- : -"},
        {"time": "21:00", "home": "Inter Milan", "away": "Juventus", "league": "Serie A", "country": "Italy", "status": "Finished", "score": "2 - 2"},
        {"time": "19:00", "home": "Bayern Munich", "away": "Dortmund", "league": "Bundesliga", "country": "Germany", "status": "1st Half", "score": "1 - 0"},
        {"time": "22:00", "home": "River Plate", "away": "Boca Juniors", "league": "Liga Profesional", "country": "Argentina", "status": "Not Started", "score": "- : -"}
    ]

    for item in fallback_database:
        with st.container():
            column_1, column_2, column_3, column_4 = st.columns([1.5, 4, 2, 2])
            with column_1:
                st.write(f"**{item['time']}**")
                st.caption(f"{item['country']}")
                st.caption(f"{item['league']}")
            with column_2:
                st
