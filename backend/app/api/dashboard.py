from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List

from app.database import get_db
from app.models import DailyLog as DailyLogModel, Plan as PlanModel
from app.schemas import DashboardResponse, ScoreBreakdown

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/", response_model=DashboardResponse)
def get_dashboard(
    user_id: int,
    period: str = Query("7d", regex="^(7d|30d|90d|ytd)$"),
    db: Session = Depends(get_db)
):
    """
    Get dashboard data with current score and period average.
    
    Args:
        user_id: User ID
        period: Time period - 7d, 30d, 90d, or ytd
    """
    
    # Get active plan
    plan = db.query(PlanModel).filter(
        PlanModel.user_id == user_id,
        PlanModel.end_date == None
    ).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="No active plan found")
    
    # Calculate date range based on period
    today = date.today()
    if period == "7d":
        start_date = today - timedelta(days=7)
    elif period == "30d":
        start_date = today - timedelta(days=30)
    elif period == "90d":
        start_date = today - timedelta(days=90)
    elif period == "ytd":
        start_date = date(today.year, 1, 1)
    else:
        start_date = today - timedelta(days=7)
    
    # Get logs for the period
    logs = db.query(DailyLogModel).filter(
        DailyLogModel.user_id == user_id,
        DailyLogModel.date >= start_date,
        DailyLogModel.date <= today
    ).order_by(DailyLogModel.date.asc()).all()
    
    if not logs:
        # No data - return zeros
        return DashboardResponse(
            current_score=0.0,
            period_average=0.0,
            score_breakdown=ScoreBreakdown(
                calories=0, protein=0, carbs=0, fat=0,
                workout=0, sleep=0, steps=0,
                supplements=0, hydration=0, total=0
            ),
            daily_scores=[]
        )
    
    # Get today's log if it exists
    today_log = next((log for log in logs if log.date == today), None)
    
    if today_log:
        current_score = today_log.total_score or 0.0
        score_breakdown = ScoreBreakdown(
            calories=today_log.calorie_score or 0,
            protein=today_log.protein_score or 0,
            carbs=today_log.carbs_score or 0,
            fat=today_log.fat_score or 0,
            workout=today_log.workout_score or 0,
            sleep=today_log.sleep_score or 0,
            steps=today_log.steps_score or 0,
            supplements=today_log.supplements_score or 0,
            hydration=today_log.hydration_score or 0,
            total=today_log.total_score or 0
        )
    else:
        current_score = 0.0
        score_breakdown = ScoreBreakdown(
            calories=0, protein=0, carbs=0, fat=0,
            workout=0, sleep=0, steps=0,
            supplements=0, hydration=0, total=0
        )
    
    # Calculate period average
    valid_scores = [log.total_score for log in logs if log.total_score is not None]
    period_average = sum(valid_scores) / len(valid_scores) if valid_scores else 0.0
    
    # Build daily scores list for chart
    daily_scores = [
        {
            "date": log.date.isoformat(),
            "score": log.total_score or 0.0
        }
        for log in logs
    ]
    
    return DashboardResponse(
        current_score=current_score,
        period_average=period_average,
        score_breakdown=score_breakdown,
        daily_scores=daily_scores
    )


@router.get("/score-color")
def get_score_color(score: float):
    """Get color code for a given score."""
    if score < 7.0:
        return {"color": "red", "label": "Needs Work"}
    elif score < 8.5:
        return {"color": "yellow", "label": "Good"}
    else:
        return {"color": "green", "label": "Dialed In"}
