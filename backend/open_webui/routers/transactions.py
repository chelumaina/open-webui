from fastapi import FastAPI, HTTPException
from open_webui.utils.webhook_handlers import create_paypal_order, capture_paypal_order
from fastapi import APIRouter, Depends, HTTPException, Request, status
import logging
from open_webui.utils.auth import get_verified_user
from open_webui.env import SRC_LOG_LEVELS
from typing import Optional

from open_webui.models.subscriptions import TransactionModel, TransactionForm, Transactions, TransactionResponse
from open_webui.constants import ERROR_MESSAGES

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

# app = FastAPI()
router = APIRouter()

############################
# Create Folder
############################
@router.post("/")
def create_transaction(form_data: TransactionForm, user=Depends(get_verified_user)):
     
    try:
        plan = Transactions.insert_new_transaction(user.id, form_data)
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

@router.get("/", response_model=list[TransactionModel])
async def get_user_transaction(user=Depends(get_verified_user)):
    transactions = Transactions.get_transactions(user.id)
    log.info(f"================ {transactions}")
    if transactions:
        return [
            TransactionResponse(**transaction.model_dump())
            for transaction in transactions
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

@router.get("/{id}", response_model=Optional[TransactionModel])
async def get_transaction_by_id(id: str, user=Depends(get_verified_user)):
    transaction = Transactions.get_transaction_by_id(id)
    if transaction:
        return TransactionResponse(**transaction.model_dump())
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )

############################
# Update Plan By Id
############################




@router.put("/{id}")
async def update_transaction_by_id(
    id: str, form_data: TransactionForm, user=Depends(get_verified_user)
):
    transaction = Transactions.get_transaction_by_id(id)
    if transaction:
        try:
            transaction = Transactions.update_transaction(
                id, form_data
            )
            if transaction:
                return TransactionResponse(**transaction.model_dump())
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
async def delete_transaction_by_id(id: str, user=Depends(get_verified_user)):
    transaction = Transactions.get_transaction_by_id(id)
    if transaction:
        try:
            result = Transactions.delete_transaction_by_id(id)
            if result:
                return result
            else:
                raise Exception("Error deleting transaction")
        except Exception as e:
            log.exception(e)
            log.error(f"Error deleting transaction: {id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES.DEFAULT("Error deleting transaction"),
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )

