from sqlalchemy import *
from model.base import Base
from sqlalchemy.orm import relationship

from .course_model import Course
from model.lecturer_model import Lecturer


class CourseLecturer(Base):
    __tablename__ = 'course_lecturer'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    course_id = Column('course_id', Integer, ForeignKey('course.id'))
    lecturer_id = Column('lecturer_id', Integer, ForeignKey('lecturer.id'))

    __table_args__ = (UniqueConstraint('course_id', 'lecturer_id',),
                      )

    def __init__(self, course_id=None, lecturer_id=None):
        self.course_id = course_id
        self.lecturer_id = lecturer_id
