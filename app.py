import streamlit as st
import requests
from datetime import date

# عنوان الموقع
st.title("⚽ موقع جدول مباريات اليوم - تونس")
st.markdown("مرحباً بك يا معلم! هنا تجد كل مباريات اليوم بتوقيتها والفرق المشاركة.")

# الحصول على تاريخ اليوم أوتوماتيكياً بالصيغة الصحيحة (السنة-الشهر-اليوم)
today_str = date.today().strftime("%Y-%m-%d")

# دالة لجلب مباريات اليوم الحالية أوتوماتيكياً
@st.cache_data(ttl=60)
def get_all_matches(day_date):
    url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={day_date}"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get("events", [])
    except:
        return []

st.subheader(f"📅 قائمة مباريات اليوم: {today_str}")

# جلب المباريات حسب تاريخ اليوم الحقيقي
matches = get_all_matches(today_str)

if matches:
    for match in matches:
        home_team = match.get("strHomeTeam", "فريق أ")
        away_team = match.get("strAwayTeam", "فريق ب")
        time = match.get("strTime", "غير محدد")
        league = match.get("strLeague", "بطولة رياضية")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"🏆 **{league}**")
            st.write(f"⏰ **التوقيت:** {time}")
        with col2:
            st.write(f"🏟️ **المباراة:**")
            st.write(f"{home_team} **VS** {away_team}")
        with col3:
            st.write(f"📊 **الحالة / النتيجة:**")
            score_home = match.get("intHomeScore")
            score_away = match.get("intAwayScore")
            if score_home is not None and score_away is not None:
                st.write(f"{score_home} - {score_away}")
            else:
                st.write("لم تبدأ بعد ⏳")
        st.divider()
else:
    # كمثال تعليمي إذا السيرفر المجاني ما رجعش ماتشوات اليوم، نعرضو جدول تجريبي باش تشوف الخدمة كيفاش تظهر
    st.info("لا توجد مباريات مسجلة حالياً في السيرفر المجاني لهذا اليوم، إليك نموذج تجريبي لاختبار الشكل:")
    
    demo_matches = [
        {"time": "18:00", "home": "النادي الإفريقي", "away": "الترجي الرياضي", "league": "الرابطة المحترفة الأولى"},
        {"time": "21:00", "home": "مانشستر سيتي", "away": "ريال مدريد", "league": "دوري أبطال أوروبا"}
    ]
    
    for match in demo_matches:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"🏆 **{match['league']}**")
            st.write(f"⏰ **التوقيت:** {match['time']}")
        with col2:
            st.write(f"🏟️ **المباراة:**")
            st.write(f"{match['home']} **VS** {match['away']}")
        with col3:
            st.write("📊 **لم تبدأ بعد ⏳**")
        st.divider()

if st.button("🔄 تحديث الجدول"):
    st.rerun()
