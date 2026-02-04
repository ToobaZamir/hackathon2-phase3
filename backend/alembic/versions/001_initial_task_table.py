"""Initial migration for Task table

Revision ID: 001_initial_task_table
Revises:
Create Date: 2026-01-09 20:00:00

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial_task_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create tasks table
    op.create_table(
        'task',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=1000), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, default=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('idx_tasks_user_id', 'task', ['user_id'])
    op.create_index('idx_tasks_completed', 'task', ['completed'])
    op.create_index('idx_tasks_user_completed', 'task', ['user_id', 'completed'])


def downgrade():
    # Drop indexes
    op.drop_index('idx_tasks_user_completed')
    op.drop_index('idx_tasks_completed')
    op.drop_index('idx_tasks_user_id')

    # Drop tasks table
    op.drop_table('task')