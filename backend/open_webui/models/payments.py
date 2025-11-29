
import time, uuid
from typing import Optional
from datetime import datetime

from open_webui.internal.db import Base, get_db


from pydantic import BaseModel, Field
from sqlalchemy import UUID, Column, DateTime, Integer, String, Float, Text
from sqlalchemy.orm import  Mapped, mapped_column
from sqlalchemy import or_

# import datetime

####################
# User DB Schema
####################


class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    reference = Column(String, unique=True, index=True, nullable=False)
    amount = Column(Float, nullable=False)  # Amount in original currency
    currency = Column(String, default="USD", nullable=False)
    plan_id = Column(String, nullable=False)
    plan_name = Column(String, nullable=False)
    billing_cycle = Column(String, default="monthly")  # monthly, yearly
    status = Column(String, default="pending")  # pending, success, failed, cancelled
    paystack_reference = Column(String, nullable=True)
    paystack_status = Column(String, nullable=True)
    gateway_response = Column(Text, nullable=True, default="{}")
    gateway_response_data = Column(Text, nullable=True) 
    group_id = Column(String, nullable=True)   
    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<PaymentTransaction(id={self.id}, user_id={self.user_id}, amount={self.amount}, currency={self.currency}, status={self.status})>"
    

class UserSubscription(Base):
    __tablename__ = "user_subscriptions"

    id = Column(Integer,default=uuid.uuid4(), primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    plan_id = Column(String, nullable=False)
    plan_name = Column(String, nullable=False)
    status = Column(String, default="active")  # active, cancelled, expired
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD", nullable=False)
    group_id = Column(String, nullable=True)
    billing_cycle = Column(String, default="monthly")  # monthly, yearly
    started_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    # current_period_end = Column(DateTime, nullable=True)
    trial_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    current_period_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    transaction_reference = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # plan_interval: Mapped[str] = mapped_column(String(16))   # 'monthly' | 'yearly' | etc.
    # status: Mapped[str] = mapped_column(String(32))          # 'active' | 'trialing' | 'canceled' | ...
    # trial_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    # current_period_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # __table_args__ = (
    #     Index("ix_user_subscriptions_lookup", "user_id", "plan_interval", "status"),
    # )
    


# Pydantic models
class PaymentInitializeRequest(BaseModel):
    amount: float = Field(..., description="Amount in the specified currency")
    currency: str = Field(default="USD", description="Currency code")
    group_id: Optional[str] = Field(None, description="Group identifier")
    plan_id: str = Field(..., description="Plan identifier")
    plan_name: str = Field(..., description="Plan name")
    callback_url: Optional[str] = Field(None, description="Callback URL")

class UserSubscriptionResponse(BaseModel):
    id: int
    user_id: str
    plan_id: str
    plan_name: str
    status: str
    amount: float
    currency: str
    group_id: Optional[str]
    billing_cycle: str
    started_at: datetime
    expires_at: Optional[datetime]
    trial_end: Optional[datetime]
    current_period_end: Optional[datetime]
    transaction_reference: str
    created_at: datetime
    updated_at: datetime
    
class PaymentTransactionResponse(BaseModel):
    id: int
    user_id: str
    reference: str
    amount: float
    currency: str
    plan_id: str     
    plan_name: str
    billing_cycle: str
    status: str
    paystack_reference: Optional[str]
    paystack_status: Optional[str]
    gateway_response: Optional[str]
    gateway_response_data: Optional[str]
    group_id: Optional[str]
    paid_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime       

class PaymentInitializeResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


class PaymentVerifyResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


class WebhookPayload(BaseModel):
    event: str
    data: dict

class PaymentsTable:
    def get_user_subscription(self, user_id: str) -> Optional[UserSubscriptionResponse]:
        with get_db() as db:
            subscription = (
                db.query(UserSubscription)
                .filter_by(user_id=user_id)
                .order_by(UserSubscription.expires_at.desc())
                .first()
            )
            if subscription:
                return subscription
            else:
                 return None
             

Payments = PaymentsTable()