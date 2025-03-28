"""create foreign key 

Revision ID: 98388e5c40c6
Revises: bd750c47ccb1
Create Date: 2025-03-25 09:33:00.821347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98388e5c40c6'
down_revision: Union[str, None] = 'bd750c47ccb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("owner_id",sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fkey", source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("posts_users_fkey", "posts")
    pass
