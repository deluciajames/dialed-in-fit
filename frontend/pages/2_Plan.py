import streamlit as st
from datetime import date
from api_client import APIClient

st.set_page_config(page_title="Plan - Dialed In Fitness", page_icon="📋", layout="wide")

# Initialize API client
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient(user_id=1)

api = st.session_state.api_client

st.title("📋 Your Fitness Plan")

# Get active plan
active_plan = api.get_active_plan()

# Tabs for Current Plan and Create/Edit
tab1, tab2, tab3 = st.tabs(["📌 Current Plan", "✏️ Create/Edit Plan", "📚 Plan History"])

with tab1:
    if active_plan:
        st.success("✅ You have an active plan!")
        
        # Display plan details
        st.markdown(f"## {active_plan['name']}")
        st.markdown(f"**Goal:** {active_plan['goal'].upper()}")
        st.markdown(f"**Started:** {active_plan['start_date']}")
        
        st.markdown("---")
        
        # Nutrition targets
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🍽️ Nutrition Targets")
            st.metric("Calories", f"{active_plan['calorie_target']} cal")
            st.caption(f"±{active_plan['calorie_margin_percent']*100:.0f}% margin")
            
            st.metric("Protein", f"{active_plan['protein_target']}g")
            st.caption(f"±{active_plan['protein_margin_percent']*100:.0f}% margin")
            
            st.metric("Carbs", f"{active_plan['carbs_target']}g")
            st.caption(f"±{active_plan['carbs_margin_percent']*100:.0f}% margin")
            
            st.metric("Fat", f"{active_plan['fat_target']}g")
            st.caption(f"±{active_plan['fat_margin_percent']*100:.0f}% margin")
        
        with col2:
            st.markdown("### 💪 Training Targets")
            st.metric("Training Days/Week", active_plan['training_days_per_week'])
            
            st.markdown("**Rep Targets (per week):**")
            for body_part, reps in active_plan['body_part_targets'].items():
                st.write(f"- **{body_part.title()}:** {reps} reps")
            
            st.markdown("### 😴 Wellness Targets")
            st.metric("Sleep", f"{active_plan['sleep_target_hours']} hours")
            st.metric("Steps", f"{active_plan['steps_target']:,}")
            st.metric("Hydration", f"{active_plan['hydration_target_oz']} oz")
            
            if active_plan['supplements']:
                st.markdown("**Supplements:**")
                for supp in active_plan['supplements']:
                    st.write(f"- {supp}")
    
    else:
        st.warning("⚠️ No active plan. Create one to get started!")

with tab2:
    st.markdown("## Create or Edit Your Plan")
    
    # If editing existing plan
    if active_plan and st.checkbox("Edit current plan"):
        is_editing = True
        st.info("Editing your current plan")
    else:
        is_editing = False
        st.success("Creating a new plan")
    
    with st.form("plan_form"):
        # Basic info
        plan_name = st.text_input(
            "Plan Name",
            value=active_plan['name'] if is_editing else "",
            placeholder="e.g., Winter Bulk 2025"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            goal = st.selectbox(
                "Goal",
                options=["bulk", "cut", "maintain"],
                index=["bulk", "cut", "maintain"].index(active_plan['goal']) if is_editing else 0
            )
        
        with col2:
            start_date_input = st.date_input(
                "Start Date",
                value=date.fromisoformat(active_plan['start_date']) if is_editing else date.today()
            )
        
        st.markdown("---")
        
        # Nutrition
        st.markdown("### 🍽️ Nutrition Targets")
        col1, col2 = st.columns(2)
        
        with col1:
            calorie_target = st.number_input(
                "Calorie Target",
                min_value=1000,
                max_value=10000,
                value=active_plan['calorie_target'] if is_editing else 2500,
                step=100
            )
            calorie_margin = st.slider(
                "Calorie Forgiveness %",
                min_value=3,
                max_value=5,
                value=int(active_plan['calorie_margin_percent']*100) if is_editing else 5
            )
            
            protein_target = st.number_input(
                "Protein Target (g)",
                min_value=50,
                max_value=500,
                value=active_plan['protein_target'] if is_editing else 180,
                step=10
            )
            protein_margin = st.slider(
                "Protein Forgiveness %",
                min_value=3,
                max_value=5,
                value=int(active_plan['protein_margin_percent']*100) if is_editing else 5
            )
        
        with col2:
            carbs_target = st.number_input(
                "Carbs Target (g)",
                min_value=50,
                max_value=1000,
                value=active_plan['carbs_target'] if is_editing else 250,
                step=10
            )
            carbs_margin = st.slider(
                "Carbs Forgiveness %",
                min_value=3,
                max_value=5,
                value=int(active_plan['carbs_margin_percent']*100) if is_editing else 5
            )
            
            fat_target = st.number_input(
                "Fat Target (g)",
                min_value=20,
                max_value=300,
                value=active_plan['fat_target'] if is_editing else 70,
                step=5
            )
            fat_margin = st.slider(
                "Fat Forgiveness %",
                min_value=3,
                max_value=5,
                value=int(active_plan['fat_margin_percent']*100) if is_editing else 5
            )
        
        st.markdown("---")
        
        # Training
        st.markdown("### 💪 Training Targets")
        training_days = st.number_input(
            "Training Days per Week",
            min_value=1,
            max_value=7,
            value=active_plan['training_days_per_week'] if is_editing else 6
        )
        
        st.markdown("**Rep Targets per Body Part (per week):**")
        
        # Pre-define common body parts
        default_body_parts = ["chest", "back", "legs", "shoulders", "biceps", "triceps"]
        body_part_targets = {}
        
        cols = st.columns(2)
        for idx, body_part in enumerate(default_body_parts):
            with cols[idx % 2]:
                existing_value = 0
                if is_editing and body_part in active_plan['body_part_targets']:
                    existing_value = active_plan['body_part_targets'][body_part]
                
                reps = st.number_input(
                    f"{body_part.title()} (reps/week)",
                    min_value=0,
                    max_value=500,
                    value=existing_value if existing_value > 0 else (120 if body_part in ["chest", "back", "legs"] else 60),
                    step=10,
                    key=f"reps_{body_part}"
                )
                if reps > 0:
                    body_part_targets[body_part] = reps
        
        st.markdown("---")
        
        # Wellness
        st.markdown("### 😴 Wellness Targets")
        col1, col2 = st.columns(2)
        
        with col1:
            sleep_target = st.number_input(
                "Sleep Target (hours)",
                min_value=4.0,
                max_value=12.0,
                value=float(active_plan['sleep_target_hours']) if is_editing else 8.0,
                step=0.5
            )
            
            steps_target = st.number_input(
                "Steps Target",
                min_value=1000,
                max_value=30000,
                value=active_plan['steps_target'] if is_editing else 7000,
                step=500
            )
        
        with col2:
            hydration_target = st.number_input(
                "Hydration Target (oz)",
                min_value=32.0,
                max_value=200.0,
                value=float(active_plan['hydration_target_oz']) if is_editing else 100.0,
                step=8.0
            )
            
            # Supplements
            st.markdown("**Supplements (comma-separated):**")
            supplements_str = st.text_input(
                "Supplements",
                value=", ".join(active_plan['supplements']) if is_editing and active_plan['supplements'] else "",
                placeholder="e.g., Creatine, Vitamin D, Protein"
            )
            supplements = [s.strip() for s in supplements_str.split(",") if s.strip()]
        
        # Submit
        submitted = st.form_submit_button("💾 Save Plan", type="primary", use_container_width=True)
        
        if submitted:
            if not plan_name:
                st.error("Please provide a plan name")
            elif not body_part_targets:
                st.error("Please set rep targets for at least one body part")
            else:
                plan_data = {
                    "name": plan_name,
                    "goal": goal,
                    "start_date": start_date_input.isoformat(),
                    "calorie_target": int(calorie_target),
                    "calorie_margin_percent": calorie_margin / 100,
                    "protein_target": int(protein_target),
                    "protein_margin_percent": protein_margin / 100,
                    "carbs_target": int(carbs_target),
                    "carbs_margin_percent": carbs_margin / 100,
                    "fat_target": int(fat_target),
                    "fat_margin_percent": fat_margin / 100,
                    "training_days_per_week": int(training_days),
                    "body_part_targets": body_part_targets,
                    "sleep_target_hours": float(sleep_target),
                    "steps_target": int(steps_target),
                    "hydration_target_oz": float(hydration_target),
                    "supplements": supplements
                }
                
                try:
                    if is_editing:
                        result = api.update_plan(active_plan['id'], plan_data)
                        st.success("✅ Plan updated successfully!")
                    else:
                        result = api.create_plan(plan_data)
                        st.success("✅ New plan created successfully!")
                    
                    st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Error saving plan: {str(e)}")

with tab3:
    st.markdown("## Plan History")
    
    try:
        all_plans = api.get_all_plans()
        
        if all_plans:
            for plan in all_plans:
                is_active = plan['end_date'] is None
                status = "🟢 Active" if is_active else "⚪ Ended"
                
                with st.expander(f"{status} - {plan['name']} ({plan['start_date']})"):
                    st.markdown(f"**Goal:** {plan['goal'].upper()}")
                    st.markdown(f"**Started:** {plan['start_date']}")
                    if not is_active:
                        st.markdown(f"**Ended:** {plan['end_date']}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Nutrition:**")
                        st.write(f"- Calories: {plan['calorie_target']}")
                        st.write(f"- Protein: {plan['protein_target']}g")
                        st.write(f"- Carbs: {plan['carbs_target']}g")
                        st.write(f"- Fat: {plan['fat_target']}g")
                    
                    with col2:
                        st.markdown("**Training:**")
                        st.write(f"- {plan['training_days_per_week']} days/week")
                        for bp, reps in plan['body_part_targets'].items():
                            st.write(f"- {bp.title()}: {reps} reps/week")
        else:
            st.info("No plan history yet.")
    
    except Exception as e:
        st.error(f"Error loading plan history: {str(e)}")

# Quick nav
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button("🏠 Back to Dashboard", use_container_width=True):
        st.switch_page("Home.py")
with col2:
    if st.button("📝 Log Today", use_container_width=True):
        st.switch_page("pages/1_Today.py")
