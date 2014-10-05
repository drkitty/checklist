from .core import Base

from sqlalchemy import Boolean, Column, String, Text


class Item(Base):
    __tablename__ = 'item'

    id = Column(String(32), primary_key=True)
    done = Column(Boolean)
    description = Column(Text)
