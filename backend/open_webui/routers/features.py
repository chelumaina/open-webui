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
import uuid
from dateutil.relativedelta import relativedelta

import requests
from fastapi import APIRouter, Depends, HTTPException, Request, status, Response

from open_webui.internal.db import Base, get_db
from open_webui.models.models import Model
from open_webui.models.groups import Group, Groups

from open_webui.models.users import Users
from open_webui.utils.auth import get_admin_user, get_verified_user

from open_webui.models.features import PagesTable, FeaturesTable, Feature, FeatureRequest, FeatureResponse,  PageContent, PageResponse, PageRequest
from open_webui.env import SRC_LOG_LEVELS


log = logging.getLogger(__name__)
pageTable=PagesTable()
##########################################
#
# Features functions
#
##########################################


router = APIRouter()


@router.get("/features", response_model=FeatureResponse)
async def get_features(request: Request, response: Response):
    """Load all active features"""
    try:
        # Get transaction from database
        features=[]
        with get_db() as db:
            features = db.query(Feature).all()
            
        #     features = db.query(Feature).all()
            
            if not features:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Features not found"
                )
            return [FeatureResponse.from_orm(feature) for feature in features] or []
    
  
    except Exception as e:
        log.error(f"Error loading features: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(e)}"
        )
        
@router.get("/features/{slug}", response_model=FeatureResponse)
async def get_feature( slug: str ):

    try:
        # Get transaction from database
        with get_db() as db: 
            feature = db.query(Feature).filter(Feature.id == slug).first()
           

            if not feature:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Features not found"
                )
            feature_response = FeatureResponse.from_orm(feature)
            return feature_response               
           
            
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Payment verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while verifying payment"
        )
@router.post("/features", response_model=FeatureResponse)
async def create_feature(feature_request: FeatureRequest, user=Depends(get_admin_user)):
    """Create a new feature"""
    try:
        with get_db() as db:
            new_feature = Feature(**feature_request.dict())
            db.add(new_feature)
            db.commit()
            db.refresh(new_feature)
            return FeatureResponse.from_orm(new_feature)
    except Exception as e:
        log.error(f"Error creating feature: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating feature"
        )
        
        
        
##########################################
#
# PageContent routes
#
##########################################


@router.get("/pages", response_model=Optional[list[PageResponse]])
async def get_pages():
    """Load all active features"""
    try:
        return pageTable.list_pages()
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Error loading features: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while loading features"
        )
        
@router.get("/page/{slug}", response_model=PageResponse)
async def get_page(slug: str):
    try:
        # Get transaction from database
        page= pageTable.get_page_content_using_slug(slug)
        return PageResponse.model_validate(page)
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"Payment verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while loading page"
        )


@router.post("/pages", response_model=PageResponse)
async def create_page(page_request: PageRequest, user=Depends(get_admin_user)):
    """Create a new page"""
    try:
        # dict_data=**page_request.dict()
        log.info(f"Creating page with title: {page_request}")
        page_data = page_request.dict()
        with get_db() as db:
            new_page = PageContent(**page_data)
            db.add(new_page)
            db.commit()
            db.refresh(new_page)
            return PageResponse.from_orm(new_page)
    except Exception as e:
        log.error(f"Error creating page: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating page"
        )
        
       