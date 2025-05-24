"""add customer id to users

Revision ID: 397b1fe1a958
Revises: 55365c358b4b
Create Date: 2025-05-24 20:22:20.132016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '397b1fe1a958'
down_revision: Union[str, None] = '55365c358b4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'users',
        sa.Column(
            'customer_id', sa.String(), nullable=True
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'customer_id')
