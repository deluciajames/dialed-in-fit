from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta

from app.database import get_db
from app.models import DailyLog as DailyLogModel, Workout as WorkoutModel, Plan as PlanModel
from app.schemas import DailyLog, DailyLogCreate, DailyLogUpdate
from app.core.scoring import calculate_daily_score

router = APIRouter(prefix="/logs", tags=["daily_logs"])


def calculate_rest_days_this_week(user_id: int, log_date: date, db: Session) -> int:
    """Calculate how many rest days have been used this week."""
    # Find start of week (Monday)
    days_since_monday = log_date.weekday()
    week_start = log_date - timedelta(days=days_since_monday)
    
    rest_days = db.query(DailyLogModel).filter(
        DailyLogModel.user_id == user_id,
        DailyLogModel.date >= week_start,
        DailyLogModel.date < log_date,
        DailyLogModel.is_rest_day == True
    ).count()
    
    return rest_days


@router.post("/", response_model=DailyLog)
def create_daily_log(log: DailyLogCreate, user_id: int, db: Session = Depends(get_db)):
    """Create a new daily log entry."""
    
    # Get active plan
    plan = db.query(PlanModel).filter(
        PlanModel.user_id == user_id,
        PlanModel.end_date == None
    ).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="No active plan found. Create a plan first.")
    
    # Check if log already exists for this date
    existing = db.query(DailyLogModel).filter(
        DailyLogModel.user_id == user_id,
        DailyLogModel.date == log.date
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Log already exists for this date")
    
    # Create daily log
    db_log = DailyLogModel(
        user_id=user_id,
        plan_id=plan.id,
        date=log.date,
        calories=log.calories,
        protein=log.protein,
        carbs=log.carbs,
        fat=log.fat,
        sleep_hours=log.sleep_hours,
        steps=log.steps,
        hydration_oz=log.hydration_oz,
        supplements_taken=log.supplements_taken,
        body_weight=log.body_weight,
        body_fat_percent=log.body_fat_percent,
        is_rest_day=log.is_rest_day
    )
    
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    
    # Add workouts
    for workout_data in log.workouts:
        total_reps = workout_data.sets * workout_data.reps
        workout = WorkoutModel(
            daily_log_id=db_log.id,
            body_part=workout_data.body_part,
            exercise_name=workout_data.exercise_name,
            sets=workout_data.sets,
            reps=workout_data.reps,
            weight=workout_data.weight,
            total_reps=total_reps
        )
        db.add(workout)
    
    db.commit()
    db.refresh(db_log)
    
    # Calculate scores
    rest_days_used = calculate_rest_days_this_week(user_id, log.date, db)
    scores = calculate_daily_score(db_log, plan, rest_days_used)
    
    # Update log with scores
    db_log.calorie_score = scores["calories"]
    db_log.protein_score = scores["protein"]
    db_log.carbs_score = scores["carbs"]
    db_log.fat_score = scores["fat"]
    db_log.workout_score = scores["workout"]
    db_log.sleep_score = scores["sleep"]
    db_log.steps_score = scores["steps"]
    db_log.supplements_score = scores["supplements"]
    db_log.hydration_score = scores["hydration"]
    db_log.total_score = scores["total"]
    
    db.commit()
    db.refresh(db_log)
    
    return db_log


@router.get("/", response_model=List[DailyLog])
def get_daily_logs(
    user_id: int,
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db)
):
    """Get daily logs for a user, optionally filtered by date range."""
    query = db.query(DailyLogModel).filter(DailyLogModel.user_id == user_id)
    
    if start_date:
        query = query.filter(DailyLogModel.date >= start_date)
    if end_date:
        query = query.filter(DailyLogModel.date <= end_date)
    
    logs = query.order_by(DailyLogModel.date.desc()).all()
    return logs


@router.get("/{log_id}", response_model=DailyLog)
def get_daily_log(log_id: int, user_id: int, db: Session = Depends(get_db)):
    """Get a specific daily log."""
    log = db.query(DailyLogModel).filter(
        DailyLogModel.id == log_id,
        DailyLogModel.user_id == user_id
    ).first()
    
    if not log:
        raise HTTPException(status_code=404, detail="Daily log not found")
    
    return log


@router.get("/date/{log_date}", response_model=DailyLog)
def get_daily_log_by_date(log_date: date, user_id: int, db: Session = Depends(get_db)):
    """Get a daily log by date."""
    log = db.query(DailyLogModel).filter(
        DailyLogModel.date == log_date,
        DailyLogModel.user_id == user_id
    ).first()
    
    if not log:
        raise HTTPException(status_code=404, detail="Daily log not found for this date")
    
    return log


@router.put("/{log_id}", response_model=DailyLog)
def update_daily_log(
    log_id: int,
    log_update: DailyLogUpdate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Update a daily log."""
    db_log = db.query(DailyLogModel).filter(
        DailyLogModel.id == log_id,
        DailyLogModel.user_id == user_id
    ).first()
    
    if not db_log:
        raise HTTPException(status_code=404, detail="Daily log not found")
    
    # Update basic fields
    for key, value in log_update.model_dump(exclude={"workouts"}).items():
        if value is not None:
            setattr(db_log, key, value)
    
    # Update workouts if provided
    if log_update.workouts is not None:
        # Delete existing workouts
        db.query(WorkoutModel).filter(WorkoutModel.daily_log_id == log_id).delete()
        
        # Add new workouts
        for workout_data in log_update.workouts:
            total_reps = workout_data.sets * workout_data.reps
            workout = WorkoutModel(
                daily_log_id=log_id,
                body_part=workout_data.body_part,
                exercise_name=workout_data.exercise_name,
                sets=workout_data.sets,
                reps=workout_data.reps,
                weight=workout_data.weight,
                total_reps=total_reps
            )
            db.add(workout)
    
    db.commit()
    db.refresh(db_log)
    
    # Recalculate scores
    plan = db.query(PlanModel).filter(PlanModel.id == db_log.plan_id).first()
    rest_days_used = calculate_rest_days_this_week(user_id, db_log.date, db)
    scores = calculate_daily_score(db_log, plan, rest_days_used)
    
    # Update scores
    db_log.calorie_score = scores["calories"]
    db_log.protein_score = scores["protein"]
    db_log.carbs_score = scores["carbs"]
    db_log.fat_score = scores["fat"]
    db_log.workout_score = scores["workout"]
    db_log.sleep_score = scores["sleep"]
    db_log.steps_score = scores["steps"]
    db_log.supplements_score = scores["supplements"]
    db_log.hydration_score = scores["hydration"]
    db_log.total_score = scores["total"]
    
    db.commit()
    db.refresh(db_log)
    
    return db_log


@router.delete("/{log_id}")
def delete_daily_log(log_id: int, user_id: int, db: Session = Depends(get_db)):
    """Delete a daily log."""
    db_log = db.query(DailyLogModel).filter(
        DailyLogModel.id == log_id,
        DailyLogModel.user_id == user_id
    ).first()
    
    if not db_log:
        raise HTTPException(status_code=404, detail="Daily log not found")
    
    db.delete(db_log)
    db.commit()
    
    return {"message": "Daily log deleted successfully"}
