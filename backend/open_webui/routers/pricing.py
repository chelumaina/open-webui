# main.py or routers/pricing.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from functools import lru_cache
from backend.open_webui.storage.plans import PLANS
from open_webui.models.pricing import PricingPlan

# router = APIRouter(prefix="/pricing", tags=["pricing"])
router = APIRouter()
# Cache the plans for 10 minutes (plans rarely change)
@lru_cache()
def get_cached_plans() -> list[PricingPlan]:
    return PLANS

@router.get("/plans",response_model=list[PricingPlan],summary="Get all pricing plans",response_description="List of available subscription plans",)
async def get_pricing_plans(request: Request):
    # Optional: add ?currency=EUR → return converted prices in the future
    plans = get_cached_plans()
    return JSONResponse(content=[plan.model_dump(by_alias=True) for plan in plans])