"""Add messages table

Revision ID: 003
Revises: 002
Create Date: 2026-02-07

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TIMESTAMP, JSON

# revision identifiers, used by Alembic
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create messages table."""
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('conversation_id', sa.Integer(), sa.ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', JSON, nullable=True),
        sa.Column('timestamp', TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False),
    )

    # Create indexes for performance
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_messages_timestamp', 'messages', ['timestamp'], postgresql_ops={'timestamp': 'DESC'})


def downgrade() -> None:
    """Drop messages table."""
    op.drop_index('idx_messages_timestamp', table_name='messages')
    op.drop_index('idx_messages_conversation_id', table_name='messages')
    op.drop_table('messages')
