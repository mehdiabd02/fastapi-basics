"""create new table

Revision ID: ee774c272d4e
Revises: f8deaa028bf7
Create Date: 2026-05-08 16:00:21.227465

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee774c272d4e'
down_revision: Union[str, Sequence[str], None] = 'f8deaa028bf7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('new_column', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('posts', 'new_column')
