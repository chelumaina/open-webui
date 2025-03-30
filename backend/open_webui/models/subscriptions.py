import json
import logging
import time
from typing import Optional
import uuid

from datetime import datetime
from enum import Enum
from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey,
    Float, DateTime, JSON, Enum as SQLAlchemyEnum
)
from pydantic import BaseModel, ConfigDict

from sqlalchemy.orm import relationship
from open_webui.internal.db import Base, get_db
from open_webui.env import SRC_LOG_LEVELS

from open_webui.models.users import UserModel, Users

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

class PaymentMethodType(str, Enum):
    CARD = "card"
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"

class TransactionStatus(str, Enum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REFUNDED = "refunded"

class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    CANCELED = "canceled"
    PAST_DUE = "past_due"
    UNPAID = "unpaid"

class PlanInterval(str, Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"


    # Relationships
    subscriptions = relationship("Subscription", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    payment_methods = relationship("PaymentMethod", back_populates="user")





class Plan(Base):
    __tablename__ = "plans" 
    id = Column(Integer, primary_key=True, index=True)
    stripe_price_id = Column(String)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    interval = Column(SQLAlchemyEnum(PlanInterval))
    features = Column(JSON)  # {"tokens": 1000, "api_calls": 5000}
    is_active = Column(Boolean, default=True)

class PlanModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str 
    name: str
    description: str
    price: float
    interval: PlanInterval
    features: dict
    is_active: bool
    stripe_price_id: str
    created_at: int  # timestamp in epoch
    updated_at: int  # timestamp in epoch


####################
# Forms
####################


class PlanResponse(BaseModel):
    id: str
    id: str 
    name: str
    description: str
    price: float
    interval: PlanInterval
    features: dict
    is_active: bool
    stripe_price_id: str
    created_at: int  # timestamp in epoch
    updated_at: int  # timestamp in epoch


class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    stripe_invoice_id = Column(String)
    amount_paid = Column(Float)
    currency = Column(String)
    pdf_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    subscription = relationship("Subscription", back_populates="invoices")
    transaction = relationship("Transaction", back_populates="invoice")

class InvoiceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    subscription_id: str
    transaction_id: str
    stripe_invoice_id: str
    amount_paid: float
    currency: str
    pdf_url: str
    created_at: int  # timestamp in epoch
    # subscription: SubscriptionModel
    # transaction: TransactionModel
    user: UserModel
    
class InvoiceResponse(BaseModel): 
    id: str
    subscription_id: str
    transaction_id: str
    stripe_invoice_id: str
    amount_paid: float
    currency: str
    pdf_url: str
    created_at: int  # timestamp in epoch
    # subscription: SubscriptionModel
    # transaction: TransactionModel
    user: UserModel 

    
    

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    plan_id = Column(Integer, ForeignKey("plans.id"))
    stripe_subscription_id = Column(String)
    status = Column(SQLAlchemyEnum(SubscriptionStatus))
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    canceled_at = Column(DateTime)
    paypal_billing_agreement_id = Column(String)
    paypal_plan_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    plan = relationship("Plan")
    invoices = relationship("Invoice", back_populates="subscription")
    
class SubscriptionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    plan_id: str
    stripe_subscription_id: str
    status: SubscriptionStatus
    current_period_start: int  # timestamp in epoch
    current_period_end: int  # timestamp in epoch
    canceled_at: Optional[int]  # timestamp in epoch
    created_at: int  # timestamp in epoch
    updated_at: int  # timestamp in epoch
    stripe_subscription_id: str
    paypal_billing_agreement_id: Optional[str] = None
    paypal_plan_id: Optional[str] = None
    user: UserModel
    plan: PlanModel
    invoices: list[InvoiceModel] = []
  
class SubscriptionResponse(BaseModel): 
    id: str
    user_id: str
    plan_id: str
    stripe_subscription_id: str
    status: SubscriptionStatus
    current_period_start: int  # timestamp in epoch
    current_period_end: int  # timestamp in epoch
    canceled_at: Optional[int]  # timestamp in epoch
    created_at: int  # timestamp in epoch
    updated_at: int  # timestamp in epoch
    stripe_subscription_id: str 
    paypal_billing_agreement_id = Optional[str] = None
    paypal_plan_id = Optional[str] = None
    user: UserModel
    plan: PlanModel
    invoices: list[Invoice] = []
    
    
    
    
    
    
class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    currency = Column(String, default="usd")
    status = Column(SQLAlchemyEnum(TransactionStatus))
    type = Column(String)  # "subscription", "one-time"
    stripe_payment_intent_id = Column(String)
    paypal_order_id = Column(String)
    paypal_capture_id = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    invoice = relationship("Invoice", back_populates="transaction")

class TransactionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    amount: float
    currency: str
    status: TransactionStatus
    type: str
    stripe_payment_intent_id: str
    paypal_order_id: Optional[str] = None
    paypal_capture_id: Optional[str] = None
    description: str
    created_at: int  # timestamp in epoch
    
    user: UserModel 
    invoices: list[Invoice] = []

class TransactionResponse(BaseModel): 
    id: str
    user_id: str
    amount: float
    currency: str
    status: TransactionStatus
    type: str
    stripe_payment_intent_id: str
    paypal_order_id: Optional[str] = None
    paypal_capture_id: Optional[str] = None
    description: str
    created_at: int  # timestamp in epoch
    
    user: UserModel 
    invoices: list[Invoice] = []  
    
    
class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    stripe_payment_method_id = Column(String)
    type = Column(SQLAlchemyEnum(PaymentMethodType))
    details = Column(JSON)  # {last4: "4242", brand: "visa"}
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="payment_methods")

class PaymentMethodModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    stripe_payment_method_id: str
    type: PaymentMethodType
    details: dict
    is_default: bool
    created_at: int  # timestamp in epoch
    user: UserModel
    
      
class InvoiceResponse(BaseModel): 
    id: str
    subscription_id: str
    transaction_id: str
    stripe_invoice_id: str
    amount_paid: float
    currency: str
    pdf_url: str
    created_at: int  # timestamp in epoch
    subscription: SubscriptionModel
    transaction: TransactionModel
    user: UserModel  
    
    
    
    
class CheckoutSession(Base):
    __tablename__ = "checkout_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    stripe_session_id = Column(String)
    status = Column(String)  # "complete", "expired", "open"
    mode = Column(String)  # "payment", "subscription"
    price_id = Column(String)
    success_url = Column(String)
    cancel_url = Column(String)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class CheckoutSessionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    stripe_session_id: str
    status: str
    mode: str
    price_id: str
    success_url: str
    cancel_url: str
    expires_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch
    user: UserModel
    
    
class CheckoutSessionResponse(BaseModel):
    id: str
    user_id: str
    stripe_session_id: str
    status: str
    mode: str
    price_id: str
    success_url: str
    cancel_url: str
    expires_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch
    user: UserModel
