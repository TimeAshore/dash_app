"""empty message

Revision ID: 6dd556890b09
Revises: 2aa818269200
Create Date: 2019-07-29 17:59:31.669098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6dd556890b09'
down_revision = '2aa818269200'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'ban_group', ['id'])
    op.create_unique_constraint(None, 'ban_keyword', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ban_keyword', type_='unique')
    op.drop_constraint(None, 'ban_group', type_='unique')
    # ### end Alembic commands ###
