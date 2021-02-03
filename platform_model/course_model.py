from sqlalchemy import *
from model.base import Base
from sqlalchemy.orm import relationship


class Course(Base):
    __tablename__ = 'course'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    code = Column('code', String(50), nullable=False, unique=True)
    title = Column('title', String(500), nullable=False)
    unit = Column('unit', Integer, nullable=False)

    def __init__(self, code=None, title=None, unit=None):
        self.code = code
        self.title = title
        self.unit = unit
