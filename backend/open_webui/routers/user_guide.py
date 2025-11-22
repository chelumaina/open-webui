"""
Payment router for handling Paystack payments and subscriptions
"""
import logging 
from fastapi import APIRouter, HTTPException, Request, status, Response
from open_webui.env import SRC_LOG_LEVELS

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pathlib import Path
import json

log = logging.getLogger(__name__)
 
##########################################
#
# Features functions
#
##########################################


router = APIRouter()
# 1) mount static folder at /static
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# router.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@router.get("/user_guide")
async def get_user_guide(request: Request, response: Response):
    """Load all active user_guide"""
    filename="../static/json_content.json"
    # file_path = STATIC_DIR / filename
    print(" filename:", filename)
    try:
        
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    return JSONResponse(content=data)

    # try:
    #     return [{"message": "User guide endpoint"}]
    # except Exception as e:
    #     log.error(f"Error loading user_guide: {str(e)}")
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"{str(e)}"
    #     )
        
@router.get("/user_guide/{slug}")
async def get_user_guide( slug: str ):

    try:
        # Get transaction from database
        return {"message": f"User guide for {slug}"}
            
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Payment verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while verifying payment"
        )
       