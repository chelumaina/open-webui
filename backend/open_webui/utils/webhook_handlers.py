# webhook_handlers.py
from sqlalchemy.orm import Session
# from . import models, schemas, crud
import logging

logger = logging.getLogger(__name__)

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
    # print(f"{PAYPAL_CLIENT_ID}\n\n{PAYPAL_CLIENT_SECRET}")
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

async def create_paypal_order(amount: str = "10.00", currency: str = "USD"):
    access_token = await get_paypal_token()
    print(f"access_token =>{access_token}")
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    print(f"headers =>{headers}")
  
        
    order_data = {
        "intent": "CAPTURE",
        "purchase_units": [{"amount": {"currency_code": currency, "value": amount}}],
        "application_context": {
            "return_url": "https://yourdomain.com/success",
            "cancel_url": "https://yourdomain.com/cancel"
        }
    }
    print(f"order_data =>{order_data}")

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{PAYPAL_BASE_URL}/v2/checkout/orders", headers=headers, json=order_data)

    return response.json()

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