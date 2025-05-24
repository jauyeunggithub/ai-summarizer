"""Add summary file name column and populate with last path segment

Revision ID: 7db10c84a9ee
Revises: 3d19dd8455ca
Create Date: 2025-05-24 23:43:50.306301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7db10c84a9ee'
down_revision: Union[str, None] = '3d19dd8455ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('summaries', sa.Column(
        'file_name', sa.String(), nullable=True))
    op.add_column('summaries', sa.Column(
        'description', sa.String(), nullable=True))
    op.execute("""
        UPDATE summaries
        SET file_name = regexp_replace(file_path, '^.*/', '')
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('summaries', 'file_name')
    op.drop_column('summaries', 'description')
