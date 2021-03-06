"""empty message

Revision ID: 30f79e7bdb6b
Revises: 75418dbc72c4
Create Date: 2019-07-22 15:25:30.037394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30f79e7bdb6b'
down_revision = '75418dbc72c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('website_banned', sa.Column('url', sa.String(length=254), nullable=False))
    op.create_index(op.f('ix_website_banned_url'), 'website_banned', ['url'], unique=True)
    op.create_unique_constraint(None, 'website_banned', ['id'])
    op.add_column('website_duplicated', sa.Column('url', sa.String(length=254), nullable=False))
    op.create_index(op.f('ix_website_duplicated_url'), 'website_duplicated', ['url'], unique=True)
    op.create_unique_constraint(None, 'website_duplicated', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'website_duplicated', type_='unique')
    op.drop_index(op.f('ix_website_duplicated_url'), table_name='website_duplicated')
    op.drop_column('website_duplicated', 'url')
    op.drop_constraint(None, 'website_banned', type_='unique')
    op.drop_index(op.f('ix_website_banned_url'), table_name='website_banned')
    op.drop_column('website_banned', 'url')
    # ### end Alembic commands ###
