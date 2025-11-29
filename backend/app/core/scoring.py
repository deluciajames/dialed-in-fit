"""
Dialed In Score Calculation Engine

Calculates the overall "Dialed In" score based on multiple metrics.
Score is from 0-10, weighted across diet, exercise, and wellness.
"""

from typing import Dict, Optional
from app.models.models import Plan, DailyLog, GoalType


# Score weights (total = 100%)
WEIGHTS = {
    "calories": 0.20,
    "protein": 0.10,
    "carbs": 0.10,
    "fat": 0.10,
    "workout": 0.25,
    "sleep": 0.10,
    "steps": 0.05,
    "supplements": 0.05,
    "hydration": 0.05,
}


def calculate_pyramid_score(
    actual: float,
    target: float,
    margin_percent: float,
    goal: GoalType,
    metric_type: str = "nutrition"
) -> float:
    """
    Calculate score with forgiveness margin and pyramid penalty.
    
    Args:
        actual: Actual value achieved
        target: Target value from plan
        margin_percent: Forgiveness margin (0.03 = 3%, 0.05 = 5%)
        goal: Bulk, Cut, or Maintain
        metric_type: "nutrition" or other (affects margin direction)
    
    Returns:
        Score from 0-100
    """
    if target == 0:
        return 100.0 if actual == 0 else 0.0
    
    # Calculate forgiveness boundaries
    if metric_type == "nutrition":
        if goal == GoalType.BULK:
            # In bulk, forgiveness is on the high side (can go over)
            favorable_boundary = target * (1 + margin_percent)
            unfavorable_boundary = target * (1 - margin_percent)
        elif goal == GoalType.CUT:
            # In cut, forgiveness is on the low side (can go under)
            favorable_boundary = target * (1 - margin_percent)
            unfavorable_boundary = target * (1 + margin_percent)
        else:  # MAINTAIN
            # Symmetric forgiveness
            favorable_boundary = target * (1 + margin_percent)
            unfavorable_boundary = target * (1 - margin_percent)
    else:
        # For non-nutrition metrics (like steps), symmetric forgiveness
        favorable_boundary = target * (1 + margin_percent)
        unfavorable_boundary = target * (1 - margin_percent)
    
    # Check if within forgiveness margin
    if goal == GoalType.BULK and metric_type == "nutrition":
        if unfavorable_boundary <= actual <= favorable_boundary:
            return 100.0
    elif goal == GoalType.CUT and metric_type == "nutrition":
        if favorable_boundary <= actual <= unfavorable_boundary:
            return 100.0
    else:
        if min(favorable_boundary, unfavorable_boundary) <= actual <= max(favorable_boundary, unfavorable_boundary):
            return 100.0
    
    # Outside margin - apply pyramid penalty
    # Score = max(0, (target - abs(actual - target)) / target) * 100
    penalty = abs(actual - target)
    score = max(0, (target - penalty) / target) * 100
    
    return score


def calculate_percentage_score(actual: float, target: float) -> float:
    """
    Simple percentage calculation for metrics like steps, sleep.
    Caps at 100% (no bonus for exceeding).
    
    Returns:
        Score from 0-100
    """
    if target == 0:
        return 100.0 if actual == 0 else 0.0
    
    score = (actual / target) * 100
    return min(score, 100.0)  # Cap at 100%


def calculate_workout_score(
    daily_log: DailyLog,
    plan: Plan,
    rest_days_used_this_week: int
) -> float:
    """
    Calculate workout score based on rep volume per body part.
    
    Args:
        daily_log: The daily log with workouts
        plan: The active plan with targets
        rest_days_used_this_week: Number of rest days already taken this week
    
    Returns:
        Score from 0-100
    """
    # If it's a rest day
    if daily_log.is_rest_day:
        allowed_rest_days = 7 - plan.training_days_per_week
        if rest_days_used_this_week <= allowed_rest_days:
            return 100.0  # Planned rest day
        else:
            return 0.0  # Extra unplanned rest day
    
    # If no workouts logged, score is 0
    if not daily_log.workouts:
        return 0.0
    
    # Calculate total reps per body part
    body_part_reps = {}
    for workout in daily_log.workouts:
        body_part = workout.body_part.lower()
        reps = workout.total_reps
        body_part_reps[body_part] = body_part_reps.get(body_part, 0) + reps
    
    # Get targets from plan
    targets = plan.body_part_targets or {}
    
    # Calculate score for each body part trained
    scores = []
    for body_part, actual_reps in body_part_reps.items():
        target_reps = targets.get(body_part, 0)
        if target_reps > 0:
            # Weekly target, but we score daily progress
            # Assume even distribution across training days
            daily_target = target_reps / plan.training_days_per_week
            score = calculate_percentage_score(actual_reps, daily_target)
            scores.append(score)
    
    # Average score across all body parts trained
    if scores:
        return sum(scores) / len(scores)
    else:
        return 0.0


def calculate_supplements_score(
    supplements_taken: Optional[list],
    supplements_planned: Optional[list]
) -> float:
    """
    Calculate supplement adherence score.
    
    Returns:
        Score from 0-100
    """
    if not supplements_planned or len(supplements_planned) == 0:
        return 100.0  # No supplements planned = perfect score
    
    if not supplements_taken:
        return 0.0  # Planned supplements but took none
    
    # Count how many planned supplements were taken
    taken_count = sum(1 for supp in supplements_planned if supp in supplements_taken)
    score = (taken_count / len(supplements_planned)) * 100
    
    return score


def calculate_daily_score(
    daily_log: DailyLog,
    plan: Plan,
    rest_days_used_this_week: int = 0
) -> Dict[str, float]:
    """
    Calculate all component scores and total "Dialed In" score for a daily log.
    
    Args:
        daily_log: The daily log to score
        plan: The active plan with targets
        rest_days_used_this_week: How many rest days already used this week
    
    Returns:
        Dictionary with all component scores and total score
    """
    scores = {}
    
    # Nutrition scores
    if daily_log.calories is not None:
        scores["calories"] = calculate_pyramid_score(
            daily_log.calories,
            plan.calorie_target,
            plan.calorie_margin_percent,
            plan.goal,
            "nutrition"
        )
    else:
        scores["calories"] = 0.0
    
    if daily_log.protein is not None:
        scores["protein"] = calculate_pyramid_score(
            daily_log.protein,
            plan.protein_target,
            plan.protein_margin_percent,
            plan.goal,
            "nutrition"
        )
    else:
        scores["protein"] = 0.0
    
    if daily_log.carbs is not None:
        scores["carbs"] = calculate_pyramid_score(
            daily_log.carbs,
            plan.carbs_target,
            plan.carbs_margin_percent,
            plan.goal,
            "nutrition"
        )
    else:
        scores["carbs"] = 0.0
    
    if daily_log.fat is not None:
        scores["fat"] = calculate_pyramid_score(
            daily_log.fat,
            plan.fat_target,
            plan.fat_margin_percent,
            plan.goal,
            "nutrition"
        )
    else:
        scores["fat"] = 0.0
    
    # Workout score
    scores["workout"] = calculate_workout_score(daily_log, plan, rest_days_used_this_week)
    
    # Wellness scores
    if daily_log.sleep_hours is not None:
        scores["sleep"] = calculate_percentage_score(
            daily_log.sleep_hours,
            plan.sleep_target_hours
        )
    else:
        scores["sleep"] = 0.0
    
    if daily_log.steps is not None:
        scores["steps"] = calculate_percentage_score(
            daily_log.steps,
            plan.steps_target
        )
    else:
        scores["steps"] = 0.0
    
    if daily_log.hydration_oz is not None:
        scores["hydration"] = calculate_percentage_score(
            daily_log.hydration_oz,
            plan.hydration_target_oz
        )
    else:
        scores["hydration"] = 0.0
    
    scores["supplements"] = calculate_supplements_score(
        daily_log.supplements_taken,
        plan.supplements
    )
    
    # Calculate weighted total score (0-100 scale)
    total = sum(scores[metric] * WEIGHTS[metric] for metric in WEIGHTS.keys())
    
    # Convert to 0-10 scale
    scores["total"] = total / 10
    
    return scores


def calculate_rolling_score(daily_logs: list[DailyLog], plan: Plan) -> float:
    """
    Calculate average "Dialed In" score across multiple days.
    
    Args:
        daily_logs: List of daily logs to average
        plan: The active plan
    
    Returns:
        Average score from 0-10
    """
    if not daily_logs:
        return 0.0
    
    total_scores = []
    
    for log in daily_logs:
        # For each log, calculate its score
        # Note: We'd need to properly track rest days per week here
        # For now, simplified version
        scores = calculate_daily_score(log, plan, rest_days_used_this_week=0)
        total_scores.append(scores["total"])
    
    return sum(total_scores) / len(total_scores)
