# 🧪 Testing Guide - Dialed In Fitness

## Quick Test Scenario

Here's a complete walkthrough to test all features:

### 1. Create Your First Plan

**Sample "Bulk" Plan:**
- Name: "Winter Bulk 2025"
- Goal: Bulk
- Start Date: Today
- Calories: 3000 (5% margin)
- Protein: 180g (5% margin)
- Carbs: 350g (5% margin)
- Fat: 80g (5% margin)
- Training Days: 6/week (1 rest day allowed)
- Body Part Targets:
  - Chest: 120 reps/week
  - Back: 120 reps/week
  - Legs: 120 reps/week
  - Shoulders: 90 reps/week
  - Biceps: 60 reps/week
  - Triceps: 60 reps/week
- Sleep: 8 hours
- Steps: 7000
- Hydration: 100 oz
- Supplements: Creatine, Vitamin D, Protein Powder

### 2. Log Day 1 - "Perfect Day"

**Nutrition:**
- Calories: 3050 (within margin!)
- Protein: 185g
- Carbs: 360g
- Fat: 78g

**Workouts (Push Day):**
1. Bench Press - Chest - 4 sets x 8 reps = 32 reps (135 lbs)
2. Incline DB Press - Chest - 3 sets x 10 reps = 30 reps (70 lbs)
3. Overhead Press - Shoulders - 4 sets x 8 reps = 32 reps (95 lbs)
4. Lateral Raises - Shoulders - 3 sets x 12 reps = 36 reps (25 lbs)
5. Tricep Pushdowns - Triceps - 3 sets x 12 reps = 36 reps (80 lbs)

Total: Chest 62 reps, Shoulders 68 reps, Triceps 36 reps

**Wellness:**
- Sleep: 8.5 hours
- Steps: 7200
- Hydration: 105 oz
- Supplements: All 3 checked

**Expected Score:** ~9.5+/10 (near perfect!)

### 3. Log Day 2 - "Good Day with Minor Misses"

**Nutrition:**
- Calories: 2850 (slightly under)
- Protein: 175g
- Carbs: 340g
- Fat: 75g

**Workouts (Pull Day):**
1. Deadlift - Back - 4 sets x 6 reps = 24 reps (225 lbs)
2. Pull-ups - Back - 4 sets x 8 reps = 32 reps (bodyweight)
3. Barbell Rows - Back - 3 sets x 10 reps = 30 reps (135 lbs)
4. Bicep Curls - Biceps - 3 sets x 10 reps = 30 reps (45 lbs)

Total: Back 86 reps, Biceps 30 reps

**Wellness:**
- Sleep: 7 hours (below target)
- Steps: 6500 (below target)
- Hydration: 90 oz
- Supplements: Forgot Vitamin D (only 2/3)

**Expected Score:** ~7.5-8/10 (good but not perfect)

### 4. Log Day 3 - "Rest Day"

**Nutrition:**
- Calories: 2900
- Protein: 180g
- Carbs: 320g (lower on rest day)
- Fat: 85g

**Workouts:**
- Check "This is a rest day"

**Wellness:**
- Sleep: 8 hours
- Steps: 8000 (more active recovery)
- Hydration: 100 oz
- Supplements: All 3

**Expected Score:** ~9/10 (rest day = 100% workout score)

### 5. Log Day 4 - "Leg Day"

**Nutrition:**
- Calories: 3200 (carb loading)
- Protein: 190g
- Carbs: 400g (high carb day)
- Fat: 75g

**Workouts:**
1. Squats - Legs - 4 sets x 8 reps = 32 reps (185 lbs)
2. Romanian Deadlifts - Legs - 3 sets x 10 reps = 30 reps (135 lbs)
3. Leg Press - Legs - 3 sets x 12 reps = 36 reps (315 lbs)
4. Leg Curls - Legs - 3 sets x 12 reps = 36 reps (90 lbs)

Total: Legs 134 reps (over target!)

**Wellness:**
- Sleep: 9 hours (feeling good!)
- Steps: 5000 (leg day fatigue)
- Hydration: 120 oz (drinking more)
- Supplements: All 3

**Expected Score:** ~9/10 (high carbs beneficial in bulk)

### 6. Log Day 5 - "Missed Workout"

**Nutrition:**
- Calories: 2700 (under)
- Protein: 160g (low)
- Carbs: 330g
- Fat: 70g

**Workouts:**
- (No workout logged, not marked as rest day)

**Wellness:**
- Sleep: 6 hours (bad sleep)
- Steps: 4500 (low)
- Hydration: 75 oz
- Supplements: Only took 1/3

**Expected Score:** ~4-5/10 (missed workout hurts)

### 7. Check Dashboard

After logging 5 days:

**Expected Dashboard View:**
- Current Score (Day 5): 4-5/10 (🔴 Red)
- 7-Day Average: ~7.5/10 (🟡 Yellow)
- Trend Chart: Shows variance across days
- Breakdown: Identifies workout and wellness as weak points on Day 5

### 8. View Reports

**After 2 weeks of varied logging:**

**Protein → Muscle Gain:**
- Should show body weight data points if entered
- Calculate correlation between protein and weight

**Carbs → Workout Performance:**
- Day 4 (high carbs) should show better workout score
- Day 2 (lower carbs) should show slightly lower

**Sleep → Training Volume:**
- Days with 8+ hours should cluster higher
- Day 5 (6 hours) should show impact

**Calorie Balance → Weight:**
- Track surplus days vs weight trend
- Show rate of gain (should be ~0.5-1 lb/week for healthy bulk)

## Testing Checklist

### Backend API (http://localhost:8000/docs)

- [ ] Create a plan via POST /plans/
- [ ] Get active plan via GET /plans/active
- [ ] Create daily log via POST /logs/
- [ ] Update daily log via PUT /logs/{id}
- [ ] Get dashboard data via GET /dashboard/
- [ ] Test different time periods (7d, 30d, 90d, ytd)

### Frontend UI

- [ ] Plan page: Create plan successfully
- [ ] Plan page: View current plan details
- [ ] Plan page: Edit existing plan
- [ ] Plan page: View plan history
- [ ] Today page: Create new log
- [ ] Today page: Edit existing log
- [ ] Today page: Add multiple exercises
- [ ] Today page: Mark as rest day
- [ ] Today page: See score immediately after save
- [ ] Home page: View current score
- [ ] Home page: Toggle time periods
- [ ] Home page: See score trend chart
- [ ] Home page: View score breakdown
- [ ] Reports page: All 4 reports load
- [ ] Reports page: Charts display correctly
- [ ] Reports page: Insights make sense

### Scoring Logic

- [ ] Perfect day scores 9.5+/10
- [ ] Missed metrics lower score appropriately
- [ ] Forgiveness margin works (3050 cal = 100% for 3000 target)
- [ ] Pyramid penalty works (3300 cal < 3050 cal score)
- [ ] Rest days count as 100% if within allowance
- [ ] Second rest day in week = 0%
- [ ] Workout rep volume calculated correctly
- [ ] All weights sum to 100% (check dashboard)

## Common Test Issues

**Issue:** Score seems too low
- Check if all metrics are logged (nulls = 0 score)
- Verify forgiveness margins are set
- Check if multiple rest days taken

**Issue:** Workout score is 0
- Verify exercises are saved with body parts
- Check body part targets are set in plan
- Ensure body part names match exactly

**Issue:** Charts not showing data
- Need at least 5-7 days of logs for meaningful charts
- Body metrics must be logged for weight-based reports
- Check date range selection

## Next Steps After Testing

1. ✅ Verify all core features work
2. 📝 Note any UI/UX improvements needed
3. 🐛 Fix any bugs discovered
4. 🎨 Refine styling and layout
5. 📸 Move to Phase 2 (screenshot processing)

## Sample API Calls (for direct testing)

**Create Plan:**
```json
POST http://localhost:8000/plans/?user_id=1
{
  "name": "Test Plan",
  "goal": "bulk",
  "start_date": "2024-11-11",
  "calorie_target": 3000,
  "calorie_margin_percent": 0.05,
  // ... rest of fields
}
```

**Create Log:**
```json
POST http://localhost:8000/logs/?user_id=1
{
  "date": "2024-11-11",
  "calories": 3050,
  "protein": 180,
  "workouts": [
    {
      "body_part": "chest",
      "exercise_name": "Bench Press",
      "sets": 4,
      "reps": 8
    }
  ]
}
```

Happy testing! 🎉
