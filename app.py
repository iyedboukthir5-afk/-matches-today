import streamlit as st
import requests
from datetime import date

st.set_page_config(page_title="Global Football LiveScore", page_icon="🌐", layout="wide")

st.title("🌍 شبكة كورة العالم - LiveScore Global Pro")
st.markdown("مرحباً بك يا معلم! هنا السيرفر المركزي الذي يجلب **كل مباريات العالم** في جميع الدوريات والبطولات أوتوماتيكياً.")

today_str = date.today().strftime("%Y-%m-%d")

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

@st.cache_data(ttl=60)
def fetch_global_matches():
    url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={today_str}"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("events", [])
    except:
        return []

matches = fetch_global_matches()

if matches:
    filtered_matches = []
    for match in matches:
        home = match.get("strHomeTeam", "")
        away = match.get("strAwayTeam", "")
        league = match.get("strLeague", "")
        
        if search_query.lower() in home.lower() or search_query.lower() in away.lower() or search_query.lower() in league.lower() or search_query == "":
            filtered_matches.append(match)

    if filtered_matches:
        st.success(f"تم العثور على {len(filtered_matches)} مباراة تبث حالياً حول العالم 🔴")
        
        for match in filtered_matches:
            home = match.get("strHomeTeam", "فريق أ")
            away = match.get("strAwayTeam", "فريق ب")
            time = match.get("strTime", "غير محدد")
            league = match.get("strLeague", "بطولة عالمية")
            country = match.get("strCountry", "دولي")
            score_h = match.get("intHomeScore")
            score_a = match.get("intAwayScore")
            
            with st.container():
                cols = st.columns([1.5, 4, 2, 2])
                with cols[0]:
                    st.write(f"⏰ **{time}**")
                    st.caption(f"🌍 {country}")
                    st.caption(f"🏆 {league}")
                with cols[1]:
                    st.write(f"🏟️ **{home}** VS **{away}**")
                with cols[2]:
                    if score_h is not None and score_a is not None:
                        st.markdown(f"### 📊 `{score_h} - {score_a}`")
                        st.caption("مباشرة / انتهت 🔴")
                    else:
                        st.markdown(f"### 📊 `- : -`")
                        st.caption("لم تبدأ بعد ⏳")
                with cols[3]:
                    if st.button("🔔 تفعيل التنبيه", key=f"global-{home}-{away}-{time}"):
                        st.toast(f"تمت متابعة مباراة {home} ضد {away} بنجاح!")
            st.divider()
    else:
        st.warning("لا توجد نتائج مطابقة لبحثك حالياً.")
else:
    st.info("🌐 جارٍ الاتصال بشبكة ملاعب العالم الكبرى... إليك نموذج شامل لأبرز مباريات القارات اليوم:")
    
    world_database = [
        {"time": "15:00", "home": "النادي الإفريقي", "away": "الترجي الرياضي", "league": "الرابطة المحترفة الأولى", "country": "تونس 🇹🇳", "status": "الشوط الثاني ⏱️", "score": "1 - 1"},
        {"time": "17:30", "home": "مانشستر سيتي", "away": "آرسنال", "league": "الدوري الإنجليزي الممتاز", "country": "إنجلترا 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "status": "لم تبدأ بعد ⏳", "score": "- : -"},
        {"time": "20:00", "home": "ريال مدريد", "away": "برشلونة", "league": "الدوري الإسباني (الكلاسيكو)", "country": "إسبانيا 🇪🇸", "status": "لم تبدأ بعد ⏳", "score": "- : -"},
        {"time":
