"""initial schema

Revision ID: 20260126_01
Revises: 
Create Date: 2026-01-26
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20260126_01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'policies',
        sa.Column('policy_id', sa.String(), primary_key=True),
        sa.Column('institution_id', sa.String(), nullable=False),
        sa.Column('course_id', sa.String(), nullable=False),
        sa.Column('content', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('version', sa.String(), nullable=False),
        sa.Column('previous_version_id', sa.String(), sa.ForeignKey('policies.policy_id'), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('effective_from', sa.DateTime(), nullable=False),
        sa.Column('deprecated_at', sa.DateTime(), nullable=True),
    )
    op.create_index('idx_course_active', 'policies', ['course_id', 'deprecated_at'])

    op.create_table(
        'ai_use_logs',
        sa.Column('log_id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('course_id', sa.String(), nullable=False),
        sa.Column('actor_id_pseudonym', sa.String(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('assessment_type', sa.String(), nullable=False),
        sa.Column('policy_id', sa.String(), sa.ForeignKey('policies.policy_id'), nullable=False),
        sa.Column('decision', sa.String(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('retention_until', sa.DateTime(), nullable=True),
    )
    op.create_index('idx_student_time', 'ai_use_logs', ['actor_id_pseudonym', 'timestamp'])


def downgrade():
    op.drop_index('idx_student_time', table_name='ai_use_logs')
    op.drop_table('ai_use_logs')
    op.drop_index('idx_course_active', table_name='policies')
    op.drop_table('policies')
