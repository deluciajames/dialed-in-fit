import streamlit as st
from datetime import date
from api_client import APIClient

st.set_page_config(page_title="Today - Dialed In Fitness", page_icon="📝", layout="wide")

# Initialize API client
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient(user_id=1)

api = st.session_state.api_client

st.title("📝 Today's Log")
st.markdown("### Track your daily metrics")

# Check for active plan
active_plan = api.get_active_plan()
if not active_plan:
    st.error("⚠️ No active plan found. Please create a plan first!")
    if st.button("Go to Plan Page"):
        st.switch_page("pages/2_Plan.py")
    st.stop()

# Date selector
log_date = st.date_input("Select Date", value=date.today(), max_value=date.today())

# Check if log already exists for this date
existing_log = api.get_daily_log_by_date(log_date)

st.markdown("---")

# Initialize form data
if existing_log:
    st.info(f"📋 Editing existing log for {log_date}")
    is_editing = True
else:
    st.success(f"✨ Creating new log for {log_date}")
    is_editing = False

# Create form
with st.form("daily_log_form"):
    
    # Nutrition Section
    st.markdown("## 🍽️ Nutrition")
    col1, col2 = st.columns(2)
    
    with col1:
        calories = st.number_input(
            "Calories",
            min_value=0,
            value=existing_log["calories"] if existing_log and existing_log["calories"] else 0,
            step=50
        )
        protein = st.number_input(
            "Protein (g)",
            min_value=0,
            value=existing_log["protein"] if existing_log and existing_log["protein"] else 0,
            step=5
        )
    
    with col2:
        carbs = st.number_input(
            "Carbs (g)",
            min_value=0,
            value=existing_log["carbs"] if existing_log and existing_log["carbs"] else 0,
            step=5
        )
        fat = st.number_input(
            "Fat (g)",
            min_value=0,
            value=existing_log["fat"] if existing_log and existing_log["fat"] else 0,
            step=5
        )
    
    st.markdown("---")
    
    # Workout Section
    st.markdown("## 💪 Workouts")
    
    # Rest day checkbox
    is_rest_day = st.checkbox(
        "This is a rest day (no workouts)",
        value=existing_log["is_rest_day"] if existing_log else False
    )
    
    workouts = []
    
    if not is_rest_day:
        # Number of exercises
        num_exercises = st.number_input(
            "Number of exercises",
            min_value=1,
            max_value=20,
            value=len(existing_log["workouts"]) if existing_log and existing_log.get("workouts") else 1,
            step=1
        )
        
        st.markdown("### Exercise Details")
        
        for i in range(int(num_exercises)):
            st.markdown(f"**Exercise {i+1}**")
            col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
            
            existing_workout = None
            if existing_log and existing_log.get("workouts") and i < len(existing_log["workouts"]):
                existing_workout = existing_log["workouts"][i]
            
            with col1:
                body_part = st.selectbox(
                    "Body Part",
                    options=list(active_plan["body_part_targets"].keys()),
                    key=f"body_part_{i}",
                    index=list(active_plan["body_part_targets"].keys()).index(existing_workout["body_part"]) if existing_workout else 0
                )
            
            with col2:
                exercise_name = st.text_input(
                    "Exercise Name",
                    value=existing_workout["exercise_name"] if existing_workout else "",
                    key=f"exercise_{i}",
                    placeholder="e.g., Bench Press"
                )
            
            with col3:
                sets = st.number_input(
                    "Sets",
                    min_value=1,
                    value=existing_workout["sets"] if existing_workout else 3,
                    key=f"sets_{i}"
                )
            
            with col4:
                reps = st.number_input(
                    "Reps",
                    min_value=1,
                    value=existing_workout["reps"] if existing_workout else 10,
                    key=f"reps_{i}"
                )
            
            with col5:
                weight = st.number_input(
                    "Weight (lbs)",
                    min_value=0.0,
                    value=float(existing_workout["weight"]) if existing_workout and existing_workout.get("weight") else 0.0,
                    key=f"weight_{i}",
                    step=5.0
                )
            
            if exercise_name:
                workouts.append({
                    "body_part": body_part,
                    "exercise_name": exercise_name,
                    "sets": int(sets),
                    "reps": int(reps),
                    "weight": float(weight) if weight > 0 else None
                })
            
            st.markdown("")
    
    st.markdown("---")
    
    # Wellness Section
    st.markdown("## 😴 Wellness")
    col1, col2 = st.columns(2)
    
    with col1:
        sleep_hours = st.number_input(
            "Sleep (hours)",
            min_value=0.0,
            max_value=24.0,
            value=float(existing_log["sleep_hours"]) if existing_log and existing_log["sleep_hours"] else 0.0,
            step=0.5
        )
        steps = st.number_input(
            "Steps",
            min_value=0,
            value=existing_log["steps"] if existing_log and existing_log["steps"] else 0,
            step=100
        )
    
    with col2:
        hydration_oz = st.number_input(
            "Hydration (oz)",
            min_value=0.0,
            value=float(existing_log["hydration_oz"]) if existing_log and existing_log["hydration_oz"] else 0.0,
            step=8.0
        )
        
        # Supplements
        st.markdown("**Supplements Taken**")
        supplements_taken = []
        if active_plan["supplements"]:
            for supp in active_plan["supplements"]:
                taken = st.checkbox(
                    supp,
                    value=supp in (existing_log["supplements_taken"] or []) if existing_log else False,
                    key=f"supp_{supp}"
                )
                if taken:
                    supplements_taken.append(supp)
    
    st.markdown("---")
    
    # Optional: Body Metrics
    with st.expander("📏 Body Metrics (Optional)"):
        col1, col2 = st.columns(2)
        with col1:
            body_weight = st.number_input(
                "Body Weight (lbs)",
                min_value=0.0,
                value=float(existing_log["body_weight"]) if existing_log and existing_log.get("body_weight") else 0.0,
                step=0.1
            )
        with col2:
            body_fat_percent = st.number_input(
                "Body Fat %",
                min_value=0.0,
                max_value=100.0,
                value=float(existing_log["body_fat_percent"]) if existing_log and existing_log.get("body_fat_percent") else 0.0,
                step=0.1
            )
    
    # Submit button
    submitted = st.form_submit_button("💾 Save Log", type="primary", use_container_width=True)
    
    if submitted:
        # Prepare log data
        log_data = {
            "date": log_date.isoformat(),
            "calories": int(calories) if calories > 0 else None,
            "protein": int(protein) if protein > 0 else None,
            "carbs": int(carbs) if carbs > 0 else None,
            "fat": int(fat) if fat > 0 else None,
            "sleep_hours": float(sleep_hours) if sleep_hours > 0 else None,
            "steps": int(steps) if steps > 0 else None,
            "hydration_oz": float(hydration_oz) if hydration_oz > 0 else None,
            "supplements_taken": supplements_taken if supplements_taken else None,
            "body_weight": float(body_weight) if body_weight > 0 else None,
            "body_fat_percent": float(body_fat_percent) if body_fat_percent > 0 else None,
            "is_rest_day": is_rest_day,
            "workouts": workouts
        }
        
        try:
            if is_editing:
                # Update existing log
                result = api.update_daily_log(existing_log["id"], log_data)
                st.success(f"✅ Log updated successfully! Your Dialed In Score: **{result['total_score']:.1f}/10**")
            else:
                # Create new log
                result = api.create_daily_log(log_data)
                st.success(f"✅ Log saved successfully! Your Dialed In Score: **{result['total_score']:.1f}/10**")
            
            # Show score breakdown
            with st.expander("📊 See Score Breakdown"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Calories", f"{result['calorie_score']:.0f}/100")
                    st.metric("Protein", f"{result['protein_score']:.0f}/100")
                    st.metric("Carbs", f"{result['carbs_score']:.0f}/100")
                    st.metric("Fat", f"{result['fat_score']:.0f}/100")
                    st.metric("Workout", f"{result['workout_score']:.0f}/100")
                
                with col2:
                    st.metric("Sleep", f"{result['sleep_score']:.0f}/100")
                    st.metric("Steps", f"{result['steps_score']:.0f}/100")
                    st.metric("Supplements", f"{result['supplements_score']:.0f}/100")
                    st.metric("Hydration", f"{result['hydration_score']:.0f}/100")
            
            # Refresh the page data
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error saving log: {str(e)}")

# Quick nav
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("🏠 Back to Dashboard", use_container_width=True):
        st.switch_page("Home.py")
with col2:
    if st.button("📊 View Reports", use_container_width=True):
        st.switch_page("pages/3_Reports.py")
