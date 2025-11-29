import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta
from api_client import APIClient
import pandas as pd

st.set_page_config(page_title="Reports - Dialed In Fitness", page_icon="📊", layout="wide")

# Initialize API client
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient(user_id=1)

api = st.session_state.api_client

st.title("📊 Performance Reports")
st.markdown("### Discover insights from your data")

# Check for active plan
active_plan = api.get_active_plan()
if not active_plan:
    st.warning("⚠️ No active plan found. Create a plan first!")
    st.stop()

# Date range selector
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=date.today() - timedelta(days=90))
with col2:
    end_date = st.date_input("End Date", value=date.today())

# Fetch data
try:
    logs = api.get_daily_logs(start_date=start_date, end_date=end_date)
except Exception as e:
    st.error(f"Error fetching data: {str(e)}")
    st.stop()

if not logs:
    st.info("📭 No data available for the selected period. Start logging your daily metrics!")
    st.stop()

# Convert to DataFrame for easier analysis
df = pd.DataFrame(logs)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

st.markdown("---")

# Report 1: Protein → Muscle Gain
st.markdown("## 🥩 Protein Intake vs Body Weight")
st.markdown("*How does your protein consumption correlate with muscle gains?*")

# Filter logs with body weight data
weight_data = df[df['body_weight'].notna()].copy()

if len(weight_data) > 1:
    fig = go.Figure()
    
    # Body weight trend
    fig.add_trace(go.Scatter(
        x=weight_data['date'],
        y=weight_data['body_weight'],
        name='Body Weight',
        yaxis='y',
        line=dict(color='blue', width=2)
    ))
    
    # Average daily protein (7-day rolling average)
    weight_data['protein_ma'] = weight_data['protein'].rolling(window=7, min_periods=1).mean()
    
    fig.add_trace(go.Scatter(
        x=weight_data['date'],
        y=weight_data['protein_ma'],
        name='Protein (7-day avg)',
        yaxis='y2',
        line=dict(color='red', width=2, dash='dash')
    ))
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis=dict(title="Body Weight (lbs)", side='left'),
        yaxis2=dict(title="Protein (g)", side='right', overlaying='y'),
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate correlation
    if len(weight_data[weight_data['protein'].notna()]) > 2:
        correlation = weight_data['protein'].corr(weight_data['body_weight'])
        st.metric("Correlation Coefficient", f"{correlation:.3f}")
        
        if correlation > 0.5:
            st.success("✅ Strong positive correlation! Higher protein intake is associated with weight gain.")
        elif correlation < -0.5:
            st.warning("⚠️ Negative correlation detected. Consider reviewing your nutrition strategy.")
        else:
            st.info("ℹ️ Weak correlation. More data may be needed to see clear patterns.")
else:
    st.info("📊 Not enough body weight data yet. Keep logging!")

st.markdown("---")

# Report 2: Carbs → Workout Performance
st.markdown("## 🍞 Carb Intake vs Workout Performance")
st.markdown("*Do high-carb days lead to better workouts?*")

workout_data = df[df['workout_score'].notna()].copy()

if len(workout_data) > 5:
    fig = px.scatter(
        workout_data,
        x='carbs',
        y='workout_score',
        trendline='ols',
        labels={'carbs': 'Carb Intake (g)', 'workout_score': 'Workout Score'},
        title='Carb Intake vs Workout Performance'
    )
    
    fig.update_traces(marker=dict(size=10, opacity=0.6))
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # High carb vs low carb comparison
    median_carbs = workout_data['carbs'].median()
    high_carb = workout_data[workout_data['carbs'] >= median_carbs]['workout_score'].mean()
    low_carb = workout_data[workout_data['carbs'] < median_carbs]['workout_score'].mean()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("High Carb Days", f"{high_carb:.1f}/100")
    with col2:
        st.metric("Low Carb Days", f"{low_carb:.1f}/100")
    with col3:
        diff = high_carb - low_carb
        st.metric("Difference", f"{diff:+.1f}", delta=f"{diff:+.1f}")
    
    if diff > 5:
        st.success("✅ You perform better on high-carb days!")
    elif diff < -5:
        st.info("🤔 Interestingly, you perform better on lower-carb days.")
    else:
        st.info("ℹ️ Carb intake doesn't seem to significantly impact your performance.")
else:
    st.info("📊 Not enough workout data yet. Keep logging!")

st.markdown("---")

# Report 3: Sleep → Training Volume
st.markdown("## 😴 Sleep Quality vs Training Volume")
st.markdown("*How does your sleep affect your workout capacity?*")

sleep_workout_data = df[(df['sleep_hours'].notna()) & (df['workout_score'].notna())].copy()

if len(sleep_workout_data) > 5:
    # Create sleep buckets
    sleep_workout_data['sleep_bucket'] = pd.cut(
        sleep_workout_data['sleep_hours'],
        bins=[0, 6, 7, 8, 12],
        labels=['<6 hrs', '6-7 hrs', '7-8 hrs', '8+ hrs']
    )
    
    # Average workout score by sleep bucket
    sleep_performance = sleep_workout_data.groupby('sleep_bucket')['workout_score'].agg(['mean', 'count']).reset_index()
    
    fig = go.Figure(data=[
        go.Bar(
            x=sleep_performance['sleep_bucket'],
            y=sleep_performance['mean'],
            text=sleep_performance['count'].apply(lambda x: f'n={x}'),
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        xaxis_title="Sleep Duration",
        yaxis_title="Average Workout Score",
        title="Workout Performance by Sleep Duration",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Find optimal sleep range
    best_sleep = sleep_performance.loc[sleep_performance['mean'].idxmax(), 'sleep_bucket']
    best_score = sleep_performance['mean'].max()
    
    st.success(f"✅ Your best workouts happen after **{best_sleep}** of sleep (avg score: {best_score:.1f}/100)")
else:
    st.info("📊 Not enough sleep & workout data yet. Keep logging!")

st.markdown("---")

# Report 4: Calorie Delta → Body Composition
st.markdown("## ⚖️ Calorie Balance vs Body Weight Trend")
st.markdown("*How is your calorie intake affecting your weight?*")

weight_cal_data = df[(df['body_weight'].notna()) & (df['calories'].notna())].copy()

if len(weight_cal_data) > 5:
    # Calculate calorie surplus/deficit
    weight_cal_data['calorie_delta'] = weight_cal_data['calories'] - active_plan['calorie_target']
    
    # 7-day rolling averages
    weight_cal_data['weight_ma'] = weight_cal_data['body_weight'].rolling(window=7, min_periods=1).mean()
    weight_cal_data['calorie_delta_ma'] = weight_cal_data['calorie_delta'].rolling(window=7, min_periods=1).mean()
    
    fig = go.Figure()
    
    # Weight trend
    fig.add_trace(go.Scatter(
        x=weight_cal_data['date'],
        y=weight_cal_data['weight_ma'],
        name='Body Weight (7-day avg)',
        yaxis='y',
        line=dict(color='blue', width=2)
    ))
    
    # Calorie delta
    fig.add_trace(go.Bar(
        x=weight_cal_data['date'],
        y=weight_cal_data['calorie_delta_ma'],
        name='Calorie Surplus/Deficit (7-day avg)',
        yaxis='y2',
        marker_color=weight_cal_data['calorie_delta_ma'].apply(lambda x: 'green' if x > 0 else 'red')
    ))
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis=dict(title="Body Weight (lbs)", side='left'),
        yaxis2=dict(title="Calorie Delta", side='right', overlaying='y'),
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate rate of change
    days_diff = (weight_cal_data['date'].max() - weight_cal_data['date'].min()).days
    if days_diff > 7:
        weight_change = weight_cal_data['body_weight'].iloc[-1] - weight_cal_data['body_weight'].iloc[0]
        weekly_rate = (weight_change / days_diff) * 7
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Starting Weight", f"{weight_cal_data['body_weight'].iloc[0]:.1f} lbs")
        with col2:
            st.metric("Current Weight", f"{weight_cal_data['body_weight'].iloc[-1]:.1f} lbs")
        with col3:
            st.metric("Weekly Rate", f"{weekly_rate:+.2f} lbs/week")
        
        # Advice based on goal
        if active_plan['goal'] == 'bulk':
            if 0.5 <= weekly_rate <= 1.0:
                st.success("✅ Perfect bulking rate! Aim for 0.5-1 lb/week.")
            elif weekly_rate > 1.0:
                st.warning("⚠️ Gaining too fast. Consider reducing calorie surplus.")
            else:
                st.info("ℹ️ Slow bulk. Consider increasing calorie surplus if desired.")
        elif active_plan['goal'] == 'cut':
            if -1.0 <= weekly_rate <= -0.5:
                st.success("✅ Perfect cutting rate! Aim for 0.5-1 lb/week loss.")
            elif weekly_rate < -1.0:
                st.warning("⚠️ Losing too fast. Consider increasing calories to preserve muscle.")
            else:
                st.info("ℹ️ Slow cut. Consider increasing calorie deficit if desired.")
else:
    st.info("📊 Not enough body weight & calorie data yet. Keep logging!")

# Quick nav
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("🏠 Back to Dashboard", use_container_width=True):
        st.switch_page("Home.py")
with col2:
    if st.button("📝 Log Today", use_container_width=True):
        st.switch_page("pages/1_Today.py")
