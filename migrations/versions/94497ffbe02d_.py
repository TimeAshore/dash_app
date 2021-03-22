"""empty message

Revision ID: 94497ffbe02d
Revises: 30f79e7bdb6b
Create Date: 2019-07-25 10:32:22.634566

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94497ffbe02d'
down_revision = '30f79e7bdb6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('website_news', sa.Column('content', sa.TEXT(), server_default='', nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('website_news', 'content')
    # ### end Alembic commands ###
