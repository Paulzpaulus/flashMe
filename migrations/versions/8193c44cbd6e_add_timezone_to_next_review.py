"""add timezone to next_review

Revision ID: 8193c44cbd6e
Revises: 
Create Date: 2026-05-21 15:47:51.182864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8193c44cbd6e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create saveddeck table (was missing from DB)
    op.create_table(
        'saveddeck',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('deck_id', sa.Integer(), nullable=False),
        sa.Column('saved_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['deck_id'], ['deck.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('user_id', 'deck_id'),
    )

    # Change next_review in cardprogress from TIMESTAMP to TIMESTAMP WITH TIME ZONE
    op.alter_column(
        'cardprogress',
        'next_review',
        type_=sa.DateTime(timezone=True),
        existing_type=sa.DateTime(timezone=False),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Revert next_review back to TIMESTAMP WITHOUT TIME ZONE
    op.alter_column(
        'cardprogress',
        'next_review',
        type_=sa.DateTime(timezone=False),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
    )

    op.drop_table('saveddeck')
