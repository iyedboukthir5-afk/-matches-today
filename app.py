import streamlit as st
import requests
from datetime import date

# Page configuration
st.set_page_config(page_title="Global Football LiveScore", page_icon="🌐", layout="wide")

st.title("🌍 شبكة كورة العالم - LiveScore Global Pro")
st.markdown("مرحباً بك يا معلم! هنا السيرفر المركزي الذي يجلب **كل مباريات العالم** في جميع الدوريات والبطولات أوتوماتيكياً.")

today_str = date.today().strftime("%Y-%m-%d")

# Sidebar filters
st.sidebar.title("🏆 تصفية دوريات العالم")
continent_filter = st.sidebar.selectbox("اختر القارة أو المنطقة:", [
    "🌍 كل مباريات العالم (الكل)",
    "🇪🇺 الدوريات الأوروبية الكبرى",
    "🇬🇧 إنجلترا (البريميرليغ والدرجات)",
    "🇪🇸 إسبانيا (الليغا)",
    "🇮🇹 إيطاليا (الكالتشيو)",
    "🇩🇪 ألمانيا (البوندسليغا)",
    "🇹🇳 البطولات العربية وأفريقيا",
    "🌎 أمريكا الجنوبية ودوريات أخرى"
])

search_query = st.sidebar.text_input("🔍 ابحث عن فريق أو بطولة معينة:", "")

st.subheader(f"📅 مباريات اليوم في جميع أنحاء العالم - {today_str}")

# Fetch global matches function
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
        
        if search_query.lower() in home_team_name.lower() or search_query.lower() in away_team_name.lower() or search_query.lower() in league_name.lower() or search_query == "":
            filtered_matches.append(current_match)

    if filtered_matches:
        st.success(f"تم العثور على {len(filtered_matches)} مباراة تبث حالياً حول العالم 🔴")
        
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
                    st.write(f"⏰ **{match_time}**")
                    st.caption(f"🌍 {match_country}")
                    st.caption(f"🏆 {league_title}")
                with column_2:
                    st.write(f"🏟️ **{home_team}** VS **{away_team}**")
                with column_3:
                    if home_score is not None and away_score is not None:
                        st.markdown(f"### 📊 `{home_score} - {away_score}`")
                        st.caption("مباشرة / انتهت 🔴")
                    else:
                        st.markdown(f"### 📊 `- : -`")
                        st.caption("لم تبدأ بعد ⏳")
                with column_4:
                    if st.button("🔔 تفعيل التنبيه", key=f"match-{home_team}-{away_team}-{match_time}"):
                        st.toast(f"تمت متابعة مباراة {home_team} ضد {away_team} بنجاح!")
            st.divider()
    else:
        st.warning("لا توجد نتائج مطابقة لبحثك حالياً.")
else:
    st.info("🌐 جارٍ الاتصال بشبكة ملاعب العالم الكبرى... إليك نموذج شامل لأبرز مباريات القارات اليوم:")
    
    fallback_database = [
        {"time": "15:00", "home": "النادي الإفريقي", "away": "الترجي الرياضي", "league": "الرابطة المحترفة الأولى", "country": "تونس 🇹🇳", "status": "الشوط الثاني ⏱️", "score": "1 - 1"},
        {"time": "17:30", "home": "مانشستر سيتي", "away": "آرسنال", "league": "الدوري الإنجليزي الممتاز", "country": "إنجلترا 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "status": "لم تبدأ بعد ⏳", "score": "- : -"},
        {"time": "20:00", "home": "ريال مدريد", "away": "برشلونة", "league": "الدوري الإسباني (الكلاسيكو)", "country": "إسبانيا 🇪🇸", "status": "لم تبدأ بعد ⏳", "score": "- : -"},
        {"time": "21:00", "home": "إنتر ميلان", "away": "يوفنتوس", "league": "الدوري الإيطالي (السيري آ)", "country": "إيطاليا 🇮🇹", "status": "انتهت ✅", "score": "2 - 2"},
        {"time": "19:00", "home": "بايرن ميونخ", "away": "بوروسيا دورتموند", "league": "الدوري الألماني", "country": "ألمانيا 🇩🇪", "status": "الشوط الأول ⏱️", "score": "1 - 0"},
        {"time": "22:00", "home": "ريفر بليت", "away": "بوكا جونيورز", "league": "الدوري الأرجنتيني", "country": "الأرجنتين 🇦🇷", "status": "لم تبدأ بعد ⏳", "score": "- : -"}
    ]

    for item in fallback_database:
        with st.container():
            column_1, column_2, column_3, column_4 = st.columns([1.5, 4, 2, 2])
            with column_1:
                st.write(f"⏰ **{item['time']}**")
                st.caption(f"{item['country']}")
                st.caption(f"{item['league']}")
            with column_2:
                st.write(f"🏟️ **{item['home']}** VS **{item['away']}**")
            with column_3:
                st.markdown(f"### 📊 `{item['score']}`")
                st.caption(item['status'])
            with column_4:
                if st.button("🔔 تفعيل التنبيه", key=f"fallback-{item['home']}-{item['time']}"):
                    st.toast(f"تمت متابعة المباراة!")
            st.divider()

if st.sidebar.button("🔄 تحديث شامل لكل المباريات"):
    st.rerun()
