from fastapi import FastAPI, HTTPException
from open_webui.utils.webhook_handlers import create_paypal_order, capture_paypal_order
from fastapi import APIRouter, Depends, HTTPException, Request, status
import logging
from open_webui.utils.auth import get_verified_user
from open_webui.env import SRC_LOG_LEVELS
from typing import Optional

from open_webui.models.subscriptions import InvoiceModel, InvoiceForm, Invoices, InvoiceResponse
from open_webui.constants import ERROR_MESSAGES

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

# app = FastAPI()
router = APIRouter()


############################
# Create Folder
############################
@router.post("/")
def create_plan(form_data: InvoiceForm, user=Depends(get_verified_user)):
     
    try:
        plan = Invoices.insert_new_invoice(user.id, form_data)
        return plan
    except Exception as e:
        log.exception(e)
        log.error("Error creating folder")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT("Error creating folder"),
        )



############################
# Get Invoice
############################
@router.get("/", response_model=list[InvoiceModel])
async def get_user_invoice(user=Depends(get_verified_user)):
    invoices = Invoices.get_invoices(user.id)
    if invoices:
        return [
            InvoiceResponse(**invoice.model_dump())
            for invoice in invoices
        ]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )
        

############################
# Get Invoice By Id
############################
@router.get("/{id}", response_model=Optional[InvoiceModel])
async def get_invoice_by_id(id: str, user=Depends(get_verified_user)):
    invoice = Invoices.get_invoice_by_id(id)
    if invoice:
        return InvoiceResponse(**invoice.model_dump())
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )



############################
# Update Invoice By Id
############################
@router.put("/{id}")
async def update_invoice_by_id(
    id: str, form_data: InvoiceForm, user=Depends(get_verified_user)
):
    invoice = Invoices.get_invoice_by_id(id)
    if invoice:
        try:
            invoice = Invoices.update_invoice(
                id, form_data
            )
            if invoice:
                return InvoiceResponse(**invoice.model_dump())
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
# Delete Invoice By Id
############################
@router.delete("/{id}")
async def delete_invoice_by_id(id: str, user=Depends(get_verified_user)):
    invoice = Invoices.get_invoice_by_id(id)
    if invoice:
        try:
            result = Invoices.delete_invoice_by_id(id)
            if result:
                return result
            else:
                raise Exception("Error deleting invoice")
        except Exception as e:
            log.error(f"Error deleting invoice: {id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES.DEFAULT("Error deleting invoice"),
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )
