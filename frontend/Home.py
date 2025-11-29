import streamlit as st
import plotly.graph_objects as go
from datetime import date
from api_client import APIClient

st.set_page_config(
    page_title="Dialed In Fitness",
    page_icon="💪",
    layout="wide"
)

# Initialize API client
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient(user_id=1)

api = st.session_state.api_client

# Page header
st.title("💪 Dialed In Fitness")
st.markdown("### Your Complete Fitness Command Center")

# Check if active plan exists
active_plan = api.get_active_plan()

if not active_plan:
    st.warning("⚠️ No active plan found. Please create a plan first!")
    st.markdown("👉 Go to the **Plan** page to set up your fitness plan.")
    st.stop()

# Time period selector
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📅 Last 7 Days", use_container_width=True):
        st.session_state.period = "7d"
with col2:
    if st.button("📅 Last 30 Days", use_container_width=True):
        st.session_state.period = "30d"
with col3:
    if st.button("📅 Last 90 Days", use_container_width=True):
        st.session_state.period = "90d"
with col4:
    if st.button("📅 Year to Date", use_container_width=True):
        st.session_state.period = "ytd"

# Default period
if "period" not in st.session_state:
    st.session_state.period = "7d"

# Fetch dashboard data
try:
    dashboard_data = api.get_dashboard(period=st.session_state.period)
except Exception as e:
    st.error(f"Error fetching dashboard data: {str(e)}")
    st.stop()

# Display current score - BIG AND BOLD
st.markdown("---")
st.markdown("## 🎯 Your Dialed In Score")

# Score display with color coding
current_score = dashboard_data["current_score"]
score_color_data = api.get_score_color(current_score)
score_color = score_color_data["color"]
score_label = score_color_data["label"]

# Map colors to hex
color_map = {
    "red": "#FF4B4B",
    "yellow": "#FFA500",
    "green": "#00C853"
}
hex_color = color_map.get(score_color, "#888888")

# Big score display
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        f"""
        <div style='text-align: center; padding: 30px; background-color: {hex_color}20; border-radius: 15px; border: 3px solid {hex_color};'>
            <h1 style='color: {hex_color}; font-size: 80px; margin: 0;'>{current_score:.1f}/10</h1>
            <p style='color: {hex_color}; font-size: 24px; margin: 0;'>{score_label}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# Period average
period_labels = {
    "7d": "7-Day Average",
    "30d": "30-Day Average",
    "90d": "90-Day Average",
    "ytd": "Year-to-Date Average"
}
period_avg = dashboard_data["period_average"]

st.markdown(f"### {period_labels[st.session_state.period]}: **{period_avg:.1f}/10**")

# Score trend chart
st.markdown("### 📈 Score Trend")

daily_scores = dashboard_data["daily_scores"]
if daily_scores:
    dates = [item["date"] for item in daily_scores]
    scores = [item["score"] for item in daily_scores]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=scores,
        mode='lines+markers',
        name='Daily Score',
        line=dict(color='#00C853', width=3),
        marker=dict(size=8)
    ))
    
    # Add target line at 8.5 (Good threshold)
    fig.add_hline(y=8.5, line_dash="dash", line_color="green", annotation_text="Dialed In")
    fig.add_hline(y=7.0, line_dash="dash", line_color="orange", annotation_text="Good")
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Score (0-10)",
        yaxis_range=[0, 10],
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No data available for the selected period. Start logging your daily metrics!")

# Score breakdown
st.markdown("---")
st.markdown("### 📊 Today's Score Breakdown")

breakdown = dashboard_data["score_breakdown"]

# Create columns for breakdown
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🍽️ Diet & Exercise (75%)")
    
    metrics_diet = {
        "Calories": (breakdown["calories"], 20),
        "Protein": (breakdown["protein"], 10),
        "Carbs": (breakdown["carbs"], 10),
        "Fats": (breakdown["fat"], 10),
        "Workout Volume": (breakdown["workout"], 25),
    }
    
    for metric, (score, weight) in metrics_diet.items():
        score_pct = score if score <= 100 else 100
        st.markdown(f"**{metric}** ({weight}%)")
        st.progress(score_pct / 100)
        st.caption(f"Score: {score:.0f}/100")
        st.markdown("")

with col2:
    st.markdown("#### 😴 Wellness (25%)")
    
    metrics_wellness = {
        "Sleep": (breakdown["sleep"], 10),
        "Steps": (breakdown["steps"], 5),
        "Supplements": (breakdown["supplements"], 5),
        "Hydration": (breakdown["hydration"], 5),
    }
    
    for metric, (score, weight) in metrics_wellness.items():
        score_pct = score if score <= 100 else 100
        st.markdown(f"**{metric}** ({weight}%)")
        st.progress(score_pct / 100)
        st.caption(f"Score: {score:.0f}/100")
        st.markdown("")

# Quick actions
st.markdown("---")
st.markdown("### ⚡ Quick Actions")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📝 Log Today's Metrics", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Today.py")
with col2:
    if st.button("📋 View/Edit Plan", use_container_width=True):
        st.switch_page("pages/2_Plan.py")
with col3:
    if st.button("📊 View Reports", use_container_width=True):
        st.switch_page("pages/3_Reports.py")
