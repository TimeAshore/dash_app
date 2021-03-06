"""empty message

Revision ID: bd90d555f529
Revises: 41aac9c03645
Create Date: 2019-06-28 15:52:04.321888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd90d555f529'
down_revision = '41aac9c03645'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('domain_archived', sa.Column('industries', sa.ARRAY(sa.String()), server_default='{}', nullable=True))
    op.add_column('domain_archived', sa.Column('tags', sa.ARRAY(sa.String()), server_default='{}', nullable=True))
    op.create_index(op.f('ix_domain_archived_industries'), 'domain_archived', ['industries'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_domain_archived_industries'), table_name='domain_archived')
    op.drop_column('domain_archived', 'tags')
    op.drop_column('domain_archived', 'industries')
    # ### end Alembic commands ###
