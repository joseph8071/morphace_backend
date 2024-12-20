from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from typing import List
from app.db import get_db
from app.models.user import User
from app.models.habits import UserHabits, HabitSkincareProducts
from app.models.products import SkincareProducts
from app.schemas.habits import HabitCreate, HabitResponse

router = APIRouter(prefix="/users/{user_id}/habits", tags=["Habits"])

@router.post("/", response_model=HabitResponse)
def create_user_habit(user_id: str, habit_data: HabitCreate, db: Session = Depends(get_db)):
    # Validate User
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user UUID")

    user = db.query(User).filter(User.id == user_uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_habit = UserHabits(
        user_id=user_uuid,
        timestamp=habit_data.timestamp,
        sleep_hours=habit_data.sleep_hours,
        used_spf=habit_data.used_spf
    )
    db.add(new_habit)
    db.flush()  # get new_habit.id

    # Link products
    used_products = []
    if habit_data.skincare_products:
        for identifier in habit_data.skincare_products:
            product = db.query(SkincareProducts).filter(SkincareProducts.identifier == identifier).first()
            if not product:
                # Optionally, create product on-the-fly or raise error
                raise HTTPException(status_code=400, detail=f"Product {identifier} not found")
            link = HabitSkincareProducts(user_habit_id=new_habit.id, product_id=product.id)
            db.add(link)
            used_products.append(identifier)

    db.commit()
    db.refresh(new_habit)

    return HabitResponse(
        id=new_habit.id,
        timestamp=new_habit.timestamp,
        sleep_hours=new_habit.sleep_hours,
        used_spf=new_habit.used_spf,
        skincare_products=used_products
    )

@router.get("/", response_model=List[HabitResponse])
def get_user_habits(user_id: str, start: datetime, end: datetime, db: Session = Depends(get_db)):
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user UUID")

    user = db.query(User).filter(User.id == user_uuid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    habits_query = db.query(UserHabits).filter(
        UserHabits.user_id == user_uuid,
        UserHabits.timestamp >= start,
        UserHabits.timestamp <= end
    ).order_by(UserHabits.timestamp)

    results = []
    for habit in habits_query.all():
        product_links = db.query(HabitSkincareProducts).filter_by(user_habit_id=habit.id).all()
        product_ids = [pl.product_id for pl in product_links]
        products = db.query(SkincareProducts).filter(SkincareProducts.id.in_(product_ids)).all()
        product_identifiers = [p.identifier for p in products]

        results.append(HabitResponse(
            id=habit.id,
            timestamp=habit.timestamp,
            sleep_hours=habit.sleep_hours,
            used_spf=habit.used_spf,
            skincare_products=product_identifiers
        ))

    return results
