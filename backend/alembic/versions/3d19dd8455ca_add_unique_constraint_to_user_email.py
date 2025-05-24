"""Add unique constraint to user.email

Revision ID: 3d19dd8455ca
Revises: 397b1fe1a958
Create Date: 2025-05-24 22:23:42.335640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d19dd8455ca'
down_revision: Union[str, None] = '397b1fe1a958'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        constraint_name='uq_user_email',
        table_name='users',
        columns=['email']
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        constraint_name='uq_user_email',
        table_name='users',
        type_='unique'
    )
