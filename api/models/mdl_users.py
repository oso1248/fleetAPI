from sqlalchemy import Column, Integer, text, String, Boolean
from ..database.database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    eid = Column(String, nullable=False, unique=True)
    name_first = Column(String, nullable=False)
    name_last = Column(String, nullable=False)
    password = Column(String, nullable=False)
    permissions = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default=text('True'))
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
