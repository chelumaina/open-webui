"""create payment_transactions

Revision ID: a28bdf9d9103
Revises: a5c220713937
Create Date: 2025-10-23 12:30:47.957906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import open_webui.internal.db


# revision identifiers, used by Alembic.
revision: str = 'a28bdf9d9103'
down_revision: Union[str, None] = 'a5c220713937'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
