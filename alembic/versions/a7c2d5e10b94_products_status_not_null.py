"""products.status not null

Revision ID: a7c2d5e10b94
Revises: e1f4c07a9b53
Create Date: 2026-09-03 01:20:00.000000

The column was nullable while ProductModel declares status as a required
ProductStatus, so a NULL row read back raised a ValidationError (500) instead
of being rejected on write.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7c2d5e10b94'
down_revision: Union[str, Sequence[str], None] = 'e1f4c07a9b53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("UPDATE products SET status = 'ACTIVE' WHERE status IS NULL")
    op.alter_column('products', 'status', existing_type=sa.String(), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('products', 'status', existing_type=sa.String(), nullable=True)
