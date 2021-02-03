from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship
from .user_model import User
from platform_model.class_model import Class

# A class to define the members of a class.

class ClassMem(Base):
    __tablename__ = 'class_mem'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    class_id = Column('class_id', Integer, ForeignKey('class.id'))
    member_id = Column('member_id', Integer, ForeignKey('user.id'))

    __table_args__ = (UniqueConstraint('class_id', 'member_id'),
                      )

    def __init__(self, class_id=None, member_id=None):
        self.class_id = class_id
        self.member_id = member_id
