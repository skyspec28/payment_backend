"""create content

Revision ID: a923064f7360
Revises: 2f712c69990a
Create Date: 2025-03-25 09:10:59.395113

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a923064f7360'
down_revision: Union[str, None] = '2f712c69990a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
