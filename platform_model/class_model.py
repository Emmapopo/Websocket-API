from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship

from .school_model import Program
from .school_model import Level



class Class(Base):
    __tablename__ = 'class'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    program_id = Column('program_id', Integer, ForeignKey('program.id'))
    level_id = Column('level_id', Integer, ForeignKey('level.id'))

    __table_args__ = (UniqueConstraint('program_id', 'level_id',),
                      )

    def __init__(self, program_id=None, level_id=None):
        self.program_id = program_id
        self.level_id = level_id
