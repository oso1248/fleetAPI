"""_functions_00001

Revision ID: 57da7e51d73f
Revises:
Create Date: 2022-12-08 18:45:28.429463

"""
from alembic import op
import sqlalchemy as sa

from sqlalchemy.orm import sessionmaker
from api.config import settings
Session = sessionmaker()

# revision identifiers, used by Alembic.
revision = '57da7e51d73f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    # session.execute("SET TIMEZONE = 'America/Denver'")
    session.execute("""
        CREATE OR REPLACE FUNCTION update_timestamp() RETURNS TRIGGER
        LANGUAGE plpgsql
        AS
        $$
        BEGIN
            NEW.time_updated = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$;
    """)


def downgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute("DROP FUNCTION update_timestamp();")
