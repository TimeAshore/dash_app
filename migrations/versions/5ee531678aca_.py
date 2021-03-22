"""empty message

Revision ID: 5ee531678aca
Revises: 182797b73033
Create Date: 2019-06-24 14:52:42.482574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ee531678aca'
down_revision = '182797b73033'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('industry',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('spell', sa.String(length=30), server_default='', nullable=True),
    sa.Column('website_count', sa.Integer(), server_default='0', nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_industry_create_time'), 'industry', ['create_time'], unique=False)
    op.create_index(op.f('ix_industry_update_time'), 'industry', ['update_time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_industry_update_time'), table_name='industry')
    op.drop_index(op.f('ix_industry_create_time'), table_name='industry')
    op.drop_table('industry')
    # ### end Alembic commands ###