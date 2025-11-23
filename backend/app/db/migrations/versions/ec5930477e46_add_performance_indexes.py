from alembic import op
import sqlalchemy as sa

revision = 'ec5930477e46'
down_revision = 'd6b286db3449'
branch_labels = None
depends_on = None


def upgrade():

    # Runs table indexes
    op.create_index('ix_runs_finished_at', 'runs', ['finished_at'])
    op.create_index('ix_runs_started_at', 'runs', ['started_at'])

    # Trends table index
    op.create_index('ix_cluster_trends_cluster_date', 'cluster_trends', ['cluster_id', 'date'])


def downgrade():
    op.drop_index('ix_runs_finished_at', table_name='runs')
    op.drop_index('ix_runs_started_at', table_name='runs')
    op.drop_index('ix_cluster_trends_cluster_date', table_name='cluster_trends')
