"""add paystack tables

Revision ID: 4af623372c9d
Revises: a490017e16fa
Create Date: 2025-11-01 11:06:38.375522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import open_webui.internal.db


# revision identifiers, used by Alembic.
revision: str = '4af623372c9d'
down_revision: Union[str, None] = 'a490017e16fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # Creating the 'payment_transactions' table
    print("Creating payment_transactions table")
    pass
    # op.create_table(
    #     "payment_transactions",
    #     sa.Column("id", sa.UUID(), nullable=False, primary_key=True, unique=True),
    #     sa.Column("user_id", sa.Text(), nullable=True),
    #     sa.Column("reference", sa.Text(), nullable=True),
    #     sa.Column("amount", sa.Float(), nullable=True),
    #     sa.Column("currency", sa.String(), nullable=True),
    #     sa.Column("plan_id", sa.String(), nullable=True),
    #     sa.Column("plan_name", sa.String(), nullable=True),
    #     sa.Column("billing_cycle", sa.String(), nullable=True),
    #     sa.Column("status", sa.String(), nullable=True),
    #     sa.Column("paystack_reference", sa.String(), nullable=True),
    #     sa.Column("paystack_status", sa.String(), nullable=True),
    #     sa.Column("gateway_response", sa.Text(), nullable=True),
    #     sa.Column("gateway_response_data", sa.Text(), nullable=True),
    #     sa.Column("group_id", sa.String(), nullable=True),
    #     sa.Column("paid_at", sa.DateTime(), nullable=True),
    #     sa.Column("created_at", sa.DateTime(), nullable=True),
    #     sa.Column("updated_at", sa.DateTime(), nullable=True), 
    # )
    
    # print("Creating user_subscriptions table")
    # op.create_table(
    #     "user_subscriptions",
    #     sa.Column("id", sa.UUID(), nullable=False, primary_key=True, unique=True),
    #     sa.Column("user_id", sa.Text(), nullable=False),
    #     sa.Column("plan_id", sa.String(), nullable=False),
    #     sa.Column("plan_name", sa.String(), nullable=False),
    #     sa.Column("status", sa.String(), nullable=True),
    #     sa.Column("amount", sa.Float(), nullable=False),
    #     sa.Column("currency", sa.String(), nullable=False),
    #     sa.Column("group_id", sa.String(), nullable=True),
    #     sa.Column("billing_cycle", sa.String(), nullable=True),
    #     sa.Column("started_at", sa.DateTime(), nullable=True),
    #     sa.Column("expires_at", sa.DateTime(), nullable=True),
    #     sa.Column("trial_end", sa.DateTime(timezone=True), nullable=True),
    #     sa.Column("current_period_end", sa.DateTime(timezone=True), nullable=True),
    #     sa.Column("transaction_reference", sa.String(), nullable=False),
    #     sa.Column("created_at", sa.DateTime(), nullable=True),
    #     sa.Column("updated_at", sa.DateTime(), nullable=True),
    # )
     
def downgrade() -> None:
    pass
    # op.drop_table("user_subscriptions")
    # op.drop_table("payment_transactions")
