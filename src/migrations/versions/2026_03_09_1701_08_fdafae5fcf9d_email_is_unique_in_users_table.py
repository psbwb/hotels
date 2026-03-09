"""email is unique in users table

Revision ID: fdafae5fcf9d
Revises: 93424c66041e
Create Date: 2026-03-09 17:01:08.111332

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "fdafae5fcf9d"
down_revision: Union[str, Sequence[str], None] = "93424c66041e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
