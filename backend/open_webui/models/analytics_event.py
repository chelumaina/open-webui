from sqlalchemy import UUID, Column, Integer, String, JSON, DateTime, text
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from open_webui.internal.db import Base, get_db
# from uuid import uuid4
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, validator

class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    # id = Column(UUID, default=uuid4(), primary_key=True, index=True)
    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=text("TIMEZONE('utc', NOW())"), index=True)
    path = Column(String, index=True)
    full_url = Column(String)
    query = Column(JSONB, default=dict)
    user_agent = Column(String)
    viewport = Column(JSONB)
    screen = Column(JSONB)
    language = Column(String(10))
    referrer = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=text("TIMEZONE('utc', NOW())"))
    
    
class AnalyticsEventCreate(BaseModel):
    section_id: str
    timestamp: datetime
    path: str
    full_url: str
    query: Dict[str, Any] = Field(default_factory=dict)
    user_agent: str
    viewport: Dict[str, int]
    screen: Dict[str, int]
    language: str
    referrer: Optional[str] = None

    @validator("timestamp", pre=True)
    def parse_timestamp(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v

class AnalyticsEventResponse(AnalyticsEventCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True