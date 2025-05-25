"""add status and password reset token to users

Revision ID: 6492b6f85341
Revises: 7ee4d5b00de0
Create Date: 2025-05-25 23:07:11.365746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6492b6f85341'
down_revision: Union[str, None] = '7ee4d5b00de0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column(
        'status', sa.String(), nullable=True))
    op.add_column('users', sa.Column(
        'password_reset_token', sa.String(), nullable=True))
    op.execute("""
        ALTER TABLE users ADD CONSTRAINT check_users_status
        CHECK (status IN ('active', 'inactive'))
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER TABLE users DROP CONSTRAINT check_users_status")
    op.drop_column('users', 'status')
    op.drop_column('users', 'password_reset_token')
