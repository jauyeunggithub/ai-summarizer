"""empty message

Revision ID: 55365c358b4b
Revises: 85b9d4b11140
Create Date: 2025-05-18 15:35:40.608676

"""
from typing import Sequence, Union
import uuid
import datetime
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash


# revision identifiers, used by Alembic.
revision: str = '55365c358b4b'
down_revision: Union[str, None] = '85b9d4b11140'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    connection = op.get_bind()
    password = "f8@p9j0U"
    hashed_password = generate_password_hash(password)
    user_id = uuid.uuid4()
    file_path = 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf'
    summary_result = 'The quick fox jumps over the lazy dog near the bright yellow flower.'

    insert_user_sql = '''
        INSERT INTO users (
            id,
            first_name,
            last_name,
            email,
            hashed_password,
            created
        ) VALUES (
            :id,
            :first_name,
            :last_name,
            :email,
            :hashed_password,
            :created
        )
    '''
    connection.execute(
        sa.text(insert_user_sql)
        .bindparams(
            id=user_id,
            first_name="John",
            last_name="Au-Yeung",
            email="mayeung@telus.net",
            hashed_password=hashed_password,
            created=datetime.datetime.now()
        )
    )

    insert_summaries_sql = '''
        INSERT INTO summaries (
            id,
            user_id,
            file_path,
            summary_result,
            created
        ) VALUES (
            :id,
            :user_id,
            :file_path,
            :summary_result,
            :created
        )
    '''
    for i in range(100):
        connection.execute(
            sa.text(insert_summaries_sql)
            .bindparams(
                id=uuid.uuid4(),
                user_id=user_id,
                file_path=file_path,
                summary_result=summary_result,
                created=datetime.datetime.now()
            )
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM summaries")
    op.execute("DELETE FROM users")
