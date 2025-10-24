import time
from typing import Literal, Optional
from zoneinfo import ZoneInfo

from open_webui.internal.db import Base, JSONField, get_db


from open_webui.env import DATABASE_USER_ACTIVE_STATUS_UPDATE_INTERVAL
from open_webui.models.chats import Chats
from open_webui.models.groups import Groups
from open_webui.utils.misc import throttle
from fastapi import FastAPI, Depends, HTTPException


from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Column, String, Text, Date
from sqlalchemy import or_
from datetime import datetime, timedelta, date, timezone

from sqlalchemy import (
    create_engine, select, func, String, DateTime, Enum, Index
)
from open_webui.models.payments import PaymentTransaction, UserSubscription
from uuid import UUID 
TZ_LOCAL = ZoneInfo("Africa/Nairobi")

UTC = timezone.utc
# import datetime

####################
# User DB Schema
####################


class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True)
    name = Column(String)

    email = Column(String)
    username = Column(String(50), nullable=True)

    role = Column(String)
    profile_image_url = Column(Text)

    bio = Column(Text, nullable=True)
    gender = Column(Text, nullable=True)
    date_of_birth = Column(Date, nullable=True)

    info = Column(JSONField, nullable=True)
    settings = Column(JSONField, nullable=True)

    api_key = Column(String, nullable=True, unique=True)
    oauth_sub = Column(Text, unique=True)

    last_active_at = Column(BigInteger)

    updated_at = Column(BigInteger)
    created_at = Column(BigInteger)



class UserSettings(BaseModel):
    ui: Optional[dict] = {}
    model_config = ConfigDict(extra="allow")
    pass


class UserModel(BaseModel):
    id: str
    name: str

    email: str
    username: Optional[str] = None

    role: str = "pending"
    profile_image_url: str

    bio: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None

    info: Optional[dict] = None
    settings: Optional[UserSettings] = None

    api_key: Optional[str] = None
    oauth_sub: Optional[str] = None

    last_active_at: int  # timestamp in epoch
    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch

    model_config = ConfigDict(from_attributes=True)


####################
# Forms
####################


class UpdateProfileForm(BaseModel):
    profile_image_url: str
    name: str
    bio: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None


class UserListResponse(BaseModel):
    users: list[UserModel]
    total: int


class UserInfoResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str


class UserIdNameResponse(BaseModel):
    id: str
    name: str


class UserInfoListResponse(BaseModel):
    users: list[UserInfoResponse]
    total: int


class UserIdNameListResponse(BaseModel):
    users: list[UserIdNameResponse]
    total: int


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    profile_image_url: str


class UserNameResponse(BaseModel):
    id: str
    name: str
    role: str
    profile_image_url: str


class UserRoleUpdateForm(BaseModel):
    id: str
    role: str


class UserUpdateForm(BaseModel):
    role: str
    name: str
    email: str
    profile_image_url: str
    password: Optional[str] = None
class ValidityResponse(BaseModel):
    user_id: UUID
    valid: bool
    source: Optional[Literal["subscription", "payment"]] = None
    now_utc: datetime
    valid_until_utc: Optional[datetime] = None
    valid_until_nairobi: Optional[datetime] = None
    grace_days: int

class UsersTable:
    def insert_new_user(
        self,
        id: str,
        name: str,
        email: str,
        profile_image_url: str = "/user.png",
        role: str = "pending",
        oauth_sub: Optional[str] = None,
    ) -> Optional[UserModel]:
        with get_db() as db:
            user = UserModel(
                **{
                    "id": id,
                    "name": name,
                    "email": email,
                    "role": role,
                    "profile_image_url": profile_image_url,
                    "last_active_at": int(time.time()),
                    "created_at": int(time.time()),
                    "updated_at": int(time.time()),
                    "oauth_sub": oauth_sub,
                }
            )
            result = User(**user.model_dump())
            db.add(result)
            db.commit()
            db.refresh(result)
            if result:
                return user
            else:
                return None

    def get_user_by_id(self, id: str) -> Optional[UserModel]:
        try:
            with get_db() as db:
                user = db.query(User).filter_by(id=id).first()
                return UserModel.model_validate(user)
        except Exception:
            return None
    
    def is_user_subscription_valid(self, user_id: str, ) -> Optional[bool]:
        try:
            # with get_db() as db:
            #     # user = db.query(User).filter_by(id=id).first()
            #     # return UserModel.model_validate(user)
            #     sub = (
            #         db.query(Subscription)
            #         .filter(
            #             Subscription.customer_id == user_id,
            #             Subscription.status == "active",
            #             Subscription.end_date >= datetime.utcnow(),
            #         )
            #         .first()
            #     )
            #     return sub is not None
            return True 

        except Exception:
            return False
    def _now_utc(self) -> datetime:
        return datetime.now(UTC)

    def is_valid_monthly_subscription(
        self,
        user_id: UUID,
        grace_days: int = 0
    ):
        if grace_days < 0 or grace_days > 14:
            raise HTTPException(400, detail="grace_days must be between 0 and 14")

        valid, valid_until_utc, source = self.check_valid_monthly(user_id, grace_days=grace_days)
        return valid
        # now = self._now_utc()
       
        # valid_until_local = valid_until_utc.astimezone(TZ_LOCAL) if valid_until_utc else None

        # return ValidityResponse(
        #     user_id=user_id,
        #     valid=bool(valid),
        #     source=source,
        #     now_utc=now,
        #     valid_until_utc=valid_until_utc,
        #     valid_until_nairobi=valid_until_local,
        #     grace_days=grace_days,
        # )
        
        
    def check_valid_monthly(self, user_id: str, grace_days: int = 0) -> tuple[bool, Optional[datetime], Optional[str]]:
        """
        Returns: (is_valid, valid_until_utc, source)
        source = 'subscription' | 'payment' | None
        """
        with get_db() as db:
            VALID_STATUSES = ["active", "trialing"]
            now = self._now_utc()

            # 1) Try user_subscriptions (trial_end or current_period_end)
            valid_until_expr = func.coalesce(UserSubscription.trial_end, UserSubscription.current_period_end).label("valid_until")
            row = db.execute(
                select(valid_until_expr)
                .where(
                    UserSubscription.user_id == user_id,
                    UserSubscription.billing_cycle == "monthly",
                    UserSubscription.status.in_(VALID_STATUSES),
                    valid_until_expr.is_not(None),
                )
                .order_by(valid_until_expr.desc())
                .limit(1)
            ).first()

            if row and row[0]:
                # Ensure timezone consistency for comparison
                db_datetime = row[0]
                if db_datetime.tzinfo is None:
                    # If database datetime is naive, assume it's UTC
                    db_datetime = db_datetime.replace(tzinfo=UTC)
                valid_until = db_datetime + timedelta(days=grace_days)
                return (now <= valid_until, db_datetime, "subscription")

            # 2) Fallback to latest successful monthly payment -> paid_at + 1 month (Python-side calculation)
            row2 = db.execute(
                select(PaymentTransaction.paid_at)
                .where(
                    PaymentTransaction.user_id == user_id,
                    PaymentTransaction.status == "success",
                    PaymentTransaction.billing_cycle == "monthly",
                    PaymentTransaction.paid_at.is_not(None),
                )
                .order_by(PaymentTransaction.paid_at.desc())
                .limit(1)
            ).first()

            if row2 and row2[0]:
                # Add 1 month to the payment date using Python datetime arithmetic
                paid_at = row2[0]
                # Ensure timezone consistency for paid_at
                if paid_at.tzinfo is None:
                    # If database datetime is naive, assume it's UTC
                    paid_at = paid_at.replace(tzinfo=UTC)
                
                if paid_at.month == 12:
                    valid_until_base = paid_at.replace(year=paid_at.year + 1, month=1)
                else:
                    valid_until_base = paid_at.replace(month=paid_at.month + 1)
                
                valid_until = valid_until_base + timedelta(days=grace_days)
                return (now <= valid_until, valid_until_base, "payment")

        return (False, None, None)

    def get_user_by_api_key(self, api_key: str) -> Optional[UserModel]:
        try:
            with get_db() as db:
                user = db.query(User).filter_by(api_key=api_key).first()
                return UserModel.model_validate(user)
        except Exception:
            return None

    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        try:
            with get_db() as db:
                user = db.query(User).filter_by(email=email).first()
                return UserModel.model_validate(user)
        except Exception:
            return None

    def get_user_by_oauth_sub(self, sub: str) -> Optional[UserModel]:
        try:
            with get_db() as db:
                user = db.query(User).filter_by(oauth_sub=sub).first()
                return UserModel.model_validate(user)
        except Exception:
            return None

    def get_users(
        self,
        filter: Optional[dict] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> dict:
        with get_db() as db:
            query = db.query(User)

            if filter:
                query_key = filter.get("query")
                if query_key:
                    query = query.filter(
                        or_(
                            User.name.ilike(f"%{query_key}%"),
                            User.email.ilike(f"%{query_key}%"),
                        )
                    )

                order_by = filter.get("order_by")
                direction = filter.get("direction")

                if order_by == "name":
                    if direction == "asc":
                        query = query.order_by(User.name.asc())
                    else:
                        query = query.order_by(User.name.desc())
                elif order_by == "email":
                    if direction == "asc":
                        query = query.order_by(User.email.asc())
                    else:
                        query = query.order_by(User.email.desc())

                elif order_by == "created_at":
                    if direction == "asc":
                        query = query.order_by(User.created_at.asc())
                    else:
                        query = query.order_by(User.created_at.desc())

                elif order_by == "last_active_at":
                    if direction == "asc":
                        query = query.order_by(User.last_active_at.asc())
                    else:
                        query = query.order_by(User.last_active_at.desc())

                elif order_by == "updated_at":
                    if direction == "asc":
                        query = query.order_by(User.updated_at.asc())
                    else:
                        query = query.order_by(User.updated_at.desc())
                elif order_by == "role":
                    if direction == "asc":
                        query = query.order_by(User.role.asc())
                    else:
                        query = query.order_by(User.role.desc())

            else:
                query = query.order_by(User.created_at.desc())

            if skip:
                query = query.offset(skip)
            if limit:
                query = query.limit(limit)

            users = query.all()
            return {
                "users": [UserModel.model_validate(user) for user in users],
                "total": db.query(User).count(),
            }

    def get_users_by_user_ids(self, user_ids: list[str]) -> list[UserModel]:
        with get_db() as db:
            users = db.query(User).filter(User.id.in_(user_ids)).all()
            return [UserModel.model_validate(user) for user in users]

    def get_num_users(self) -> Optional[int]:
        with get_db() as db:
            return db.query(User).count()

    def has_users(self) -> bool:
        with get_db() as db:
            return db.query(db.query(User).exists()).scalar()

    def get_first_user(self) -> UserModel:
        try:
            with get_db() as db:
                user = db.query(User).order_by(User.created_at).first()
                return UserModel.model_validate(user)
        except Exception:
            return None

    def get_user_webhook_url_by_id(self, id: str) -> Optional[str]:
        try:
            with get_db() as db:
                user = db.query(User).filter_by(id=id).first()

                if user.settings is None:
                    return None
                else:
                    return (
                        user.settings.get("ui", {})
                        .get("notifications", {})
                        .get("webhook_url", None)
                    )
        except Exception:
            return None

    def update_user_role_by_id(self, id: str, role: str) -> Optional[UserModel]:
        try:
            with get_db() as db:
                db.query(User).filter_by(id=id).update({"role": role})
                db.commit()
                user = db.query(User).filter_by(id=id).first()
                return UserModel.model_validate(user)
        except Exception:
            return None

    def update_user_profile_image_url_by_id(
        self, id: str, profile_image_url: str
    ) -> Optional[UserModel]:
        try:
            with get_db() as db:
                db.query(User).filter_by(id=id).update(
                    {"profile_image_url": profile_image_url}
                )
                db.commit()

                user = db.query(User).filter_by(id=id).first()
                return UserModel.model_validate(user)
        except Exception:
            return None

    @throttle(DATABASE_USER_ACTIVE_STATUS_UPDATE_INTERVAL)
    def update_user_last_active_by_id(self, id: str) -> Optional[UserModel]:
        try:
            with get_db() as db:
                db.query(User).filter_by(id=id).update(
                    {"last_active_at": int(time.time())}
                )
                db.commit()

                user = db.query(User).filter_by(id=id).first()
                return UserModel.model_validate(user)
        except Exception:
            return None

    def update_user_oauth_sub_by_id(
        self, id: str, oauth_sub: str
    ) -> Optional[UserModel]:
        try:
            with get_db() as db:
                db.query(User).filter_by(id=id).update({"oauth_sub": oauth_sub})
                db.commit()

                user = db.query(User).filter_by(id=id).first()
                return UserModel.model_validate(user)
        except Exception:
            return None

    def update_user_by_id(self, id: str, updated: dict) -> Optional[UserModel]:
        try:
            with get_db() as db:
                db.query(User).filter_by(id=id).update(updated)
                db.commit()

                user = db.query(User).filter_by(id=id).first()
                return UserModel.model_validate(user)
                # return UserModel(**user.dict())
        except Exception as e:
            print(e)
            return None

    def update_user_settings_by_id(self, id: str, updated: dict) -> Optional[UserModel]:
        try:
            with get_db() as db:
                user_settings = db.query(User).filter_by(id=id).first().settings

                if user_settings is None:
                    user_settings = {}

                user_settings.update(updated)

                db.query(User).filter_by(id=id).update({"settings": user_settings})
                db.commit()

                user = db.query(User).filter_by(id=id).first()
                return UserModel.model_validate(user)
        except Exception:
            return None

    def delete_user_by_id(self, id: str) -> bool:
        try:
            # Remove User from Groups
            Groups.remove_user_from_all_groups(id)

            # Delete User Chats
            result = Chats.delete_chats_by_user_id(id)
            if result:
                with get_db() as db:
                    # Delete User
                    db.query(User).filter_by(id=id).delete()
                    db.commit()

                return True
            else:
                return False
        except Exception:
            return False

    def update_user_api_key_by_id(self, id: str, api_key: str) -> bool:
        try:
            with get_db() as db:
                result = db.query(User).filter_by(id=id).update({"api_key": api_key})
                db.commit()
                return True if result == 1 else False
        except Exception:
            return False

    def get_user_api_key_by_id(self, id: str) -> Optional[str]:
        try:
            with get_db() as db:
                user = db.query(User).filter_by(id=id).first()
                return user.api_key
        except Exception:
            return None

    def get_valid_user_ids(self, user_ids: list[str]) -> list[str]:
        with get_db() as db:
            users = db.query(User).filter(User.id.in_(user_ids)).all()
            return [user.id for user in users]

    def get_super_admin_user(self) -> Optional[UserModel]:
        with get_db() as db:
            user = db.query(User).filter_by(role="admin").first()
            if user:
                return UserModel.model_validate(user)
            else:
                return None


Users = UsersTable()
