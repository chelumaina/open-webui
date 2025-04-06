from fastapi import FastAPI, HTTPException
from open_webui.utils.webhook_handlers import create_paypal_order, capture_paypal_order, get_payment_details_update
from fastapi import APIRouter, Depends, HTTPException, Request, status
import logging
from open_webui.utils.auth import get_admin_user, get_verified_user

from open_webui.env import SRC_LOG_LEVELS
from typing import Optional

from open_webui.models.subscriptions import Subscription, Transactions, SubscriptionModel, SubscriptionForm, Subscriptions, SubscriptionResponse
from open_webui.constants import ERROR_MESSAGES

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

# app = FastAPI()
router = APIRouter()

@router.post("/create-payment")
async def create_order(amount: float = "15.00"):
 
    order = await create_paypal_order('c3db4cce-cd6a-4596-ad4e-e5e7fbe3e4a7', amount)
    if "id" not in order:
        raise HTTPException(status_code=400, detail="Failed to create PayPal order")
    return {"invoice_id": order["invoice_id"],"subscription_id": order["subscription_id"],"order_id": order["id"], "approval_url": order["links"][1]["href"]}
 

@router.post("/capture-payment/{order_id}")
async def capture_order(order_id: str):
    # capture = await capture_paypal_order(order_id)
    # if "id" not in capture:
    #     raise HTTPException(status_code=400, detail="Failed to capture PayPal order")
    # paypal_order_id=capture["id"]
  
    captured = await get_payment_details_update(order_id)
    # log.info(f"captured.get('id') = {captured.get('id')}")
    ress=await Transactions.save_paypal_response_to_db(order_id, captured)
    return ress


@router.get("/payment-details/{order_id}")
async def get_payment_details(order_id: str):
    capture = await get_payment_details_update(order_id)
    if "id" not in capture:
        raise HTTPException(status_code=400, detail="Failed to capture PayPal order")
    return {"order_id": capture["id"], "status": capture["status"]}


    # access_token = get_paypal_access_token()
    # url = f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}"
    # headers = {
    #     "Content-Type": "application/json",
    #     "Authorization": f"Bearer {access_token}",
    # }

    # response = requests.get(url, headers=headers)
    # if response.status_code != 200:
    #     raise HTTPException(status_code=response.status_code, detail="Failed to fetch order details")
    # return response.json()

############################
# Create Folder
############################
@router.post("/")
def create_subscription(form_data: SubscriptionForm, user=Depends(get_verified_user)):
     
    try:
        plan = Subscriptions.insert_new_subscription(user.id, form_data)
        return plan
    except Exception as e:
        log.exception(e)
        log.error("Error creating folder")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT("Error creating folder"),
        )
        
############################
# Get Plan
############################

@router.get("/", response_model=list[SubscriptionModel])
async def get_user_subscription(user=Depends(get_verified_user)):
    subscriptions = Subscriptions.get_subscriptions(user.id)
    log.info(f"================ {subscriptions}")
    if subscriptions:
        return [
            SubscriptionResponse(**subscription.model_dump())
            for subscription in subscriptions
        ]
            
        # return plans
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )

############################
# Get Plan By Id
############################

@router.get("/{id}", response_model=Optional[SubscriptionModel])
async def get_subscription_by_id(id: str, user=Depends(get_verified_user)):
    subscription = Subscriptions.get_subscription_by_id(id)
    if subscription:
        return SubscriptionResponse(**subscription.model_dump())
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )

############################
# Update Plan By Id
############################




@router.put("/{id}")
async def update_subscription_by_id(
    id: str, form_data: SubscriptionForm, user=Depends(get_verified_user)
):
    subscription = Subscriptions.get_subscription_by_id(id)
    if subscription:
        try:
            subscription = Subscriptions.update_subscription(
                id, form_data
            )
            if subscription:
                return SubscriptionResponse(**subscription.model_dump())
            else:
                raise Exception(f"Error updating folder: {id}")
        except Exception as e:
            log.exception(e)
            log.error(f"Error updating folder: {id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES.DEFAULT("Error updating folder"),
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )

############################
# Delete Plan By Id
############################

@router.delete("/{id}")
async def delete_subscription_by_id(id: str, user=Depends(get_verified_user)):
    subscription = Subscriptions.get_subscription_by_id(id)
    if subscription:
        try:
            result = Subscriptions.delete_subscription_by_id(id)
            if result:
                return result
            else:
                raise Exception("Error deleting subscription")
        except Exception as e:
            log.exception(e)
            log.error(f"Error deleting subscription: {id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES.DEFAULT("Error deleting subscription"),
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )

