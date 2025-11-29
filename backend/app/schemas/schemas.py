from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, Dict, List
from app.models.models import GoalType


# Plan schemas
class PlanBase(BaseModel):
    name: str
    goal: GoalType
    start_date: date
    
    # Nutrition targets
    calorie_target: int
    calorie_margin_percent: float = Field(ge=0.03, le=0.05)
    protein_target: int
    protein_margin_percent: float = Field(ge=0.03, le=0.05)
    carbs_target: int
    carbs_margin_percent: float = Field(ge=0.03, le=0.05)
    fat_target: int
    fat_margin_percent: float = Field(ge=0.03, le=0.05)
    
    # Training targets
    training_days_per_week: int = Field(ge=1, le=7)
    body_part_targets: Dict[str, int]  # {"chest": 120, "back": 120, ...}
    
    # Wellness targets
    sleep_target_hours: float
    steps_target: int
    hydration_target_oz: float
    supplements: List[str] = []


class PlanCreate(PlanBase):
    pass


class PlanUpdate(PlanBase):
    pass


class Plan(PlanBase):
    id: int
    user_id: int
    end_date: Optional[date] = None
    
    class Config:
        from_attributes = True


# Workout schemas
class WorkoutBase(BaseModel):
    body_part: str
    exercise_name: str
    sets: int
    reps: int
    weight: Optional[float] = None


class WorkoutCreate(WorkoutBase):
    pass


class Workout(WorkoutBase):
    id: int
    daily_log_id: int
    total_reps: int
    
    class Config:
        from_attributes = True


# Daily Log schemas
class DailyLogBase(BaseModel):
    date: date
    
    # Nutrition
    calories: Optional[int] = None
    protein: Optional[int] = None
    carbs: Optional[int] = None
    fat: Optional[int] = None
    
    # Wellness
    sleep_hours: Optional[float] = None
    steps: Optional[int] = None
    hydration_oz: Optional[float] = None
    supplements_taken: Optional[List[str]] = None
    
    # Body metrics
    body_weight: Optional[float] = None
    body_fat_percent: Optional[float] = None
    
    # Rest day flag
    is_rest_day: bool = False


class DailyLogCreate(DailyLogBase):
    workouts: List[WorkoutCreate] = []


class DailyLogUpdate(DailyLogBase):
    workouts: Optional[List[WorkoutCreate]] = None


class DailyLog(DailyLogBase):
    id: int
    user_id: int
    plan_id: int
    workouts: List[Workout] = []
    
    # Scores
    calorie_score: Optional[float] = None
    protein_score: Optional[float] = None
    carbs_score: Optional[float] = None
    fat_score: Optional[float] = None
    workout_score: Optional[float] = None
    sleep_score: Optional[float] = None
    steps_score: Optional[float] = None
    supplements_score: Optional[float] = None
    hydration_score: Optional[float] = None
    total_score: Optional[float] = None
    
    class Config:
        from_attributes = True


# Score response schema
class ScoreBreakdown(BaseModel):
    calories: float
    protein: float
    carbs: float
    fat: float
    workout: float
    sleep: float
    steps: float
    supplements: float
    hydration: float
    total: float  # 0-10 scale


class DashboardResponse(BaseModel):
    current_score: float  # 0-10 scale
    period_average: float  # 0-10 scale for selected time period
    score_breakdown: ScoreBreakdown
    daily_scores: List[Dict[str, any]]  # List of {date, score} for chart


# User schemas
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True
