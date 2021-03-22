"""empty message

Revision ID: 080ef868b370
Revises: 6c8dadbecfc0
Create Date: 2019-06-24 15:01:12.393918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '080ef868b370'
down_revision = '6c8dadbecfc0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('industry', sa.Column('name', sa.String(length=50), nullable=False))
    op.create_unique_constraint(None, 'industry', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'industry', type_='unique')
    op.drop_column('industry', 'name')
    # ### end Alembic commands ###