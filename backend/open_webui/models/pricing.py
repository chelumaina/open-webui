# models/pricing.py
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from uuid import UUID

class PlanFeature(BaseModel):
    text: str
    enabled: bool = True          # useful to temporarily disable a feature
    coming_soon: bool = False     # optional: for upcoming features

class PricingPlan(BaseModel):
    id: Literal["basic", "enterprise", "enterprise_plus"]
    name: str
    tagline: str
    price: str                          # e.g. "$5" or "$59"
    period: Literal["month", "year"]
    amount: int                         # numeric value in cents or dollars
    currency: str = "USD"
    group_id: str
    highlighted: bool = False
    badge: Optional[str] = None         # "Most Popular", "Best Value", etc.

    features: List[PlanFeature]

    class Config:
        # Allows UUID to be serialized correctly
        json_encoders = {UUID: str}