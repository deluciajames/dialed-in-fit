from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.database import get_db
from app.models import Plan as PlanModel
from app.schemas import Plan, PlanCreate, PlanUpdate

router = APIRouter(prefix="/plans", tags=["plans"])


@router.post("/", response_model=Plan)
def create_plan(plan: PlanCreate, user_id: int, db: Session = Depends(get_db)):
    """Create a new plan for a user."""
    
    # End any currently active plans for this user
    active_plans = db.query(PlanModel).filter(
        PlanModel.user_id == user_id,
        PlanModel.end_date == None
    ).all()
    
    for active_plan in active_plans:
        active_plan.end_date = date.today()
    
    # Create new plan
    db_plan = PlanModel(
        user_id=user_id,
        **plan.model_dump()
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    
    return db_plan


@router.get("/", response_model=List[Plan])
def get_plans(user_id: int, db: Session = Depends(get_db)):
    """Get all plans for a user."""
    plans = db.query(PlanModel).filter(PlanModel.user_id == user_id).all()
    return plans


@router.get("/active", response_model=Plan)
def get_active_plan(user_id: int, db: Session = Depends(get_db)):
    """Get the currently active plan for a user."""
    plan = db.query(PlanModel).filter(
        PlanModel.user_id == user_id,
        PlanModel.end_date == None
    ).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="No active plan found")
    
    return plan


@router.get("/{plan_id}", response_model=Plan)
def get_plan(plan_id: int, user_id: int, db: Session = Depends(get_db)):
    """Get a specific plan."""
    plan = db.query(PlanModel).filter(
        PlanModel.id == plan_id,
        PlanModel.user_id == user_id
    ).first()
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    return plan


@router.put("/{plan_id}", response_model=Plan)
def update_plan(plan_id: int, plan_update: PlanUpdate, user_id: int, db: Session = Depends(get_db)):
    """Update a plan."""
    db_plan = db.query(PlanModel).filter(
        PlanModel.id == plan_id,
        PlanModel.user_id == user_id
    ).first()
    
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    for key, value in plan_update.model_dump().items():
        setattr(db_plan, key, value)
    
    db.commit()
    db.refresh(db_plan)
    
    return db_plan


@router.delete("/{plan_id}")
def delete_plan(plan_id: int, user_id: int, db: Session = Depends(get_db)):
    """Delete a plan."""
    db_plan = db.query(PlanModel).filter(
        PlanModel.id == plan_id,
        PlanModel.user_id == user_id
    ).first()
    
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    db.delete(db_plan)
    db.commit()
    
    return {"message": "Plan deleted successfully"}
