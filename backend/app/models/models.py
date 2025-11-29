from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import date
import enum
from app.database import Base


class GoalType(str, enum.Enum):
    BULK = "bulk"
    CUT = "cut"
    MAINTAIN = "maintain"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    # Relationships
    plans = relationship("Plan", back_populates="user")
    daily_logs = relationship("DailyLog", back_populates="user")


class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Plan details
    name = Column(String)  # e.g., "Winter Bulk 2025"
    goal = Column(SQLEnum(GoalType))
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)  # null = current active plan
    
    # Nutrition targets
    calorie_target = Column(Integer)
    calorie_margin_percent = Column(Float)  # 3-5% forgiveness
    protein_target = Column(Integer)
    protein_margin_percent = Column(Float)
    carbs_target = Column(Integer)
    carbs_margin_percent = Column(Float)
    fat_target = Column(Integer)
    fat_margin_percent = Column(Float)
    
    # Training targets
    training_days_per_week = Column(Integer)  # e.g., 6 means 1 rest day allowed
    body_part_targets = Column(JSON)  # {"chest": 120, "back": 120, "legs": 120, ...}
    
    # Wellness targets
    sleep_target_hours = Column(Float)  # e.g., 8.0
    steps_target = Column(Integer)  # e.g., 7000
    hydration_target_oz = Column(Float)  # e.g., 100
    supplements = Column(JSON)  # ["Creatine", "Vitamin D", "Protein Powder"]
    
    # Relationships
    user = relationship("User", back_populates="plans")
    daily_logs = relationship("DailyLog", back_populates="plan")


class DailyLog(Base):
    __tablename__ = "daily_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_id = Column(Integer, ForeignKey("plans.id"))
    date = Column(Date, index=True)
    
    # Nutrition actuals
    calories = Column(Integer, nullable=True)
    protein = Column(Integer, nullable=True)
    carbs = Column(Integer, nullable=True)
    fat = Column(Integer, nullable=True)
    
    # Wellness actuals
    sleep_hours = Column(Float, nullable=True)
    steps = Column(Integer, nullable=True)
    hydration_oz = Column(Float, nullable=True)
    supplements_taken = Column(JSON, nullable=True)  # List of supplement names taken
    
    # Body metrics (optional - for correlation reports)
    body_weight = Column(Float, nullable=True)
    body_fat_percent = Column(Float, nullable=True)
    
    # Is this a rest day?
    is_rest_day = Column(Boolean, default=False)
    
    # Calculated scores (cached for performance)
    calorie_score = Column(Float, nullable=True)
    protein_score = Column(Float, nullable=True)
    carbs_score = Column(Float, nullable=True)
    fat_score = Column(Float, nullable=True)
    workout_score = Column(Float, nullable=True)
    sleep_score = Column(Float, nullable=True)
    steps_score = Column(Float, nullable=True)
    supplements_score = Column(Float, nullable=True)
    hydration_score = Column(Float, nullable=True)
    total_score = Column(Float, nullable=True)  # Final "Dialed In" score (0-10)
    
    # Relationships
    user = relationship("User", back_populates="daily_logs")
    plan = relationship("Plan", back_populates="daily_logs")
    workouts = relationship("Workout", back_populates="daily_log", cascade="all, delete-orphan")


class Workout(Base):
    __tablename__ = "workouts"
    
    id = Column(Integer, primary_key=True, index=True)
    daily_log_id = Column(Integer, ForeignKey("daily_logs.id"))
    
    # Workout details
    body_part = Column(String)  # e.g., "chest", "back", "legs"
    exercise_name = Column(String)  # e.g., "Bench Press"
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float, nullable=True)  # Optional weight tracking
    
    # Total reps for this exercise
    total_reps = Column(Integer)  # sets * reps (calculated)
    
    # Relationships
    daily_log = relationship("DailyLog", back_populates="workouts")
