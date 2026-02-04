"""Add priority and due_date to tasks table

Revision ID: 002_add_task_priority_due_date
Revises: 001_add_conversation_message_tables
Create Date: 2026-02-05 02:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers
revision: str = '002_add_task_priority_due_date'
down_revision: Union[str, None] = '001_add_conversation_message_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add columns to tasks table
    # Check if tasks table exists (it should, but created via SQLModel create_all probably)
    op.add_column('tasks', sa.Column('due_date', sa.String(length=50), nullable=True))
    op.add_column('tasks', sa.Column('priority', sa.String(length=20), nullable=True, server_default='medium'))


def downgrade() -> None:
    op.drop_column('tasks', 'priority')
    op.drop_column('tasks', 'due_date')
