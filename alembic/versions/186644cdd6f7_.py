"""empty message

Revision ID: 186644cdd6f7
Revises: 
Create Date: 2024-06-28 10:06:07.097698

"""
from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy  # Add this import



# revision identifiers, used by Alembic.
revision = '186644cdd6f7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('access_policy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('daily_api_calls', sa.Integer(), server_default='1000', nullable=False),
    sa.Column('monthly_api_calls', sa.Integer(), server_default='30000', nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_access_policy_id'), 'access_policy', ['id'], unique=False)
    op.create_table('user',
    sa.Column('date_created', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('date_deleted', sa.DateTime(timezone=True), nullable=True),
    sa.Column('id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('inference_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('problem', sa.String(), nullable=False),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('version', sa.String(), nullable=True),
    sa.Column('first_deployed', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('last_updated', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('deployment_status', sa.String(), server_default='Pending', nullable=False),
    sa.Column('in_production', sa.Boolean(), server_default='False', nullable=False),
    sa.Column('mlflow_id', sa.String(), nullable=True),
    sa.Column('source_url', sa.String(), nullable=True),
    sa.Column('access_policy_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['access_policy_id'], ['access_policy.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inference_model_id'), 'inference_model', ['id'], unique=False)
    op.create_table('service_call',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('time_requested', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('time_completed', sa.DateTime(timezone=True), nullable=True),
    sa.Column('celery_task_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['model_id'], ['inference_model.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_service_call_id'), 'service_call', ['id'], unique=False)
    op.create_table('user_access',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('model_id', sa.Integer(), nullable=False),
    sa.Column('access_policy_id', sa.Integer(), nullable=False),
    sa.Column('api_calls', sa.Integer(), nullable=False),
    sa.Column('access_granted', sa.Boolean(), nullable=False),
    sa.Column('last_accessed', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['access_policy_id'], ['access_policy.id'], ),
    sa.ForeignKeyConstraint(['model_id'], ['inference_model.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'model_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_access')
    op.drop_index(op.f('ix_service_call_id'), table_name='service_call')
    op.drop_table('service_call')
    op.drop_index(op.f('ix_inference_model_id'), table_name='inference_model')
    op.drop_table('inference_model')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_access_policy_id'), table_name='access_policy')
    op.drop_table('access_policy')
    # ### end Alembic commands ###