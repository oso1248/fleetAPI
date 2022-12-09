"""_users)00002

Revision ID: d6931db81268
Revises: 57da7e51d73f
Create Date: 2022-12-08 18:46:09.137791

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker
from api.config import settings
Session = sessionmaker()

# revision identifiers, used by Alembic.
revision = 'd6931db81268'
down_revision = '57da7e51d73f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('eid', sa.String(), nullable=False, unique=True),
        sa.Column('name_first', sa.String(), nullable=False),
        sa.Column('name_last', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('permissions', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='True', nullable=False),
        sa.Column('time_created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('time_updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(settings.USER_INSERT)
    session.execute("""
        CREATE TRIGGER update_timestamp
        BEFORE UPDATE
        ON users
        FOR EACH ROW
        EXECUTE PROCEDURE update_timestamp();
    """)


def downgrade():
    op.drop_table('users')
