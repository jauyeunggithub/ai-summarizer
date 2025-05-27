"""add status and is deleted columns

Revision ID: 11d999cfaf47
Revises: 6492b6f85341
Create Date: 2025-05-27 00:01:20.800527

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '11d999cfaf47'
down_revision: Union[str, None] = '6492b6f85341'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column(
        'is_active', sa.Boolean(), nullable=True))
    op.add_column('summaries', sa.Column(
        'is_deleted', sa.Boolean(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'is_active')
    op.drop_column('summaries', 'is_deleted')
