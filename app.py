import streamlit as st
import requests
from datetime import date

# إعدادات الصفحة الكبرى
st.set_page_config(page_title="Global Football LiveScore", page_icon="🌐", layout="wide")

st.title("🌍 شبكة كورة العالم - LiveScore Global Pro")
st.markdown("مرحباً بك يا معلم! هنا السيرفر المركزي الذي يجلب **كل مباريات العالم** في جميع الدوريات والبطولات أوتوماتيكياً.")

today_str = date.today().strftime("%Y-%m-%d")

# قائمة جانبية ضخمة لاختيار قارات ودوريات العالم الكل
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

# دالة ذكية جداً لجلب كل مباريات العالم من السيرفر الرياضي العالمي
@st.cache_data(ttl=60)
def fetch_global_matches():
    # رابط شامل لجلب أحداث اليوم الحالي لكل بطولات العالم المتاحة
    url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={today_str}"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("events", [])
    except:
        return []

matches = fetch_global_matches()

if matches:
    # فلتر البحث والفلتر الجانبي
    filtered_matches = []
    for match in matches:
        home = match.get("strHomeTeam", "")
        away = match.get("strAwayTeam", "")
        league = match.get("strLeague", "")
        
        # تطبيق البحث لو المستخدم كتب اسم فريق
        if search_query.lower() in home.lower() or search_query.lower() in away.lower() or search_query.lower() in league.lower() or search_query == "":
            filtered_matches.append(match)

    if filtered_matches:
        st.success(تم العثور على {len(filtered_matches)} مباراة تبث حالياً حول العالم 🔴)
        
        for match in filtered_matches:
            home = match.get("strHomeTeam", "فريق أ")
            away = match.get("strAwayTeam", "فريق ب")
            time = match.get("strTime", "غير محدد")
            league = match.get("strLeague", "بطولة عالمية")
            country = match.get("strCountry", "دولي")
            score_h = match.get("intHomeScore")
            score_a = match.get("intAwayScore")
            
            with st.container():
                cols = st.columns([1.5, 4, 
