from sqlalchemy import *
from model.base import Base
from sqlalchemy.orm import relationship

from user_model import User
from .course_model import Course

# A class to define the members of a class.


class CourseMem(Base):
    __tablename__ = 'course_mem'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    course_id = Column('course_id', Integer, ForeignKey('course.id'))
    member_id = Column('member_id', Integer, ForeignKey('user.id'))

    __table_args__ = (UniqueConstraint('course_id', 'member_id'),
                      )

    def __init__(self, course_id=None, member_id=None):
        self.course_id = course_id
        self.member_id = member_id
