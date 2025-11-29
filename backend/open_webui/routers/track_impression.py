from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# from ... import schemas, models, database
from backend.open_webui.utils.auth import get_current_user
from open_webui.internal.db import Base, get_db
from open_webui.models.analytics_event import AnalyticsEvent, AnalyticsEventResponse, AnalyticsEventCreate
router = APIRouter()

@router.post("/track", response_model=AnalyticsEventResponse, status_code=status.HTTP_201_CREATED)
async def track_event(event: AnalyticsEventCreate):
    with get_db() as db:
        db_event = AnalyticsEvent(**event.dict())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event