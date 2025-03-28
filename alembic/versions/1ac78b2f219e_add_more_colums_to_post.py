"""add more colums to post

Revision ID: 1ac78b2f219e
Revises: 98388e5c40c6
Create Date: 2025-03-25 09:48:42.348615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ac78b2f219e'
down_revision: Union[str, None] = '98388e5c40c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False ,server_default='True'))
    op.add_column("posts", sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
