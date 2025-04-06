# webhook_handlers.py
from sqlalchemy.orm import Session
# from . import models, schemas, crud
import logging, requests
from datetime import datetime

logger = logging.getLogger(__name__)
from fastapi import  HTTPException
from open_webui.models.subscriptions import Subscription, Subscriptions, Invoices, InvoiceForm, SubscriptionForm

import httpx
import base64
import os

# # PayPal API Credentials
# PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "your-client-id")
# PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET", "your-client-secret")

PAYPAL_BASE_URL = "https://api-m.sandbox.paypal.com"  # Change to "live" for production
PAYPAL_CLIENT_ID = "AV7CoRHni5FA0I-RQkQRcjGbmR6fiE2sxbOV9iivnm7Sn03UG5gufJceXBGj08qI4-N3cDE17i6bSR48"
PAYPAL_CLIENT_SECRET ="EI2HsBHaJvG5rKAsoAMdfA1pSKms7J5gNOIk8TZC1VS8FBDAzsAg0-K0Lk4Waw996AFjThfHQV-0wnb5"

async def get_paypal_token():
    auth = base64.b64encode(f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}", "Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{PAYPAL_BASE_URL}/v1/oauth2/token", headers=headers, data={"grant_type": "client_credentials"})
    
    response_data = response.json()
    return response_data.get("access_token")

async def capture_paypal_order(order_id: str):
    access_token = await get_paypal_token()
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
   
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture", headers=headers)

    return response.json()

async def get_payment_details_update(order_id: str):
    access_token = await get_paypal_token()
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    #curl -v -X GET https://api-m.sandbox.paypal.com/v2/checkout/orders/5O190127TN364715T \

    url = f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    # logger.info(f"{response=}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to create order")

    return response.json()
     

async def create_paypal_order(user_id:str, amount: float = "10.00", currency: str = "USD"):
    access_token = await get_paypal_token()
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [
        {
            "reference_id": f"ORDER_{user_id}",
            "amount": {
                "currency_code": currency,
                "value": amount,
                "breakdown": {
                "item_total": {
                    "currency_code": currency,
                    "value": amount
                }
                }
            },
            "description": "BixAI subscription",
            "items": [
                {
                "name": "BixAI Plus Subscription Plan",
                "unit_amount": {
                    "currency_code": currency,
                    "value": amount
                },
                "quantity": "1"
                }
            ]
            }
        ],
        # "purchase_units": [{"amount": {"currency_code": currency, "value": amount}}],
        "application_context": {
            "return_url": "https://yourdomain.com/success",
            "cancel_url": "https://yourdomain.com/cancel"
        }
    }
 
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{PAYPAL_BASE_URL}/v2/checkout/orders", headers=headers, json=order_data)
    
    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail="Failed to create order")
    order_info = response.json()
    paypal_order_id = order_info["id"]
    
    form_data={ 
            'customer_id': user_id,
            'plan_id': '3aa2741e-0944-4c22-b48c-298200fb4a90',
            'status': 'pending',
            'start_date': datetime.now(),
            'end_date': datetime.now(),
            'next_billing_date': datetime.now(),
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
    }
    form_data=SubscriptionForm(**form_data)
    subscription = Subscriptions.insert_new_subscription(user_id, form_data)

    form_data={ 
        'subscription_id': subscription.id,
        'amount': amount,
        'paypal_order_id': paypal_order_id,
        'currency': currency,
        'status': 'pending',
        'issue_date': datetime.now(),
        'due_date': datetime.now(),
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
    }
    form_data=InvoiceForm(**form_data) 
    invoice = Invoices.insert_new_invoice(user_id, form_data)
    order_info["invoice_id"]=invoice.id 
    order_info["subscription_id"]=subscription.id 
    
    return order_info

# async def handle_payment_completed(db: Session, event_data: dict):
#     """
#     Handle PAYMENT.CAPTURE.COMPLETED webhook event
#     """
#     try:
#         # Extract relevant data from webhook
#         payment_id = event_data.get('id')
#         amount = event_data.get('amount', {}).get('value')
#         currency = event_data.get('amount', {}).get('currency_code')
#         custom_id = event_data.get('custom_id')  # Should contain user ID
#         payer_id = event_data.get('payer', {}).get('payer_id')
        
#         # Check if we've already processed this event
#         if crud.get_transaction_by_paypal_id(db, payment_id):
#             logger.warning(f"Payment {payment_id} already processed")
#             return

#         # Find associated user
#         user = crud.get_user_by_paypal_payer_id(db, payer_id) or \
#                crud.get_user_by_custom_id(db, custom_id)

#         if not user:
#             logger.error(f"User not found for payment {payment_id}")
#             return

#         # Create transaction record
#         transaction = schemas.TransactionCreate(
#             amount=float(amount),
#             currency=currency,
#             status="completed",
#             paypal_capture_id=payment_id,
#             description="PayPal payment completed"
#         )

#         db_transaction = crud.create_transaction(db, user.id, transaction)
        
#         # Update user balance or token count
#         user.current_balance += float(amount)
#         db.commit()
        
#         # Send confirmation email
#         await send_payment_confirmation_email(user.email, db_transaction)
        
#         logger.info(f"Processed payment {payment_id} for user {user.id}")

#     except Exception as e:
#         logger.error(f"Error processing payment completed: {str(e)}")
#         db.rollback()
#         raise

# async def handle_subscription_activated(db: Session, event_data: dict):
#     """
#     Handle BILLING.SUBSCRIPTION.ACTIVATED webhook event
#     """
#     try:
#         subscription_id = event_data.get('id')
#         plan_id = event_data.get('plan_id')
#         payer = event_data.get('subscriber', {}).get('payer_id')
#         start_time = event_data.get('start_time')
        
#         # Check for existing subscription
#         existing_sub = crud.get_subscription_by_paypal_id(db, subscription_id)
#         if existing_sub:
#             logger.warning(f"Subscription {subscription_id} already exists")
#             return

#         # Find user by PayPal payer ID
#         user = crud.get_user_by_paypal_payer_id(db, payer)
#         if not user:
#             logger.error(f"User not found for subscription {subscription_id}")
#             return

#         # Create subscription record
#         subscription = schemas.SubscriptionCreate(
#             paypal_plan_id=plan_id,
#             paypal_billing_agreement_id=subscription_id,
#             status="active",
#             start_date=datetime.fromisoformat(start_time),
#             user_id=user.id
#         )

#         db_subscription = crud.create_subscription(db, subscription)
        
#         # Update user's plan
#         user.subscription_plan = plan_id
#         db.commit()
        
#         logger.info(f"Activated subscription {subscription_id} for user {user.id}")

#     except Exception as e:
#         logger.error(f"Error processing subscription activation: {str(e)}")
#         db.rollback()
#         raise

# async def handle_subscription_cancelled(db: Session, event_data: dict):
#     """
#     Handle BILLING.SUBSCRIPTION.CANCELLED webhook event
#     """
#     try:
#         subscription_id = event_data.get('id')
#         reason = event_data.get('reason_code')
#         cancellation_time = event_data.get('cancellation_time')

#         # Find subscription
#         subscription = crud.get_subscription_by_paypal_id(db, subscription_id)
#         if not subscription:
#             logger.error(f"Subscription {subscription_id} not found")
#             return

#         # Update subscription status
#         subscription.status = "cancelled"
#         subscription.cancelled_at = datetime.fromisoformat(cancellation_time)
#         subscription.cancellation_reason = reason
#         db.commit()

#         # Downgrade user plan
#         user = subscription.user
#         user.subscription_plan = "free"
#         db.commit()
        
#         # Send notification
#         await send_subscription_cancellation_email(user.email, reason)
        
#         logger.info(f"Cancelled subscription {subscription_id} for user {user.id}")

#     except Exception as e:
#         logger.error(f"Error processing subscription cancellation: {str(e)}")
#         db.rollback()
#         raise

# # Helper functions
# async def send_payment_confirmation_email(email: str, transaction: models.Transaction):
#     # Implementation for sending email
#     pass

# async def send_subscription_cancellation_email(email: str, reason: str):
#     # Implementation for sending email
#     pass