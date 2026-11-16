import streamlit as st
from datetime import date

# إعداد الصفحة لتكون واسعة ومريحة كيف المواقع الكبيرة
st.set_page_config(page_title="FlashScore Tunisia", page_icon="⚽", layout="wide")

# تصميم العنوان الرئيسي
st.title("⚡ FlashScore - تونس (نسخة المطورين)")
st.markdown("مرحباً بك يا معلم في قلب الحدث الرياضي المباشر!")

# تاريخ اليوم
today_str = date.today().strftime("%Y-%m-%d")

# قائمة جانبية (Sidebar) للتحكم في الأقسام كيف Flashscore
st.sidebar.title("🎛️ أقسام الموقع")
app_mode = st.sidebar.selectbox("اختر القسم:", ["📅 مباريات اليوم", "📊 ترتيب الهدافين والفرق", "⭐ المباريات المفضلة"])

if app_mode == "📅 مباريات اليوم":
    st.subheader(f"live 🔴 مباريات اليوم المباشرة - {today_str}")
    
    # فلتر حسب البطولات (كيف Flashscore)
    league_filter = st.selectbox("اختر البطولات:", ["الكل", "الرابطة المحترفة الأولى (تونس)", "دوري أبطال أوروبا", "الدوري الإنجليزي الممتاز"])
    
    st.divider()

    # محاكاة لجدول مباريات غني وفيه تفاصيل تكتيكية كيف الفلاش سكور
    matches_db = [
        {
            "league": "الرابطة المحترفة الأولى (تونس)",
            "time": "16:00",
            "home": "الترجي الرياضي",
            "away": "النادي الإفريقي",
            "score": "1 - 1",
            "status": "الشوط الثاني ⏱️",
            "events": "⚽ 23' رودريغو (الترجي) | ⚽ 55' توفيق الشريفي (الإفريقي)"
        },
        {
            "league": "دوري أبطال أوروبا",
            "time": "21:00",
            "home": "ريال مدريد",
            "away": "مانشستر سيتي",
            "score": "0 - 0",
            "status": "لم تبدأ بعد ⏳",
            "events": "التشكيلة الأساسية لم تعلن بعد"
        },
        {
            "league": "الدوري الإنجليزي الممتاز",
            "time": "18:30",
            "home": "لندن آرسنال",
            "away": "ليفربول",
            "score": "2 - 1",
            "status": "انتهت ✅",
            "events": "⚽ 12' ساكا | ⚽ 40' صلاح | ⚽ 78' تروسارد"
        }
    ]

    # عرض المباريات بطريقة احترافية
    for m in matches_db:
        if league_filter == "الكل" or league_filter == m["league"]:
            with st.container():
                cols = st.columns([1, 4, 2, 2])
                with cols[0]:
                    st.write(f"⏰ **{m['time']}**")
                    st.caption(m['status'])
                with cols[1]:
                    st.write(f"🏟️ **{m['home']}** VS **{m['away']}**")
                    st.caption(f"📝 *الأحداث:* {m['events']}")
                with cols[2]:
                    st.markdown(f"### 📊 `{m['score']}`")
                with cols[3]:
                    if st.button("🔔 متابعة", key=f"{m['home']}-{m['away']}"):
                        st.toast(f"تمت إضافة {m['home']} للمفضلة!")
            st.divider()

elif app_mode == "📊 ترتيب الهدافين والفرق":
    st.subheader("📊 جدول الترتيب العام (نموذج)")
    st.info("قريباً جداً سنتناول جلب جداول الترتيب الحقيقية من قواعد البيانات الكبرى!")
    
    # جدول تجريبي للترتيب
    import pandas as pd
    df = pd.DataFrame({
        "الفريق": ["الترجي الرياضي", "النادي الإفريقي", "النجم الساحلي", "النادي الصفاقسي"],
        "لعب": [10, 10, 10, 10],
        "نقاط": [25, 22, 19, 17]
    })
    st.table(df)

elif app_mode == "⭐ المباريات المفضلة":
    st.subheader("⭐ مبارياتك المفضلة والمتابعة")
    st.write("ليس لديك أي مباريات في قائمة المفضلة حالياً. اضغط على زر 'متابعة' في أي مباراة لإضافتها هنا.")

# زر تحديث عام
if st.sidebar.button("🔄 تحديث شامل للصفحة"):
    st.rerun()
