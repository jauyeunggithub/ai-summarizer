"""empty message

Revision ID: 85b9d4b11140
Revises: c41f951d1565
Create Date: 2025-05-18 15:28:20.391079

"""
from typing import Sequence, Union
import uuid
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85b9d4b11140'
down_revision: Union[str, None] = 'c41f951d1565'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'summaries',
        sa.Column('id', sa.UUID(), nullable=False, default=uuid.uuid4),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('file_path', sa.String(), nullable=True),
        sa.Column('text_to_summarize', sa.String(), nullable=True),
        sa.Column('created', sa.Date(), nullable=False,
                  default=sa.func.current_date()),
        sa.Column('summary_result', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_foreign_key(
        constraint_name='fk_summaries_user_id',
        source_table='summaries',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        constraint_name='fk_summaries_user_id',
        table_name='summaries',
        type_='foreignkey'
    )
    op.drop_table('summaries')
