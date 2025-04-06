from fastapi import FastAPI, HTTPException
from open_webui.utils.webhook_handlers import create_paypal_order, capture_paypal_order
from fastapi import APIRouter, Depends, HTTPException, Request, status
import logging
from open_webui.utils.auth import get_verified_user
from open_webui.env import SRC_LOG_LEVELS
from typing import Optional

from open_webui.models.subscriptions import Plan, PlanModel, PlanForm, Plans, PlanResponse
from open_webui.constants import ERROR_MESSAGES

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

# app = FastAPI()
router = APIRouter()


############################
# Create Folder
############################


@router.post("/")
def create_plan(form_data: PlanForm, user=Depends(get_verified_user)):
    plan = Plans.get_plan_by_user_id_and_name(user.id, form_data.name)
    if plan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.DEFAULT("Folder already exists"),
        )
    try:
        plan = Plans.insert_new_plan(user.id, form_data)
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

@router.get("/", response_model=list[PlanModel])
async def get_plans(user=Depends(get_verified_user)):
    plans = Plans.get_plans()
    log.info(f"================ {plans}")
    if plans:
        return [
            PlanResponse(**plan.model_dump())
            for plan in plans
        ]
            
        # return plans
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )
    # return None
    # return [{**plan.model_dump()}
    #     for plan in plans
    # ]

############################
# Get Plan By Id
############################

@router.get("/{id}", response_model=Optional[PlanModel])
async def get_plan_by_id(id: str, user=Depends(get_verified_user)):
    plan = Plans.get_plan_by_id(id)
    if plan:
        return PlanResponse(**plan.model_dump())
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )

############################
# Update Plan By Id
############################


@router.put("/{id}")
async def update_plan_by_id( id: str, form_data: PlanForm, user=Depends(get_verified_user)):
    plan = Plans.get_plan_by_id(id)
    if plan:
        try: 
            # updated_chat = {**plan.model_dump(), **form_data}
            chat = Plans.update_plan(id, form_data)
            return PlanResponse(**chat.model_dump())
             
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
async def delete_plan_by_id(id: str, user=Depends(get_verified_user)):
    plan = Plans.get_plan_by_id(id)
    if plan:
        try:
            deleted = Plans.delete_plan_by_id(id)
            
            if deleted:
                return True
            else:
                raise Exception("Error deleting folder")
        except Exception as e:
            # log.exception(e)
            # log.error(f"Error deleting folder: {id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES.DEFAULT("Error deleting folder"),
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )

