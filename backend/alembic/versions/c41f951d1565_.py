"""empty message

Revision ID: c41f951d1565
Revises:
Create Date: 2025-05-18 00:13:35.166172

"""
from typing import Sequence, Union
import uuid
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c41f951d1565'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), nullable=False, default=uuid.uuid4),
        sa.Column('first_name', sa.String(length=300), nullable=False),
        sa.Column('last_name', sa.String(length=300), nullable=False),
        sa.Column('email', sa.String(length=300), nullable=False),
        sa.Column('subscription_id', sa.String(length=300), nullable=True),
        sa.Column('created', sa.Date(), nullable=False,
                  default=sa.func.current_date()),
        sa.Column('hashed_password', sa.String(length=500), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
