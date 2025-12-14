"""create analytics_events table

Revision ID: 202511290322
Revises:4af623372c9d
Create Date: 2025-11-29
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '202511290322'
down_revision: Union[str, None] = 'b10670c03dd5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('analytics_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('section_id', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', NOW())"), nullable=False),
        sa.Column('path', sa.String(), nullable=False),
        sa.Column('full_url', sa.String(), nullable=False),
        sa.Column('query', postgresql.JSONB(astext_type=sa.Text()), default=dict),
        sa.Column('user_agent', sa.String(), nullable=False),
        sa.Column('viewport', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('screen', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('language', sa.String(length=10), nullable=False),
        sa.Column('referrer', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', NOW())"), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analytics_events_section_id'), 'analytics_events', ['section_id'])
    op.create_index(op.f('ix_analytics_events_path'), 'analytics_events', ['path'])
    op.create_index(op.f('ix_analytics_events_timestamp'), 'analytics_events', ['timestamp'])

def downgrade():
    op.drop_index(op.f('ix_analytics_events_timestamp'), table_name='analytics_events')
    op.drop_index(op.f('ix_analytics_events_path'), table_name='analytics_events')
    op.drop_index(op.f('ix_analytics_events_section_id'), table_name='analytics_events')
    op.drop_table('analytics_events')