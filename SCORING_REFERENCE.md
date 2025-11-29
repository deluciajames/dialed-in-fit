# 📊 Dialed In Score - Calculation Reference

## Overview
Your Dialed In Score is calculated daily on a **0-10 scale** based on 9 weighted metrics.

---

## Score Components & Weights

```
┌────────────────────────────────────────────────────┐
│           DIALED IN SCORE (0-10)                   │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │     DIET & EXERCISE (75%)                   │  │
│  │                                              │  │
│  │  Calories      ████████████████████  20%    │  │
│  │  Protein       ██████████            10%    │  │
│  │  Carbs         ██████████            10%    │  │
│  │  Fats          ██████████            10%    │  │
│  │  Workout Vol   █████████████████████ 25%    │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │     WELLNESS (25%)                          │  │
│  │                                              │  │
│  │  Sleep         ██████████            10%    │  │
│  │  Steps         █████                  5%    │  │
│  │  Supplements   █████                  5%    │  │
│  │  Hydration     █████                  5%    │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  Final Score = Σ(component_score × weight)         │
│              ÷ 10                                   │
└────────────────────────────────────────────────────┘
```

---

## Scoring Methods

### 1️⃣ Pyramid Scoring (Nutrition Metrics)

Used for: Calories, Protein, Carbs, Fat

**Formula:**
```
IF within forgiveness margin:
    score = 100

ELSE:
    penalty = |actual - target|
    score = max(0, (target - penalty) / target × 100)
```

**Forgiveness Margin (User-Defined 3-5%):**

**In BULK:**
- Can go OVER target by margin (eating more is okay)
- Example: 3000 cal target, 5% margin
  - 2850-3150 cal = 100% ✅
  - 2700 cal = 90% ⚠️
  - 3300 cal = 90% ⚠️

**In CUT:**
- Can go UNDER target by margin (eating less is okay)
- Example: 2500 cal target, 5% margin
  - 2375-2500 cal = 100% ✅
  - 2600 cal = 96% ⚠️
  - 2300 cal = 100% ✅

**Visual:**
```
        BULK                      CUT
Score                       Score
100%  ████████████████      100%  ████████████████
      │    Target   │             │  Target      │
      │←Margin→│←M→ │             │ ←M→│←Margin→ │
 80%  ▼         ▼    ▼        80%  ▼   ▼         ▼
      Under    Over              Under  Over
```

---

### 2️⃣ Percentage Scoring (Simple Metrics)

Used for: Sleep, Steps, Hydration

**Formula:**
```
score = min(100, (actual / target) × 100)
```

**Examples:**
- Sleep: 8 hrs actual / 8 hrs target = **100%**
- Sleep: 7 hrs actual / 8 hrs target = **87.5%**
- Steps: 7200 / 7000 target = **100%** (capped)
- Steps: 5000 / 7000 target = **71.4%**

---

### 3️⃣ Workout Volume Scoring

Used for: Workout reps

**Formula:**
```
For each body part trained:
    daily_target = weekly_target / training_days_per_week
    score = (actual_reps / daily_target) × 100

workout_score = average(all body parts trained that day)
```

**Example:**
- Plan: Chest 120 reps/week, 6 training days
- Daily target: 120 / 6 = 20 reps
- Actual: Logged 62 reps for chest
- Score: 62 / 20 × 100 = **310%** → capped at **100%** ✅

**Rest Days:**
```
IF is_rest_day AND rest_days_used <= allowed:
    workout_score = 100%  ✅

ELSE IF is_rest_day AND rest_days_used > allowed:
    workout_score = 0%    ❌

ELSE IF no workouts logged:
    workout_score = 0%    ❌
```

---

### 4️⃣ Supplement Adherence

Used for: Supplements

**Formula:**
```
score = (supplements_taken / supplements_planned) × 100
```

**Example:**
- Planned: [Creatine, Vitamin D, Protein]
- Taken: [Creatine, Protein]
- Score: 2/3 × 100 = **66.7%**

---

## Score Aggregation

### Step 1: Calculate Component Scores (0-100 each)

```python
component_scores = {
    'calories': 95,      # Slightly under target
    'protein': 100,      # Perfect
    'carbs': 88,         # Bit low
    'fat': 100,          # Perfect
    'workout': 100,      # Hit volume target
    'sleep': 87.5,       # 7 hrs / 8 hrs target
    'steps': 71.4,       # 5000 / 7000 target
    'supplements': 100,  # All taken
    'hydration': 90      # 90 oz / 100 oz target
}
```

### Step 2: Apply Weights

```python
weighted_scores = {
    'calories': 95 × 0.20 = 19.0
    'protein': 100 × 0.10 = 10.0
    'carbs': 88 × 0.10 = 8.8
    'fat': 100 × 0.10 = 10.0
    'workout': 100 × 0.25 = 25.0
    'sleep': 87.5 × 0.10 = 8.75
    'steps': 71.4 × 0.05 = 3.57
    'supplements': 100 × 0.05 = 5.0
    'hydration': 90 × 0.05 = 4.5
}
```

### Step 3: Sum and Convert to 0-10 Scale

```python
total = sum(weighted_scores) = 94.62

final_score = total / 10 = 9.46 / 10 ✅
```

**Result: 9.5/10 - Dialed In! 🟢**

---

## Color Coding

```
🔴 RED (<7.0): Needs Work
   - Missing major metrics
   - Far from targets
   - Action needed

🟡 YELLOW (7.0-8.4): Good
   - Most metrics hit
   - Minor improvements needed
   - On track

🟢 GREEN (8.5+): Dialed In!
   - Crushing it
   - All major metrics hit
   - Keep it up!
```

---

## Example Score Scenarios

### 💯 Perfect Day (10.0/10)

```
Calories: 3000/3000 = 100%
Protein: 180/180g = 100%
Carbs: 350/350g = 100%
Fat: 80/80g = 100%
Workout: 120/120 reps = 100%
Sleep: 8/8 hrs = 100%
Steps: 7500/7000 = 100%
Supplements: 3/3 = 100%
Hydration: 100/100 oz = 100%

Score: 10.0/10 🟢
```

### 👍 Good Day (8.2/10)

```
Calories: 2950/3000 = 98%
Protein: 175/180g = 97%
Carbs: 330/350g = 94%
Fat: 75/80g = 94%
Workout: 110/120 reps = 92%
Sleep: 7/8 hrs = 87.5%
Steps: 6000/7000 = 86%
Supplements: 2/3 = 67%
Hydration: 85/100 oz = 85%

Score: 8.2/10 🟡
```

### ⚠️ Rough Day (5.5/10)

```
Calories: 2500/3000 = 83%
Protein: 150/180g = 83%
Carbs: 280/350g = 80%
Fat: 65/80g = 81%
Workout: 0 reps = 0% (missed gym)
Sleep: 6/8 hrs = 75%
Steps: 4000/7000 = 57%
Supplements: 0/3 = 0%
Hydration: 60/100 oz = 60%

Score: 5.5/10 🔴
```

---

## Tips for Maximizing Score

### Priority 1 (Biggest Impact - 45%)
✅ Hit calorie target (20%)
✅ Complete workout volume (25%)

### Priority 2 (Medium Impact - 30%)
✅ Hit protein target (10%)
✅ Get enough sleep (10%)
✅ Hit carb target (10%)

### Priority 3 (Fine-Tuning - 25%)
✅ Hit fat target (10%)
✅ Get steps in (5%)
✅ Take supplements (5%)
✅ Drink enough water (5%)

**Strategy:**
1. Never skip workouts (huge penalty)
2. Hit protein and calories (big wins)
3. Get 7.5+ hours sleep (easy points)
4. Let the small stuff (steps, water) add up

---

## Technical Implementation

**Location:** `backend/app/core/scoring.py`

**Key Functions:**
- `calculate_pyramid_score()` - Nutrition with margins
- `calculate_percentage_score()` - Simple metrics
- `calculate_workout_score()` - Volume tracking
- `calculate_daily_score()` - Main aggregation
- `calculate_rolling_score()` - Multi-day average

**Cached in Database:**
All component scores are saved in `daily_logs` table for fast dashboard loading.

---

## Formula Summary Card

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  DIALED IN SCORE FORMULA                ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│                                          │
│  Score = (                               │
│    calories_score × 0.20 +               │
│    protein_score × 0.10 +                │
│    carbs_score × 0.10 +                  │
│    fat_score × 0.10 +                    │
│    workout_score × 0.25 +                │
│    sleep_score × 0.10 +                  │
│    steps_score × 0.05 +                  │
│    supplements_score × 0.05 +            │
│    hydration_score × 0.05                │
│  ) ÷ 10                                  │
│                                          │
│  Where each component_score is 0-100    │
│  Final score is 0-10                    │
│                                          │
└──────────────────────────────────────────┘
```

---

**Remember:** The score is YOUR accountability tool. It's not about perfection every day - it's about consistency over time. A 7-8 average over months beats sporadic 10s with lots of 3s.

**Aim for:** 85%+ of days above 7.0 🎯
