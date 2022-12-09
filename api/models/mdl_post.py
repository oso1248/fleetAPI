from sqlalchemy import Column, Integer, text, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from ..database.database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    uuid = Column(UUID(as_uuid=True), nullable=False, server_default=text('gen_random_uuid()'))
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    is_published = Column(Boolean, nullable=False, server_default=text('True'))
    created_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    creator = relationship("Users")


class Votes(Base):
    __tablename__ = "votes"

    id_user = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    id_post = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    time_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
