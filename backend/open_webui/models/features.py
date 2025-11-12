
import time, uuid
from typing import List, Optional, Dict, Any

from datetime import datetime

from open_webui.internal.db import Base, get_db

from open_webui.env import DATABASE_USER_ACTIVE_STATUS_UPDATE_INTERVAL
from open_webui.models.chats import Chats
from open_webui.models.groups import Groups
from open_webui.utils.misc import throttle
from pydantic import BaseModel, Field
from sqlalchemy import ARRAY, Column, DateTime, Integer, String, Float, Boolean, Text, UUID, JSON, ARRAY, DateTime, func
from sqlalchemy.orm import (
    declarative_base, Session, sessionmaker, Mapped, mapped_column
)
from sqlalchemy import or_
from sqlmodel import Relationship

# import datetime

####################
# pages DB Schema
####################

class Feature(Base):
    __tablename__ = "page_feature"
    id = Column(UUID, default=uuid.uuid4(), primary_key=True)
    page_id = Column(Integer, index=True, default=0)
    slug=Column(String, index=True, unique=True)
    title = Column(String, index=True)
    subtitle = Column(String, nullable=True)
    content = Column(Text, nullable=True)   # store sanitized HTML or Markdown
    image_path = Column(String, nullable=True)  # S3 key or local path
    icon_name = Column(String, nullable=True)
    order_index = Column(Integer, default=0, index=True)
    
    
    # SEO Fields
    seo_title = Column(String, nullable=False)
    seo_description = Column(Text, nullable=False)
    meta_keywords = Column(ARRAY(String), nullable=True, default=[])
    canonical_url = Column(String, nullable=False)
    meta_robots = Column(String, nullable=False, default="index,follow")
    
    # Configuration Fields
    locale = Column(String, nullable=False, default="en")
    
    # Icon/Image Fields
    svg_icon = Column(Text, nullable=True)
    icon_url = Column(String, nullable=True)
    
    # JSON Fields for Complex Data
    icon_reference = Column(JSON, nullable=True)
    open_graph = Column(JSON, nullable=True)
    twitter_card = Column(JSON, nullable=True)
    structured_data = Column(JSON, nullable=True)
    meta_tags = Column(JSON, nullable=True)
    schema_org_jsonld = Column(JSON, nullable=True)
    
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    

class PageContent(Base):
    __tablename__ = "page_contents"
    id = Column(UUID, default=uuid.uuid4(), primary_key=True)
    
    # Core Content Fields
    title = Column(String, nullable=False, index=True)
    slug = Column(String, nullable=False, unique=True, index=True)
    intro = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    is_published = Column(Boolean, default=False, index=True)

    # SEO Fields
    seo_title = Column(String, nullable=False)
    seo_description = Column(Text, nullable=False)
    meta_keywords = Column(ARRAY(String), nullable=True, default=[])
    canonical_url = Column(String, nullable=False)
    meta_robots = Column(String, nullable=False, default="index,follow")
    
    # Configuration Fields
    locale = Column(String, nullable=False, default="en", index=True)
    order_index = Column(Integer, nullable=False, default=0, index=True)
    
    # Icon/Image Fields
    svg_icon = Column(Text, nullable=True)
    icon_url = Column(String, nullable=True)
    
    # JSON Fields for Complex Data
    icon_reference = Column(JSON, nullable=True)
    open_graph = Column(JSON, nullable=True)
    twitter_card = Column(JSON, nullable=True)
    structured_data = Column(JSON, nullable=True)
    meta_tags = Column(JSON, nullable=True)
    schema_org_jsonld = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), index=True)
    

    # Relationships
    page_features: Mapped[List["Feature"]] = Relationship(back_populates="page_contents")
    
 
# Pydantic models
class FeatureRequest(BaseModel): 
    page_id: int = Field(foreign_key="page_contents.id", index=True)
    title: str
    subtitle: Optional[str] = None
    content: Optional[str] = None   # store sanitized HTML or Markdown
    image_path: Optional[str] = None  # S3 key or local path
    icon_name: Optional[str] = None
    
    
    seo_description: str
    meta_keywords: Optional[List[str]] = []
    canonical_url: str
    meta_robots: str = "index,follow"
    locale: str = "en"
    order_index: int = 0
    svg_icon: Optional[str] = None
    icon_reference: Optional[Dict[str, Any]] = None  # JSON dict
    icon_url: Optional[str] = None
    open_graph: Optional[Dict[str, Any]] = None  # JSON dict
    twitter_card: Optional[Dict[str, Any]] = None  # JSON dict
    structured_data: Optional[Dict[str, Any]] = None  # JSON dict
    meta_tags: Optional[List[Dict[str, Any]]] = None  # JSON list of dicts
    schema_org_jsonld: Optional[Dict[str, Any]] = None  # JSON dict
    
     
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
class PageRequest(BaseModel):
    title: str
    slug: str
    intro: str
    summary: str
    seo_title: str
    is_published: bool = False
    seo_description: str
    meta_keywords: Optional[List[str]] = []
    canonical_url: str
    meta_robots: str = "index,follow"
    locale: str = "en"
    order_index: int = 0
    svg_icon: Optional[str] = None
    icon_reference: Optional[Dict[str, Any]] = None  # JSON dict
    icon_url: Optional[str] = None
    open_graph: Optional[Dict[str, Any]] = None  # JSON dict
    twitter_card: Optional[Dict[str, Any]] = None  # JSON dict
    structured_data: Optional[Dict[str, Any]] = None  # JSON dict
    meta_tags: Optional[List[Dict[str, Any]]] = None  # JSON list of dicts
    schema_org_jsonld: Optional[Dict[str, Any]] = None  # JSON dict
    
    # title: str
    # slug: str = Field(index=True, unique=True)
    # summary: Optional[str] = None
    # intro: Optional[str] = None    # short HTML/Markdown
    # seo_title: Optional[str] = None
    # seo_description: Optional[str] = None
    # is_published: bool = Field(default=False, index=True)
    # locale: Optional[str] = Field(default="en")
    # order_index: int = Field(default=0, index=True)
    # meta_robots: Optional[str] = Field(default="index, follow")
    # meta_keywords: Optional[JSON] = Field(default=[])
    # canonical_url: Optional[str] = Field(default=None)
    # meta_tags: Optional[JSON] = Field(default=[])
    # schema_org_jsonld: Optional[JSON] = Field(default={})
    # structured_data: Optional[JSON] = Field(default={})
    # open_graph: Optional[JSON] = Field(default={})
    # twitter_card: Optional[JSON] = Field(default={})
    # svg_icon: Optional[str] = None
    # icon_reference: Optional[JSON] = Field(default={})
    # icon_url: Optional[str] = None
    
    # created_at: datetime = Field(default_factory=datetime.utcnow)
    # updated_at: datetime = Field(default_factory=datetime.utcnow)
    # page_features: List[FeatureRequest] = []
     

class FeatureResponse(BaseModel):
    id: uuid.UUID
    page_id: int
    title: str
    subtitle: Optional[str] = None
    content: Optional[str] = None   # store sanitized HTML or Markdown
    image_path: Optional[str] = None  # S3 key or local path
    icon_name: Optional[str] = None
    order_index: int
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}

class PageResponse(BaseModel): 
    title: str
    slug: str
    intro: Optional[str] = None    # short HTML/Markdown
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    is_published: bool
    locale: Optional[str]
    order_index: Optional[int]
    created_at: datetime
    updated_at: datetime
    # page_features: List[FeatureResponse] = []
    model_config = {"from_attributes": True}
    
class FeaturesTable:
    def get_feature(self, id: str) -> Optional[FeatureResponse]:
        with get_db() as db:
            page_feature = (
                db.query(Feature).filter_by(id=id).first()
            )
            if page_feature:
                return page_feature
            else:
                 return None
    def list_features(self, page_id: int) -> List[FeatureResponse]:
        with get_db() as db:
            page_features = (
                db.query(Feature)
                .filter_by(page_id=page_id)
                .order_index(Feature.order.asc())
                .all()
            )
            return page_features
        
    def create_feature(self, feature_data: FeatureRequest) -> FeatureResponse:
        with get_db() as db:
            new_feature = Feature(**feature_data.dict())
            db.add(new_feature)
            db.commit()
            db.refresh(new_feature)
            return new_feature
    def update_feature(self, id: str, feature_data: FeatureRequest) -> Optional[FeatureResponse]:
        with get_db() as db:
            page_feature = db.query(Feature).filter_by(id=id).first()
            if page_feature:
                for key, value in feature_data.dict().items():
                    setattr(page_feature, key, value)
                page_feature.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(page_feature)
                return page_feature
            else:
                return None
    def delete_feature(self, id: str) -> bool:
        with get_db() as db:
            page_feature = db.query(Feature).filter_by(id=id).first()
            if page_feature:
                db.delete(page_feature)
                db.commit()
                return True
            else:
                return False

class PagesTable:
    def get_page(self, id: str) -> Optional[PageResponse]:
        with get_db() as db:
            page_content = (
                db.query(PageContent).filter_by(id=id).first()
            )
            if page_content:
                return page_content
            else:
                 return None
             
    def list_pages(self) -> List[PageResponse]:
        with get_db() as db:
            pages = (
                db.query(PageContent)
                .order_index(PageContent.created_at.desc())
                .all()
            )
            return pages
    def create_page(self, page_data: PageRequest) -> PageResponse:
        with get_db() as db:
            new_page = PageContent(**page_data.dict())
            db.add(new_page)
            db.commit()
            db.refresh(new_page)
            return new_page
    def update_page(self, id: str, page_data: PageRequest) -> Optional[PageResponse]:
        with get_db() as db:
            page_content = db.query(PageContent).filter_by(id=id).first()
            if page_content:
                for key, value in page_data.dict().items():
                    setattr(page_content, key, value)
                page_content.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(page_content)
                return page_content
            else:
                return None
    def delete_page(self, id: str) -> bool:
        with get_db() as db:
            page_content = db.query(PageContent).filter_by(id=id).first()
            if page_content:
                db.delete(page_content)
                db.commit()
                return True
            else:
                return False
            
Pages = PagesTable()
Features = FeaturesTable()