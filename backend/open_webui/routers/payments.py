"""
Payment router for handling Paystack payments and subscriptions
"""

import logging
import os
import secrets
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Optional

import requests
from fastapi import APIRouter, Depends, HTTPException, Request, status

from open_webui.internal.db import Base, get_db
from open_webui.models.models import Model
from open_webui.models.groups import Group, Groups

from open_webui.models.users import Users
from open_webui.utils.auth import get_verified_user

from open_webui.models.payments import PaymentInitializeRequest, PaymentInitializeResponse, PaymentTransaction, UserSubscription, PaymentVerifyResponse
from open_webui.env import SRC_LOG_LEVELS


# Paystack configuration - these should be set as environment variables
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY", "")
PAYSTACK_PUBLIC_KEY = os.getenv("PAYSTACK_PUBLIC_KEY", "")
PAYSTACK_BASE_URL = "https://api.paystack.co"

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["OPENAI"])

##########################################
#
# Payment functions
#
##########################################


# class PaymentTransaction(Base):
#     __tablename__ = "payment_transactions"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(String, index=True, nullable=False)
#     reference = Column(String, unique=True, index=True, nullable=False)
#     amount = Column(Float, nullable=False)  # Amount in original currency
#     currency = Column(String, default="NGN", nullable=False)
#     plan_id = Column(String, nullable=False)
#     plan_name = Column(String, nullable=False)
#     status = Column(String, default="pending")  # pending, success, failed, cancelled
#     paystack_reference = Column(String, nullable=True)
#     paystack_status = Column(String, nullable=True)
#     gateway_response = Column(Text, nullable=True)
#     paid_at = Column(DateTime, nullable=True)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# class UserSubscription(Base):
#     __tablename__ = "user_subscriptions"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(String, index=True, nullable=False)
#     plan_id = Column(String, nullable=False)
#     plan_name = Column(String, nullable=False)
#     status = Column(String, default="active")  # active, cancelled, expired
#     amount = Column(Float, nullable=False)
#     currency = Column(String, default="NGN", nullable=False)
#     billing_cycle = Column(String, default="monthly")  # monthly, yearly
#     started_at = Column(DateTime, default=datetime.utcnow)
#     expires_at = Column(DateTime, nullable=True)
#     transaction_reference = Column(String, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# # Pydantic models
# class PaymentInitializeRequest(BaseModel):
#     amount: float = Field(..., description="Amount in the specified currency")
#     currency: str = Field(default="NGN", description="Currency code")
#     plan_id: str = Field(..., description="Plan identifier")
#     plan_name: str = Field(..., description="Plan name")
#     callback_url: Optional[str] = Field(None, description="Callback URL")
    
    
# class PaymentInitializeResponse(BaseModel):
#     success: bool
#     message: str
#     data: Optional[dict] = None


# class PaymentVerifyResponse(BaseModel):
#     success: bool
#     message: str
#     data: Optional[dict] = None


# class WebhookPayload(BaseModel):
#     event: str
#     data: dict


def __update_group_access(group_id: str, user):
    """Create or update user subscription based on payment transaction"""
    group = Groups.add_users_to_group(group_id, [user.id])
    if group:
        log.info(f"User {user.id} added to group {group_id} after payment")
        return group
    else:
        log.error(f"Failed to add user {user.id} to group {group_id} after payment")
        return False

def generate_reference() -> str:
    """Generate a unique payment reference"""
    timestamp = str(int(datetime.utcnow().timestamp()))
    random_str = secrets.token_hex(4)
    return f"ref_{timestamp}_{random_str}"


def verify_webhook_signature(payload: bytes, signature: str) -> bool:
    """Verify Paystack webhook signature"""
    if not PAYSTACK_SECRET_KEY:
        log.warning("Paystack secret key not configured")
        return False
    
    computed_signature = hmac.new(
        PAYSTACK_SECRET_KEY.encode('utf-8'),
        payload,
        hashlib.sha512
    ).hexdigest()
    
    return hmac.compare_digest(signature, computed_signature)

##########################################
#
# Payment routes
#
##########################################

router = APIRouter()

@router.post("/initialize", response_model=PaymentInitializeResponse)
# @router.post("/initialize",response_model=Optional[PaymentInitializeResponse])
async def initialize_payment(
    request: PaymentInitializeRequest,
    # user=Depends(get_verified_user)
    user = Depends(get_verified_user)
):
    """Initialize a payment with Paystack"""
    
    if not PAYSTACK_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Payment service not configured"
        )
    
    try:
        # Generate unique reference
        reference = generate_reference()
        
        # Prepare Paystack payload
        paystack_payload = {
            "email": user.email,
            "amount": int(request.amount * 100),  # Convert to kobo
            "currency": request.currency,
            "reference": reference,
            "callback_url": request.callback_url,
            "metadata": {
                "user_id": user.id,
                "plan_id": request.plan_id,
                "plan_name": request.plan_name,
                "custom_fields": [
                    {
                        "display_name": "Plan",
                        "variable_name": "plan",
                        "value": request.plan_name,
                        "group_id": request.group_id
                    }
                ]
            }
        }
        print(paystack_payload)
        
        # Initialize payment with Paystack
        headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{PAYSTACK_BASE_URL}/transaction/initialize",
            json=paystack_payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code != 200:
            log.error(f"Paystack API error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Payment initialization failed"
            )
        
        paystack_response = response.json()
        
        if not paystack_response.get("status"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=paystack_response.get("message", "Payment initialization failed")
            )
        # print(f"Payment paystack_response: {paystack_response.get('metadata').get('custom_fields')[0].get('group_id')}")
        # Store transaction in database
        with get_db() as db:
            transaction = PaymentTransaction(
                user_id=user.id,
                reference=reference,
                amount=request.amount,
                currency=request.currency,
                plan_id=request.plan_id,
                plan_name=request.plan_name,
                group_id=request.group_id,
                gateway_response_data="",
                gateway_response="", 
                status="pending"
            )
            print(f"{transaction=}")
            
            db.add(transaction)
            db.commit()
        
        return PaymentInitializeResponse(
            success=True,
            message="Payment initialized successfully",
            data=paystack_response.get("data")
        )

    except HTTPException as e:
        log.error(f"Payment initialization error: {str(e)}")
        raise
    except Exception as e:
        log.error(f"Payment initialization error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while initializing payment"
        )


@router.get("/verify/{reference}", response_model=PaymentVerifyResponse)
async def verify_payment(
    reference: str,
    user = Depends(get_verified_user)
):
    """Verify a payment with Paystack"""
    paystack_data = {}
    if not PAYSTACK_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Payment service not configured"
        )
    
    try:
        # Get transaction from database
        with get_db() as db:
            transaction = db.query(PaymentTransaction).filter(
                PaymentTransaction.reference == reference,
                PaymentTransaction.user_id == user.id
            ).first()
            
            if not transaction:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Transaction not found"
                )


            # Verify with Paystack
            headers = {
                "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
                "Content-Type": "application/json"
            }
            paystack_data = {}
            
            response = requests.get(
                f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code != 200:
                log.error(f"Paystack verification error: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Payment verification failed"
                )
            # print(f"{response.text=}")
            paystack_response = response.json()
            paystack_data = paystack_response.get("data", {})
            # print(f"Payment paystack_response: {paystack_data}")
            if not paystack_response.get("status"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=paystack_response.get("message", "Payment verification failed")
                )
            
            paystack_data = paystack_response.get("data", {})
            payment_status = paystack_data.get("status")

            group_id = transaction.group_id
            print(f"Payment group_id: {group_id}")
            # print(f"Payment paystack_response: {paystack_data.get('metadata').get('custom_fields')[0].get('group_id')}")

            
            # Update transaction
            transaction.paystack_status = payment_status
            transaction.gateway_response = paystack_data.get("gateway_response")
            transaction.updated_at = datetime.utcnow()
            # transaction.gateway_response_data = str(paystack_data)

            if payment_status == "success":
                transaction.status = "success"
                transaction.paid_at = datetime.utcnow()
                
                # Create or update subscription
                existing_subscription = db.query(UserSubscription).filter(
                    UserSubscription.user_id == user.id,
                    UserSubscription.status == "active"
                ).first()
                
                if existing_subscription:
                    # Update existing subscription
                    existing_subscription.plan_id = transaction.plan_id
                    existing_subscription.plan_name = transaction.plan_name
                    existing_subscription.amount = transaction.amount
                    existing_subscription.currency = transaction.currency
                    existing_subscription.transaction_reference = reference
                    existing_subscription.updated_at = datetime.utcnow() 
                    existing_subscription.billing_cycle = transaction.billing_cycle
                    existing_subscription.expires_at = existing_subscription.expires_at + timedelta(days=30)
                    existing_subscription.trial_end = existing_subscription.expires_at + timedelta(days=30)
                else:
                    # Create new subscription
                    subscription = UserSubscription(
                        user_id=user.id,
                        plan_id=transaction.plan_id,
                        plan_name=transaction.plan_name,
                        amount=transaction.amount,
                        currency=transaction.currency,
                        transaction_reference=reference,
                        billing_cycle=transaction.billing_cycle,
                        expires_at=datetime.utcnow() + timedelta(days=30),
                        trial_end=datetime.utcnow() + timedelta(days=30),
                        
                        # transaction_reference=reference
                    )
                    db.add(subscription)
            else:
                transaction.status = "failed"
            
            db.commit()
            __update_group_access(group_id, user)
            
            return PaymentVerifyResponse(
                success=True,
                message="Payment verification completed",
                data=paystack_data
            )
        
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Payment verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while verifying payment"
        )


@router.post("/webhook")
async def paystack_webhook(
    request: Request
):
    """Handle Paystack webhooks"""
    
    try:
        # Get raw body and signature
        body = await request.body()
        signature = request.headers.get("x-paystack-signature", "")
        
        # Verify signature
        if not verify_webhook_signature(body, signature):
            log.warning("Invalid webhook signature")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid signature"
            )
        
        # Parse webhook data
        webhook_data = await request.json()
        event = webhook_data.get("event")
        data = webhook_data.get("data", {})
        
        log.info(f"Received webhook event: {event}")
        
        if event == "charge.success":
            # Handle successful payment
            reference = data.get("reference")
            
            if reference:
                with get_db() as db:
                    transaction = db.query(PaymentTransaction).filter(
                        PaymentTransaction.reference == reference
                    ).first()
                    
                    if transaction:
                        transaction.status = "success"
                        transaction.paystack_status = "success"
                        transaction.paid_at = datetime.utcnow()
                        transaction.gateway_response = data.get("gateway_response")
                        transaction.updated_at = datetime.utcnow()
                        
                        # Create or update subscription
                        existing_subscription = db.query(UserSubscription).filter(
                            UserSubscription.user_id == transaction.user_id,
                            UserSubscription.status == "active"
                        ).first()
                        
                        if existing_subscription:
                            existing_subscription.plan_id = transaction.plan_id
                            existing_subscription.plan_name = transaction.plan_name
                            existing_subscription.amount = transaction.amount
                            existing_subscription.currency = transaction.currency
                            existing_subscription.transaction_reference = reference
                            existing_subscription.updated_at = datetime.utcnow()
                        else:
                            subscription = UserSubscription(
                                user_id=transaction.user_id,
                                plan_id=transaction.plan_id,
                                plan_name=transaction.plan_name,
                                amount=transaction.amount,
                                currency=transaction.currency,
                                transaction_reference=reference
                            )
                            db.add(subscription)
                        
                        db.commit()
                        log.info(f"Payment processed successfully: {reference}")
        
        return {"status": "success"}
        
    except Exception as e:
        log.error(f"Webhook processing error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook processing failed"
        )


@router.get("/subscription")
async def get_user_subscription(
    user = Depends(get_verified_user)
):
    """Get user's current subscription"""
    
    with get_db() as db:
        subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == user.id,
            UserSubscription.status == "active"
        ).first()
        
        if not subscription:
            return {"subscription": None}
        
        return {
            "subscription": {
                "id": subscription.id,
                "plan_id": subscription.plan_id,
                "plan_name": subscription.plan_name,
                "status": subscription.status,
                "amount": subscription.amount,
                "currency": subscription.currency,
                "billing_cycle": subscription.billing_cycle,
                "started_at": subscription.started_at.isoformat(),
                "expires_at": subscription.expires_at.isoformat() if subscription.expires_at else None
            }
        }


@router.get("/transactions")
async def get_user_transactions(
    user = Depends(get_verified_user),
    limit: int = 10,
    offset: int = 0
):
    """Get user's payment transactions"""
    
    with get_db() as db:
        transactions = db.query(PaymentTransaction).filter(
            PaymentTransaction.user_id == user.id
        ).order_by(
            PaymentTransaction.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        return {
            "transactions": [
                {
                    "id": tx.id,
                    "reference": tx.reference,
                    "amount": tx.amount,
                    "currency": tx.currency,
                    "plan_id": tx.plan_id,
                    "plan_name": tx.plan_name,
                    "status": tx.status,
                    "paid_at": tx.paid_at.isoformat() if tx.paid_at else None,
                    "created_at": tx.created_at.isoformat()
                }
                for tx in transactions
            ]
        }