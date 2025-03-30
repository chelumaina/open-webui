from fastapi import FastAPI, HTTPException
from open_webui.utils.webhook_handlers import create_paypal_order, capture_paypal_order
from fastapi import APIRouter, Depends, HTTPException, Request, status

# app = FastAPI()
router = APIRouter()

@router.post("/create-payment")
async def create_order(amount: str = "10.00"):
    order = await create_paypal_order(amount)
    print(order)
    if "id" not in order:
        raise HTTPException(status_code=400, detail="Failed to create PayPal order")
    return {"order_id": order["id"], "approval_url": order["links"][1]["href"]}

@router.post("/capture-payment/{order_id}")
async def capture_order(order_id: str):
    capture = await capture_paypal_order(order_id)
    if "id" not in capture:
        raise HTTPException(status_code=400, detail="Failed to capture PayPal order")
    return {"order_id": capture["id"], "status": capture["status"]}
