"""add clusters table and failure clustering columns"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0a857e3f8f5b'
down_revision = None   # IMPORTANT: If your previous migration exists, set it here.
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Create clusters table
    op.create_table(
        'clusters',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('representative_message', sa.Text(), nullable=True),
        sa.Column('representative_embedding', sa.Text(), nullable=True),
        sa.Column('member_count', sa.Integer(), nullable=False, server_default="0"),
        sa.Column('cluster_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True, server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True)
    )

    # 2. Add cluster_id + embedding columns to failures table
    op.add_column('failures', sa.Column('cluster_id', sa.Integer(), nullable=True))
    op.add_column('failures', sa.Column('embedding', sa.Text(), nullable=True))

    # 3. Add index on cluster_id
    op.create_index('ix_failures_cluster_id', 'failures', ['cluster_id'])

    # 4. Add foreign key constraint
    op.create_foreign_key(
        'fk_failures_cluster_id',
        'failures', 'clusters',
        ['cluster_id'], ['id'],
        ondelete='SET NULL'
    )


def downgrade() -> None:
    # Reverse order during downgrade
    op.drop_constraint('fk_failures_cluster_id', 'failures', type_='foreignkey')
    op.drop_index('ix_failures_cluster_id', table_name='failures')

    op.drop_column('failures', 'embedding')
    op.drop_column('failures', 'cluster_id')

    op.drop_table('clusters')
