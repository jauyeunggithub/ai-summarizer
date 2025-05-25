"""add status column to summaries table

Revision ID: 7ee4d5b00de0
Revises: 7db10c84a9ee
Create Date: 2025-05-25 19:49:30.684209

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ee4d5b00de0'
down_revision: Union[str, None] = '7db10c84a9ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('summaries', sa.Column(
        'status', sa.String(), nullable=True))
    op.execute("""
        ALTER TABLE summaries ADD CONSTRAINT check_summaries_status
        CHECK (status IN ('processing', 'complete', 'error'))
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE users DROP CONSTRAINT check_summaries_status")
    op.drop_column('summaries', 'status')
