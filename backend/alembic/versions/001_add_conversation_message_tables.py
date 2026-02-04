"""Add conversation and message tables

Revision ID: 001_add_conversation_message_tables
Revises:
Create Date: 2026-01-17 15:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from uuid import uuid4
import datetime

# revision identifiers
revision: str = '001_add_conversation_message_tables'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create conversations table
    op.create_table('conversations',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversations_user_id'), 'conversations', ['user_id'])
    op.create_index(op.f('ix_conversations_created_at'), 'conversations', ['created_at'])

    # Create messages table
    op.create_table('messages',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('conversation_id', sa.UUID(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('tool_calls', sa.JSON(), nullable=True),
        sa.Column('tool_responses', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_conversation_id'), 'messages', ['conversation_id'])
    op.create_index(op.f('ix_messages_role'), 'messages', ['role'])
    op.create_index(op.f('ix_messages_timestamp'), 'messages', ['timestamp'])


def downgrade() -> None:
    # Drop messages table
    op.drop_index(op.f('ix_messages_timestamp'), table_name='messages')
    op.drop_index(op.f('ix_messages_role'), table_name='messages')
    op.drop_index(op.f('ix_messages_conversation_id'), table_name='messages')
    op.drop_table('messages')

    # Drop conversations table
    op.drop_index(op.f('ix_conversations_created_at'), table_name='conversations')
    op.drop_index(op.f('ix_conversations_user_id'), table_name='conversations')
    op.drop_table('conversations')