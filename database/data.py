from .core import Base

from sqlalchemy import Boolean, Column, Integer, Text


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    done = Column(Boolean)
    description = Column(Text)
