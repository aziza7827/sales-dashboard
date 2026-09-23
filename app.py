import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="لوحة تحكم تحليلية متقدمة", page_icon="📊", layout="wide")

st.title("📊 لوحة تحكم تحليلية الأداء (Performance Dashboard)")
st.markdown("---")
st.markdown("هذا التطبيق يعرض تحليلاً تفاعلياً للبيانات والرسوم البيانية لمساعدتك في اتخاذ القرارات الذكية.")

@st.cache_data
def load_data():
    data = {
        'التاريخ': pd.date_range(start='2026-01-01', periods=100, freq='D'),
        'القسم': ['إلكترونيات', 'ملابس', 'أثاث', 'أجهزة منزلية'] * 25,
        'المبيعات': [120, 300, 450, 200, 600, 150, 800, 350] * 12 + [200, 300, 400, 500],
        'العملاء': [10, 25, 30, 15, 40, 12, 55, 22] * 12 + [15, 20, 25, 30]
    }
    return pd.DataFrame(data)

df = load_data()

st.sidebar.header("⚙️ خيارات التصفية (Filters)")
selected_department = st.sidebar.selectbox("اختر القسم:", options=['الكل'] + list(df['القسم'].unique()))

if selected_department != 'الكل':
    df_filtered = df[df['القسم'] == selected_department]
else:
    df_filtered = df

total_sales = df_filtered['المبيعات'].sum()
total_customers = df_filtered['العملاء'].sum()
avg_sales = round(df_filtered['المبيعات'].mean(), 2)

col1, col2, col3 = st.columns(3)
col1.metric("إجمالي المبيعات", f"${total_sales:,.0f}", "+12% عن الشهر السابق")
col2.metric("إجمالي العملاء", f"{total_customers:,}", "+5% جدد")
col3.metric("متوسط المبيعات اليومية", f"${avg_sales:,.2f}", "مستقر")

st.markdown("---")

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📈 تطور المبيعات بمرور الوقت")
    fig_line = px.line(df_filtered, x='التاريخ', y='المبيعات', color='القسم', template='plotly_white')
    st.plotly_chart(fig_line, use_container_width=True)

with col_chart2:
    st.subheader("🍩 توزيع المبيعات حسب القسم")
    fig_pie = px.pie(df_filtered, names='القسم', values='المبيعات', hole=0.4, template='plotly_white')
    st.plotly_chart(fig_pie, use_container_width=True)

st.subheader("📋 جدول البيانات التفصيلي")
st.dataframe(df_filtered, use_container_width=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>تم تطوير هذا التطبيق بواسطة محلل بيانات ومطور ويب محترف 🚀</p>", unsafe_allow_html=True)
