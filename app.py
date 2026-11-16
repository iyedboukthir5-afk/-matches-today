import streamlit as st
import folium
from streamlit_folium import st_folium

# عنوان الموقع
st.title("🗺️ موقعي الأول للخرائط التفاعلية")
st.write("هذا موقع ويب حقيقي تعرض فيه خريطة تفاعلية لتعيين الأماكن!")

# اختيار المدينة أو الإحداثيات (مثلاً تونس العاصمة)
lat = 36.8065
lon = 10.1815

# إنشاء الخريطة باستخدام Folium
m = folium.Map(location=[lat, lon], zoom_start=13)

# إضافة علامة (Marker) على الخريطة
folium.Marker(
    location=[lat, lon],
    popup="تونس العاصمة",
    tooltip="اضغط هنا للتفاصيل"
).add_to(m)

# عرض الخريطة داخل موقع Streamlit
st_folium(m, width=700, height=500)

st.success("تم تشغيل الخريطة بنجاح داخل موقع الويب!")
