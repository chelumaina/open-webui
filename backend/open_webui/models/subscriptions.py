import json
import logging
import time
from typing import Optional
import uuid
from sqlalchemy import not_

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


from pydantic import BaseModel as PydanticBaseModel
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, Enum, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship


Base = declarative_base()

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


    # # Relationships
    # subscriptions = relationship("Subscription", back_populates="user")
    # transactions = relationship("Transaction", back_populates="user")
    # payment_methods = relationship("PaymentMethod", back_populates="user")



class DbBaseModel(Base):
    __abstract__ = True
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class ResponseModel(PydanticBaseModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class Plan(DbBaseModel):
    __tablename__ = "plans"
    # paypal_plan_id = Column(PG_UUID(as_uuid=True), unique=True, nullable=False)
    paypal_plan_id = Column(String, nullable=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    currency = Column(String, default="USD", nullable=False)
    billing_cycle = Column(String, nullable=False)
    status = Column(String, default="ACTIVE", nullable=False)
    # Relationship: one plan can have many subscriptions
    # subscriptions = relationship("Subscription", back_populates="subscriptions") 
    
    

class PlanModel(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    # id: PG_UUID
    id: uuid.UUID
    paypal_plan_id:Optional[str]
    name: str
    description: Optional[str]
    price: float
    currency: Optional[str]
    billing_cycle: str
    status: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    # subscriptions: List[Subscription] = []
    # model_config = ConfigDict(from_attributes=True)  # ✅ Enables ORM conversion
    class Config:
        from_attributes = True

    @classmethod 
    def from_orm(cls, obj):
        return cls.model_validate({
            "id": obj.id,  # Convert UUID to string
            "name": obj.name,
            "price": obj.price,
            "paypal_plan_id": obj.paypal_plan_id,
            "description": obj.description,
            "currency": obj.currency,
            "billing_cycle": obj.billing_cycle,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
            "status": obj.status
        })
        
class PlanForm(BaseModel):
    name: str
    description: Optional[str]
    price: float
    currency: str
    billing_cycle: str
    status: str
    # model_config = ConfigDict(extra="allow")


    
class PlanResponse(ResponseModel):
    name: str
    description: Optional[str]
    price: float
    currency: str
    billing_cycle: str
    status: str
    # model_config = ConfigDict(extra="allow")

    
class Subscription(DbBaseModel):
    __tablename__ = "subscriptions"
    customer_id = Column(PG_UUID(as_uuid=True), nullable=False)
    plan_id = Column(PG_UUID(as_uuid=True), ForeignKey("plans.id"), nullable=True)
    status = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    next_billing_date = Column(DateTime)


class SubscriptionModel(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    customer_id: Optional[uuid.UUID]
    plan_id: Optional[uuid.UUID]
    status: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    next_billing_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)  # ✅ Enables ORM conversion

    @classmethod 
    def from_orm(cls, obj):
        return cls.model_validate({
            "id": obj.id,  # Convert UUID to string
            "customer_id": obj.customer_id,
            "plan_id": obj.plan_id,
            "status": obj.status,
            "start_date": obj.start_date,
            "end_date": obj.end_date,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
            "next_billing_date": obj.next_billing_date
        })
        
    
class SubscriptionForm(BaseModel):
    customer_id: Optional[uuid.UUID]
    plan_id: Optional[uuid.UUID]
    status: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    next_billing_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    
class SubscriptionResponse(ResponseModel):
    customer_id: uuid.UUID
    plan_id: uuid.UUID
    status: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    next_billing_date: Optional[datetime]
 
 
 
    
    
class Invoice(DbBaseModel):
    __tablename__ = "invoices"
    # paypal_invoice_id = Column(PG_UUID(as_uuid=True), unique=True, nullable=False)
    # customer_id = Column(PG_UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    subscription_id = Column(PG_UUID(as_uuid=True), ForeignKey("subscriptions.id"))
    paypal_order_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    captured_json = Column(JSON, nullable=True, default={})
    currency = Column(String, default="USD", nullable=False)
    status = Column(String, nullable=False)
    issue_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime)

    @classmethod 
    def from_orm(cls, obj):
        return cls.model_validate({
            "id": obj.id,  # Convert UUID to string
            "subscription_id": obj.subscription_id,
            'paypal_order_id':obj.paypal_order_id,
            "amount": obj.amount,
            "status": obj.status,
            "currency": obj.currency,
            "due_date": obj.due_date,
            "issue_date": obj.issue_date,
            'captured_json':obj.captured_json,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
        })

class InvoiceModel(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    subscription_id: uuid.UUID
    amount: float
    paypal_order_id: Optional[str]
    currency: str
    status: str
    captured_json: Optional[dict]={}
    issue_date: datetime
    due_date: datetime
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)  # ✅ Enables ORM conversion
    
    
class InvoiceForm(BaseModel):
    subscription_id: uuid.UUID
    amount: float
    paypal_order_id: Optional[str]
    currency: str
    status: str
    captured_json: Optional[dict]={}
    issue_date: datetime
    due_date: datetime
    created_at: datetime
    updated_at: datetime

    
class InvoiceResponse(BaseModel):
    id: uuid.UUID
    subscription_id: uuid.UUID
    amount: float
    paypal_order_id: Optional[str]
    currency: str
    status: str
    captured_json: Optional[dict]={}
    issue_date: datetime
    due_date: datetime
    created_at: datetime
    updated_at: datetime
 


class Transaction(DbBaseModel):
    __tablename__ = "transactions"
    subscription_id = Column(PG_UUID(as_uuid=True), ForeignKey("subscriptions.id"), nullable=False)
    invoice_id = Column(PG_UUID(as_uuid=True), ForeignKey("invoices.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD", nullable=False)
    status = Column(String, nullable=False)
    transaction_date = Column(DateTime, nullable=False)



class TransactionModel(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    subscription_id: Optional[uuid.UUID] 
    invoice_id: Optional[uuid.UUID] 
    amount: float
    currency: str
    status: str
    transaction_date: Optional[datetime] 
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)  # ✅ Enables ORM conversion

    @classmethod 
    def from_orm(cls, obj):
        return cls.model_validate({
            "id": obj.id,  # Convert UUID to string
            "subscription_id": obj.subscription_id,
            "amount": obj.amount,
            "status": obj.status,
            "currency": obj.currency,
            "transaction_date": obj.transaction_date,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
        })
        
    
class TransactionForm(BaseModel):
    subscription_id: Optional[uuid.UUID] 
    invoice_id: Optional[uuid.UUID] 
    amount: float
    currency: str
    status: str
    transaction_date: Optional[datetime]  

    
class TransactionResponse(ResponseModel):
    subscription_id: Optional[uuid.UUID] 
    invoice_id: Optional[uuid.UUID] 
    amount: float
    currency: str
    status: str
    transaction_date: Optional[datetime] 
 
    
class CheckoutSession(DbBaseModel):
    __tablename__ = "checkout_sessions"
    paypal_session_id = Column(PG_UUID(as_uuid=True), unique=True, nullable=False)
    customer_id = Column(PG_UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    subscription_id = Column(PG_UUID(as_uuid=True), ForeignKey("subscriptions.id"))
    status = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD", nullable=False)


class CustomerResponse(ResponseModel):
    paypal_customer_id: UUID
    email: str
    first_name: Optional[str]
    last_name: Optional[str]



class Payer(Base):
    __tablename__ = "payers"
    id = Column(String, primary_key=True)
    email = Column(String)
    country_code = Column(String)
    given_name = Column(String)
    surname = Column(String)
    orders = relationship("Order", back_populates="payer")


class Order(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True)
    intent = Column(String)
    status = Column(String)
    create_time = Column(DateTime)
    update_time = Column(DateTime)

    payer_id = Column(String, ForeignKey("payers.id"))
    payer = relationship("Payer", back_populates="orders")
    purchase_units = relationship("PurchaseUnit", back_populates="order")


class PurchaseUnit(Base):
    __tablename__ = "purchase_units"
    id = Column(String, primary_key=True)  # use reference_id as ID
    order_id = Column(String, ForeignKey("orders.id"))
    amount = Column(Float)
    currency = Column(String)
    description = Column(String)
    merchant_id = Column(String)
    payee_email = Column(String)

    shipping_name = Column(String)
    shipping_address = Column(JSON)

    order = relationship("Order", back_populates="purchase_units")
    captures = relationship("Capture", back_populates="purchase_unit")
    items = relationship("Item", back_populates="purchase_unit")


class Capture(Base):
    __tablename__ = "captures"
    id = Column(String, primary_key=True)
    status = Column(String)
    purchase_unit_id = Column(String, ForeignKey("purchase_units.id"))
    amount = Column(Float)
    currency = Column(String)
    is_final = Column(Boolean)
    gross_amount = Column(Float)
    paypal_fee = Column(Float)
    net_amount = Column(Float)
    create_time = Column(DateTime)
    update_time = Column(DateTime)

    dispute_categories = Column(ARRAY(String))

    purchase_unit = relationship("PurchaseUnit", back_populates="captures")


class Item(Base):
    __tablename__ = "items"
    id = Column(String, primary_key=True)
    purchase_unit_id = Column(String, ForeignKey("purchase_units.id"))
    name = Column(String)
    quantity = Column(String)
    unit_amount = Column(Float)
    currency = Column(String)

    purchase_unit = relationship("PurchaseUnit", back_populates="items")
    
    
class PlanTable:
    def insert_new_plan(self, user_id: str, form_data:PlanForm) -> Optional[PlanModel]:
        
        with get_db() as db:
            id = str(uuid.uuid4())
            plan = PlanModel(
                 **{
                    **form_data.model_dump(),
                    "paypal_plan_id":"None21",
                    "created_at":datetime.now(),
                    "updated_at":datetime.now(),
                 }
            )
            
            # log.debug(f"chat => {**plan.model_dump()}")


            result = Plan(**plan.model_dump())
            
            log.debug(f"result => {result}")

            db.add(result)
            db.commit()
            db.refresh(result)
            return PlanModel.model_validate(result) if result else None

    def update_plan(self, id: str, form_data:PlanForm,  ) -> Optional[PlanModel]:
        try:
            with get_db() as db:
                plan_item = db.get(Plan, id)
                # chat_item.chat = chat
                # chat_item.prompt_token = prompt_token

                plan_item.name = form_data.name
                plan_item.description = form_data.description
                plan_item.price = form_data.price
                plan_item.currency = form_data.currency
                plan_item.billing_cycle = form_data.billing_cycle
                plan_item.status = form_data.status
                plan_item.paypal_plan_id = form_data.paypal_plan_id
                plan_item.updated_at = datetime.now()
                db.commit()
                db.refresh(plan_item) 
                return PlanModel.model_validate(plan_item)
        except Exception as ex:
            print(f"Error updating chat: {ex}")
            return None
         
    def get_plans(self) -> list[PlanModel]:
        with get_db() as db:
            query = db.query(Plan)
            query = query.order_by(Plan.updated_at.desc())
            all_plans = query.all()
            return [PlanModel.model_validate(p) for p in all_plans]
         
    def get_plan_by_id(self, id: str) -> Optional[dict]:
        try:
            with get_db() as db:
                plan_item = db.get(Plan, id) 
                return PlanModel.model_validate(plan_item)
                # return Plan(**plan_item.model_dump())
        except Exception as ex:
            print(f"Error updating chat: {ex}")
            return None
        
        # plan = self.get_plan_by_id(id)
        # if plan is None:
        #     return None
        # return Plan(**plan.model_dump())
  
  
    def get_plan_by_user_id_and_name(
        self, user_id: str, name: str
    ) -> Optional[PlanModel]:
        try:
            with get_db() as db:
                # Check if folder exists
                plan = (
                    db.query(Plan)
                    # .filter_by(parent_id=parent_id, user_id=user_id)
                    .filter(Plan.name.ilike(name))
                    .first()
                )

                if not plan:
                    return None

                return PlanModel.model_validate(plan)
        except Exception as e:
            log.error(f"get_plan_by_user_id_and_name: {e}")
            return None

    def delete_plan_by_id(self, id: str) -> bool:
        try: 
            with get_db() as db: 
                # plan_item = db.get(Plan, id) 
                db.query(Plan).filter_by(id=id).delete()
                db.commit()
                return True
        except Exception:
            return False
        
Plans = PlanTable()







class SubscriptionTable:
    def insert_new_subscription(self, user_id: str, form_data:SubscriptionForm) -> Optional[SubscriptionModel]:
        
        with get_db() as db:
            id = str(uuid.uuid4())
            model = SubscriptionModel(
                 **{
                    **form_data.model_dump(), 
                    'id':id
                 }
            )
            
            log.debug(f"chat => {model.model_dump()}")


            result = Subscription(**model.model_dump())
            
            log.debug(f"result => {result}")

            db.add(result)
            db.commit()
            db.refresh(result)
            return SubscriptionModel.model_validate(result) if result else None

    def update_subscription(self, id: str, form_data:SubscriptionForm,  ) -> Optional[SubscriptionModel]:
        try:
            with get_db() as db:
                plan_item = db.get(Subscription, id)
               
                plan_item.customer_id = form_data.customer_id
                plan_item.plan_id = form_data.plan_id
                plan_item.status = form_data.status
                plan_item.start_date = form_data.start_date
                plan_item.end_date = form_data.end_date
                plan_item.status = form_data.status
                plan_item.next_billing_date = form_data.next_billing_date
                plan_item.updated_at = datetime.now()
                db.commit()
                db.refresh(plan_item) 
                return SubscriptionModel.model_validate(plan_item)
        except Exception as ex:
            print(f"Error updating chat: {ex}")
            return None
         
    def get_subscriptions(self, user_id:str) -> list[SubscriptionModel]:
        with get_db() as db:
            query = db.query(Subscription)
            query = query.order_by(Subscription.updated_at.desc())
            all_plans = query.all()
            return [SubscriptionModel.model_validate(p) for p in all_plans]
         
    def get_subscription_by_id(self, id: str) -> Optional[dict]:
        try:
            with get_db() as db:
                plan_item = db.get(Subscription, id) 
                return SubscriptionModel.model_validate(plan_item)
                # return Plan(**plan_item.model_dump())
        except Exception as ex:
            print(f"Error updating chat: {ex}")
            return None

    def delete_subscription_by_id(self, id: str) -> bool:
        try: 
            with get_db() as db: 
                # plan_item = db.get(Plan, id) 
                db.query(Subscription).filter_by(id=id).delete()
                db.commit()
                return True
        except Exception:
            return False
        
Subscriptions = SubscriptionTable()




class TransactionTable:
    def insert_new_transaction(self, user_id: str, form_data:TransactionForm) -> Optional[TransactionModel]:
        
        with get_db() as db:
            id = str(uuid.uuid4())
            plan = TransactionModel(
                 **{
                    **form_data.model_dump(), 
                    "created_at":datetime.now(),
                    "updated_at":datetime.now(),
                 }
            )
            
            log.debug(f"chat => {plan.model_dump()}")


            result = Transaction(**plan.model_dump())
            
            log.debug(f"result => {result}")

            db.add(result)
            db.commit()
            db.refresh(result)
            return TransactionModel.model_validate(result) if result else None

    def update_transaction(self, id: str, form_data:TransactionForm,  ) -> Optional[TransactionModel]:
        try:
            with get_db() as db:
                plan_item = db.get(Transaction, id)
                  
                plan_item.subscription_id = form_data.subscription_id
                plan_item.amount = form_data.amount
                plan_item.currency = form_data.currency
                plan_item.status = form_data.status
                plan_item.transaction_date = form_data.transaction_date 
                plan_item.updated_at = datetime.now()
                db.commit()
                db.refresh(plan_item) 
                return TransactionModel.model_validate(plan_item)
        except Exception as ex:
            print(f"Error updating chat: {ex}")
            return None
         
    def get_transactions(self, user_id:str) -> list[TransactionModel]:
        with get_db() as db:
            query = db.query(Transaction)
            query = query.order_by(Transaction.updated_at.desc())
            all_plans = query.all()
            return [TransactionModel.model_validate(p) for p in all_plans]
         
    def get_transaction_by_id(self, id: str) -> Optional[dict]:
        try:
            with get_db() as db:
                plan_item = db.get(Transaction, id) 
                return TransactionModel.model_validate(plan_item)
                # return Plan(**plan_item.model_dump())
        except Exception as ex:
            print(f"Error updating chat: {ex}")
            return None

    def delete_transaction_by_id(self, id: str) -> bool:
        try: 
            with get_db() as db: 
                # plan_item = db.get(Plan, id) 
                db.query(Transaction).filter_by(id=id).delete()
                db.commit()
                return True
        except Exception:
            return False
        
Transactions = TransactionTable()






class InvoiceTable:
    def insert_new_invoice(self, user_id: str, form_data:InvoiceForm) -> Optional[InvoiceModel]:
        
        with get_db() as db:
            id = str(uuid.uuid4())
            plan = InvoiceModel(
                 **{
                    **form_data.model_dump(), 
                    "id":id,
                 }
            )
            
            log.debug(f"chat => {plan.model_dump()}")


            result = Invoice(**plan.model_dump())
            
            log.debug(f"result => {result}")

            db.add(result)
            db.commit()
            db.refresh(result)
            return InvoiceModel.model_validate(result) if result else None

    def update_invoice(self, id: str, form_data:InvoiceForm,  ) -> Optional[InvoiceModel]:
        try:
            with get_db() as db:
                plan_item = db.get(Invoice, id)
                  
                plan_item.subscription_id = form_data.subscription_id
                plan_item.amount = form_data.amount
                plan_item.currency = form_data.currency
                plan_item.status = form_data.status
                plan_item.invoice_date = form_data.invoice_date 
                plan_item.updated_at = datetime.now()
                db.commit()
                db.refresh(plan_item) 
                return InvoiceModel.model_validate(plan_item)
        except Exception as ex:
            print(f"Error updating chat: {ex}")
            return None
         
    def get_invoices(self, user_id:str) -> list[InvoiceModel]:
        with get_db() as db:
            query = db.query(Invoice)
            query = query.order_by(Invoice.updated_at.desc())
            all_plans = query.all()
            return [InvoiceModel.model_validate(p) for p in all_plans]
         
    def get_invoice_by_id(self, id: str) -> Optional[dict]:
        try:
            with get_db() as db:
                plan_item = db.get(Invoice, id) 
                return InvoiceModel.model_validate(plan_item)
                # return Plan(**plan_item.model_dump())
        except Exception as ex:
            print(f"Error updating chat: {ex}")
            return None


    def get_invoice_by_name(self, id: str) -> Optional[dict]:
        try:
            with get_db() as db:
                plan_item = db.query(Invoice).filter_by(id=id).delete()

                # plan_item = db.get(Invoice, id) 
                return InvoiceModel.model_validate(plan_item)
                # return Plan(**plan_item.model_dump())
        except Exception as ex:
            print(f"Error updating chat: {ex}")
            return None
        
    def delete_invoice_by_id(self, id: str) -> bool:
        try: 
            with get_db() as db: 
                # plan_item = db.get(Plan, id) 
                db.query(Invoice).filter_by(id=id).delete()
                db.commit()
                return True
        except Exception:
            return False
        
Invoices = InvoiceTable()



class TransactionTable:
    def insert_new_transaction(self, user_id: str, form_data:TransactionForm) -> Optional[TransactionModel]:
        
        with get_db() as db:
            id = str(uuid.uuid4())
            plan = TransactionModel(
                 **{
                    **form_data.model_dump(), 
                    "created_at":datetime.now(),
                    "updated_at":datetime.now(),
                 }
            )
            
            log.debug(f"chat => {plan.model_dump()}")


            result = Transaction(**plan.model_dump())
            
            log.debug(f"result => {result}")

            db.add(result)
            db.commit()
            db.refresh(result)
            return TransactionModel.model_validate(result) if result else None

    def update_transaction(self, id: str, form_data:TransactionForm,  ) -> Optional[TransactionModel]:
        try:
            with get_db() as db:
                plan_item = db.get(Transaction, id)
                  
                plan_item.subscription_id = form_data.subscription_id
                plan_item.amount = form_data.amount
                plan_item.currency = form_data.currency
                plan_item.status = form_data.status
                plan_item.transaction_date = form_data.transaction_date 
                plan_item.updated_at = datetime.now()
                db.commit()
                db.refresh(plan_item) 
                return TransactionModel.model_validate(plan_item)
        except Exception as ex:
            print(f"Error updating chat: {ex}")
            return None
         
    def get_transactions(self, user_id:str) -> list[TransactionModel]:
        with get_db() as db:
            query = db.query(Transaction)
            query = query.order_by(Transaction.updated_at.desc())
            all_plans = query.all()
            return [TransactionModel.model_validate(p) for p in all_plans]
         
    def get_transaction_by_id(self, id: str) -> Optional[dict]:
        try:
            with get_db() as db:
                plan_item = db.get(Transaction, id) 
                return TransactionModel.model_validate(plan_item)
                # return Plan(**plan_item.model_dump())
        except Exception as ex:
            print(f"Error updating chat: {ex}")
            return None

    def delete_transaction_by_id(self, id: str) -> bool:
        try: 
            with get_db() as db: 
                # plan_item = db.get(Plan, id) 
                db.query(Transaction).filter_by(id=id).delete()
                db.commit()
                return True
        except Exception:
            return False
        
        
            
    async def save_paypal_response_to_db(self, order_id:str, data: dict):
        try: 
            from datetime import datetime
            from dateutil.relativedelta import relativedelta

            with get_db() as db: 
                invoice= db.query(Invoice).filter_by(paypal_order_id=order_id).filter(not_(Invoice.status != "COMPLETED")).first()
                
                subscription= db.get(Subscription, invoice.subscription_id)
                if not invoice:
                    return False
                if not subscription:
                    return False
                
                diff = subscription.end_date - subscription.start_date
                days = diff.days
                if days <= 0:
                    days=0
                    
                # # Example end date
                # end_date = datetime.strptime(subscription.end_date, "%Y-%m-%d")
                one_month_later = datetime.now() + relativedelta(months=1)+days

                # print(f"{one_month_later=}")

                # # Add 1 month
                # new_end_date = end_date + relativedelta(months=1)
                # print(f"{new_end_date=}")


                subscription.status = 'active'
                # subscription.updated_at=data.get('update_time')
                subscription.end_date = one_month_later
                subscription.next_billing_date = one_month_later
               
                
                db.commit()
                db.refresh(subscription)

                invoice.captured_json = data
                invoice.status = data.get("status")
                # invoice.updated_at=data.get('update_time')
              
                db.commit()
                db.refresh(invoice) 
                 
                return {'invoice':InvoiceModel.model_validate(invoice),'subscription':SubscriptionModel.model_validate(subscription),} 
                        
                # # Save payer
                # payer_info = data["payer"]
                # payer = Payer(
                #     id=payer_info["payer_id"],
                #     email=payer_info["email_address"],
                #     country_code=payer_info["address"]["country_code"],
                #     given_name=payer_info["name"]["given_name"],
                #     surname=payer_info["name"]["surname"],
                # )
                # db.merge(payer)

                # # Save order
                # order = Order(
                #     id=data["id"],
                #     intent=data["intent"],
                #     status=data["status"],
                #     payer_id=payer.id,
                #     create_time=datetime.fromisoformat(data["create_time"].replace("Z", "+00:00")),
                #     update_time=datetime.fromisoformat(data["update_time"].replace("Z", "+00:00"))
                # )
                # db.merge(order)

                # for pu in data["purchase_units"]:
                #     pu_model = PurchaseUnit(
                #         id=pu["reference_id"],
                #         order_id=order.id,
                #         amount=float(pu["amount"]["value"]),
                #         currency=pu["amount"]["currency_code"],
                #         description=pu.get("description"),
                #         merchant_id=pu["payee"]["merchant_id"],
                #         payee_email=pu["payee"]["email_address"],
                #         shipping_name=pu["shipping"]["name"]["full_name"],
                #         shipping_address=pu["shipping"]["address"]
                #     )
                #     db.merge(pu_model)

                #     # Items
                #     for item in pu.get("items", []):
                #         item_model = Item(
                #             id=str(uuid.uuid4()),
                #             purchase_unit_id=pu_model.id,
                #             name=item["name"],
                #             quantity=item["quantity"],
                #             unit_amount=float(item["unit_amount"]["value"]),
                #             currency=item["unit_amount"]["currency_code"]
                #         )
                #         db.add(item_model)

                #     # Captures
                #     for capture in pu["payments"]["captures"]:
                #         cap_model = Capture(
                #             id=capture["id"],
                #             purchase_unit_id=pu_model.id,
                #             status=capture["status"],
                #             amount=float(capture["amount"]["value"]),
                #             currency=capture["amount"]["currency_code"],
                #             is_final=capture["final_capture"],
                #             gross_amount=float(capture["seller_receivable_breakdown"]["gross_amount"]["value"]),
                #             paypal_fee=float(capture["seller_receivable_breakdown"]["paypal_fee"]["value"]),
                #             net_amount=float(capture["seller_receivable_breakdown"]["net_amount"]["value"]),
                #             dispute_categories=capture["seller_protection"].get("dispute_categories", []),
                #             create_time=datetime.fromisoformat(capture["create_time"].replace("Z", "+00:00")),
                #             update_time=datetime.fromisoformat(capture["update_time"].replace("Z", "+00:00")),
                #         )
                #         db.merge(cap_model)

                # db.commit()

        except Exception as e:
            print(f"Error saving PayPal response to DB: {e}")
            return False

Transactions = TransactionTable()

