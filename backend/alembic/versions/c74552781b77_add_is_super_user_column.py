"""add is super user column

Revision ID: c74552781b77
Revises: 20ffd1a294e1
Create Date: 2025-05-29 00:17:35.041238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c74552781b77'
down_revision: Union[str, None] = '20ffd1a294e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'users',
        sa.Column(
            'is_super_user', sa.Boolean(), nullable=True
        )
    )
    op.execute(
        """
            UPDATE users
            SET is_super_user = true
            WHERE email = 'mayeung@telus.net'
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'is_super_user')
