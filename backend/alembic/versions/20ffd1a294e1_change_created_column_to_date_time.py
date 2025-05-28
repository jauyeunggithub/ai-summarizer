"""change created column to date time

Revision ID: 20ffd1a294e1
Revises: 11d999cfaf47
Create Date: 2025-05-28 01:02:27.942420

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20ffd1a294e1'
down_revision: Union[str, None] = '11d999cfaf47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('summaries', sa.Column(
        'created_tmp', sa.DateTime(), nullable=True))
    op.execute(
        """
            UPDATE summaries SET created_tmp = created
        """
    )

    op.drop_column('summaries', 'created')
    op.alter_column(
        'summaries',
        'created_tmp',
        new_column_name='created'
    )

    op.add_column('users', sa.Column(
        'created_tmp', sa.DateTime(), nullable=True))
    op.execute(
        """
            UPDATE users SET created_tmp = created
        """
    )

    op.drop_column('users', 'created')
    op.alter_column(
        'users',
        'created_tmp',
        new_column_name='created'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('summaries', sa.Column(
        'created_tmp', sa.Date(), nullable=True))
    op.execute(
        """
            UPDATE summaries SET created_tmp = DATE(created)
        """
    )
    op.drop_column('summaries', 'created')
    op.alter_column(
        'summaries',
        'created',
        new_column_name='created'
    )

    op.add_column('users', sa.Column(
        'created_tmp', sa.Date(), nullable=True))
    op.execute(
        """
            UPDATE users SET created_tmp = DATE(created)
        """
    )
    op.drop_column('users', 'created')
    op.alter_column(
        'users',
        'created',
        new_column_name='created'
    )
