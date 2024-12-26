"""first migrations

Revision ID: 5f092261e000
Revises: 773254f076c4
Create Date: 2024-12-26 03:24:10.816624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f092261e000'
down_revision: Union[str, None] = '773254f076c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
