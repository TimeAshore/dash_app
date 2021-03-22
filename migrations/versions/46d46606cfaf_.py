"""empty message

Revision ID: 46d46606cfaf
Revises: 
Create Date: 2019-06-12 17:52:09.996796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46d46606cfaf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('city',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('spell', sa.String(length=100), server_default='', nullable=True),
    sa.Column('spell_short', sa.String(length=20), server_default='', nullable=True),
    sa.Column('keywords', sa.ARRAY(sa.String()), server_default='{}', nullable=True),
    sa.Column('priority', sa.Integer(), server_default='1', nullable=True),
    sa.Column('code', sa.String(length=10), nullable=True),
    sa.Column('province_name', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_city_create_time'), 'city', ['create_time'], unique=False)
    op.create_index(op.f('ix_city_update_time'), 'city', ['update_time'], unique=False)
    op.create_table('domain_archived',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('city_code', sa.String(length=50), nullable=True),
    sa.Column('region_code', sa.String(length=100), nullable=True),
    sa.Column('icp_number', sa.String(length=50), server_default='', nullable=True),
    sa.Column('icp_updated', sa.TIMESTAMP(), nullable=True),
    sa.Column('icp_source', sa.String(length=30), server_default='', nullable=True),
    sa.Column('sponsor', sa.String(length=254), server_default='', nullable=True),
    sa.Column('sponsor_type', sa.String(length=50), server_default='', nullable=True),
    sa.Column('invalid_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('industries', sa.String(length=50), server_default='', nullable=True),
    sa.Column('national_level', sa.Boolean(), server_default='0', nullable=True),
    sa.Column('tags', sa.String(length=50), server_default='', nullable=True),
    sa.Column('subdomain_count', sa.Integer(), server_default='0', nullable=True),
    sa.Column('website_count', sa.Integer(), server_default='0', nullable=True),
    sa.Column('website_count_updated', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_domain_archived_create_time'), 'domain_archived', ['create_time'], unique=False)
    op.create_index(op.f('ix_domain_archived_industries'), 'domain_archived', ['industries'], unique=False)
    op.create_index(op.f('ix_domain_archived_sponsor'), 'domain_archived', ['sponsor'], unique=False)
    op.create_index(op.f('ix_domain_archived_sponsor_type'), 'domain_archived', ['sponsor_type'], unique=False)
    op.create_index(op.f('ix_domain_archived_tags'), 'domain_archived', ['tags'], unique=False)
    op.create_index(op.f('ix_domain_archived_update_time'), 'domain_archived', ['update_time'], unique=False)
    op.create_table('domain_recycler',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('city_code', sa.String(length=10), nullable=True),
    sa.Column('region_code', sa.String(length=10), nullable=True),
    sa.Column('icp_number', sa.String(length=50), server_default='', nullable=True),
    sa.Column('icp_updated', sa.DateTime(), nullable=True),
    sa.Column('icp_source', sa.String(length=30), server_default='', nullable=True),
    sa.Column('industries', sa.String(length=50), server_default='', nullable=True),
    sa.Column('national_level', sa.Boolean(), server_default='0', nullable=True),
    sa.Column('tags', sa.String(length=50), server_default='', nullable=True),
    sa.Column('sponsor', sa.String(length=254), server_default='', nullable=True),
    sa.Column('sponsor_type', sa.String(length=50), server_default='', nullable=True),
    sa.Column('reason', sa.String(length=254), server_default='', nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_domain_recycler_create_time'), 'domain_recycler', ['create_time'], unique=False)
    op.create_index(op.f('ix_domain_recycler_industries'), 'domain_recycler', ['industries'], unique=False)
    op.create_index(op.f('ix_domain_recycler_sponsor'), 'domain_recycler', ['sponsor'], unique=False)
    op.create_index(op.f('ix_domain_recycler_sponsor_type'), 'domain_recycler', ['sponsor_type'], unique=False)
    op.create_index(op.f('ix_domain_recycler_tags'), 'domain_recycler', ['tags'], unique=False)
    op.create_index(op.f('ix_domain_recycler_update_time'), 'domain_recycler', ['update_time'], unique=False)
    op.create_table('province',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('spell', sa.String(length=100), server_default='', nullable=True),
    sa.Column('spell_short', sa.String(length=20), server_default='', nullable=True),
    sa.Column('keywords', sa.ARRAY(sa.String()), server_default='{}', nullable=True),
    sa.Column('priority', sa.Integer(), server_default='1', nullable=True),
    sa.Column('code', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_province_create_time'), 'province', ['create_time'], unique=False)
    op.create_index(op.f('ix_province_update_time'), 'province', ['update_time'], unique=False)
    op.create_table('region',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('spell', sa.String(length=50), nullable=False),
    sa.Column('spell_short', sa.String(length=20), server_default='', nullable=True),
    sa.Column('priority', sa.Integer(), server_default='1', nullable=True),
    sa.Column('keywords', sa.ARRAY(sa.String()), server_default='{}', nullable=True),
    sa.Column('code', sa.String(length=6), nullable=True),
    sa.Column('city_name', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_region_create_time'), 'region', ['create_time'], unique=False)
    op.create_index(op.f('ix_region_update_time'), 'region', ['update_time'], unique=False)
    op.create_table('setting',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('create_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('update_time', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('value', sa.String(length=500), server_default='', nullable=False),
    sa.Column('group', sa.String(length=100), server_default='', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_setting_create_time'), 'setting', ['create_time'], unique=False)
    op.create_index(op.f('ix_setting_name'), 'setting', ['name'], unique=True)
    op.create_index(op.f('ix_setting_update_time'), 'setting', ['update_time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_setting_update_time'), table_name='setting')
    op.drop_index(op.f('ix_setting_name'), table_name='setting')
    op.drop_index(op.f('ix_setting_create_time'), table_name='setting')
    op.drop_table('setting')
    op.drop_index(op.f('ix_region_update_time'), table_name='region')
    op.drop_index(op.f('ix_region_create_time'), table_name='region')
    op.drop_table('region')
    op.drop_index(op.f('ix_province_update_time'), table_name='province')
    op.drop_index(op.f('ix_province_create_time'), table_name='province')
    op.drop_table('province')
    op.drop_index(op.f('ix_domain_recycler_update_time'), table_name='domain_recycler')
    op.drop_index(op.f('ix_domain_recycler_tags'), table_name='domain_recycler')
    op.drop_index(op.f('ix_domain_recycler_sponsor_type'), table_name='domain_recycler')
    op.drop_index(op.f('ix_domain_recycler_sponsor'), table_name='domain_recycler')
    op.drop_index(op.f('ix_domain_recycler_industries'), table_name='domain_recycler')
    op.drop_index(op.f('ix_domain_recycler_create_time'), table_name='domain_recycler')
    op.drop_table('domain_recycler')
    op.drop_index(op.f('ix_domain_archived_update_time'), table_name='domain_archived')
    op.drop_index(op.f('ix_domain_archived_tags'), table_name='domain_archived')
    op.drop_index(op.f('ix_domain_archived_sponsor_type'), table_name='domain_archived')
    op.drop_index(op.f('ix_domain_archived_sponsor'), table_name='domain_archived')
    op.drop_index(op.f('ix_domain_archived_industries'), table_name='domain_archived')
    op.drop_index(op.f('ix_domain_archived_create_time'), table_name='domain_archived')
    op.drop_table('domain_archived')
    op.drop_index(op.f('ix_city_update_time'), table_name='city')
    op.drop_index(op.f('ix_city_create_time'), table_name='city')
    op.drop_table('city')
    # ### end Alembic commands ###