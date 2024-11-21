"""Initial version

Revision ID: 3a86b89facd7
Revises: 
Create Date: 2023-11-19 19:38:40.006902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '3a86b89facd7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('priorities',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('priority_name', sa.String(length=255), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_priorities_priority_name'), 'priorities', ['priority_name'], unique=False)
    op.create_table('roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role_name', sa.String(length=255), nullable=False),
    sa.Column('permissions', sa.JSON(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_role_name'), 'roles', ['role_name'], unique=False)
    op.create_table('statuses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('status_name', sa.String(length=255), nullable=False),
    sa.Column('permissions', sa.JSON(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_statuses_status_name'), 'statuses', ['status_name'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('full_name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.Column('ipaddress', sa.String(), nullable=True),
    sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('registered_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_full_name'), 'users', ['full_name'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('deadline', sa.DateTime(timezone=True), nullable=True),
    sa.Column('priority_id', sa.Integer(), nullable=True),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.Column('creator_id', sa.Integer(), nullable=False),
    sa.Column('assignee_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['assignee_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['priority_id'], ['priorities.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['status_id'], ['statuses.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('tasks')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_full_name'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_statuses_status_name'), table_name='statuses')
    op.drop_table('statuses')
    op.drop_index(op.f('ix_roles_role_name'), table_name='roles')
    op.drop_table('roles')
    op.drop_index(op.f('ix_priorities_priority_name'), table_name='priorities')
    op.drop_table('priorities')