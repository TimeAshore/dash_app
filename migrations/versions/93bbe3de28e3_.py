"""empty message

Revision ID: 93bbe3de28e3
Revises: bd90d555f529
Create Date: 2019-07-03 16:24:52.303506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93bbe3de28e3'
down_revision = 'bd90d555f529'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('website_news', 'domain',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.alter_column('website_news', 'domain_id',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('website_news', 'ip',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('website_news', 'web_type',
               existing_type=sa.VARCHAR(length=30),
               nullable=True,
               existing_server_default=sa.text("''::character varying"))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('website_news', 'web_type',
               existing_type=sa.VARCHAR(length=30),
               nullable=False,
               existing_server_default=sa.text("''::character varying"))
    op.alter_column('website_news', 'ip',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('website_news', 'domain_id',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('website_news', 'domain',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###
