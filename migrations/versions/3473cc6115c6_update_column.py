"""update column

Revision ID: 3473cc6115c6
Revises: 080ef868b370
Create Date: 2019-06-28 15:48:29.293714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3473cc6115c6'
down_revision = '080ef868b370'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('website_news',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('url', sa.String(length=254), nullable=False),
    sa.Column('domain', sa.String(length=100), nullable=False),
    sa.Column('domain_id', sa.BigInteger(), nullable=False),
    sa.Column('city_code', sa.String(length=10), nullable=True),
    sa.Column('region_code', sa.String(length=10), nullable=True),
    sa.Column('ip', sa.String(length=50), nullable=False),
    sa.Column('ip_area', sa.String(length=254), server_default='', nullable=True),
    sa.Column('title', sa.String(length=254), server_default='', nullable=True),
    sa.Column('web_type', sa.String(length=30), server_default='', nullable=False),
    sa.Column('host_dept', sa.String(length=254), server_default='', nullable=True),
    sa.Column('host_type', sa.String(length=50), server_default='', nullable=True),
    sa.Column('industries', sa.ARRAY(sa.String()), server_default='{}', nullable=True),
    sa.Column('ai_industries', sa.ARRAY(sa.String()), server_default='{}', nullable=True),
    sa.Column('tags', sa.ARRAY(sa.String()), server_default='{}', nullable=True),
    sa.Column('code_language', sa.String(length=50), server_default='', nullable=True),
    sa.Column('http_status', sa.Integer(), server_default='-1', nullable=True),
    sa.Column('http_status_list', sa.String(length=254), server_default='', nullable=True),
    sa.Column('category', sa.String(length=50), server_default='', nullable=True),
    sa.Column('title_updated', sa.TIMESTAMP(), nullable=True),
    sa.Column('status_updated', sa.TIMESTAMP(), nullable=True),
    sa.Column('source', sa.ARRAY(sa.String()), server_default='{}', nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_website_news_ai_industries'), 'website_news', ['ai_industries'], unique=False)
    op.create_index(op.f('ix_website_news_category'), 'website_news', ['category'], unique=False)
    op.create_index(op.f('ix_website_news_create_time'), 'website_news', ['create_time'], unique=False)
    op.create_index(op.f('ix_website_news_domain'), 'website_news', ['domain'], unique=False)
    op.create_index(op.f('ix_website_news_http_status'), 'website_news', ['http_status'], unique=False)
    op.create_index(op.f('ix_website_news_industries'), 'website_news', ['industries'], unique=False)
    op.create_index(op.f('ix_website_news_ip'), 'website_news', ['ip'], unique=False)
    op.create_index(op.f('ix_website_news_source'), 'website_news', ['source'], unique=False)
    op.create_index(op.f('ix_website_news_update_time'), 'website_news', ['update_time'], unique=False)
    op.create_index(op.f('ix_website_news_url'), 'website_news', ['url'], unique=True)
    op.create_index(op.f('ix_website_news_web_type'), 'website_news', ['web_type'], unique=False)
    op.drop_index('ix_domain_archived_tags', table_name='domain_archived')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_domain_archived_tags', 'domain_archived', ['tags'], unique=False)
    op.drop_index(op.f('ix_website_news_web_type'), table_name='website_news')
    op.drop_index(op.f('ix_website_news_url'), table_name='website_news')
    op.drop_index(op.f('ix_website_news_update_time'), table_name='website_news')
    op.drop_index(op.f('ix_website_news_source'), table_name='website_news')
    op.drop_index(op.f('ix_website_news_ip'), table_name='website_news')
    op.drop_index(op.f('ix_website_news_industries'), table_name='website_news')
    op.drop_index(op.f('ix_website_news_http_status'), table_name='website_news')
    op.drop_index(op.f('ix_website_news_domain'), table_name='website_news')
    op.drop_index(op.f('ix_website_news_create_time'), table_name='website_news')
    op.drop_index(op.f('ix_website_news_category'), table_name='website_news')
    op.drop_index(op.f('ix_website_news_ai_industries'), table_name='website_news')
    op.drop_table('website_news')
    # ### end Alembic commands ###
