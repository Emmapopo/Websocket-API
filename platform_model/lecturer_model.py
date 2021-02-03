
from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from user_model import User
from .school_model import School, Faculty, Department
import enum
from user_type import UserType


class LecturerTitle(enum.Enum):
    mr = 'Mr'
    mrs = 'Mrs'
    miss = 'Miss'
    dr = 'Dr'
    prof = 'Prof'


class LecturerPosition(enum.Enum):
    juniorlecturer = 'Junior Lecturer'
    lecturerI = 'Leturer I'
    lecturerII = 'Lecturer II'
    seniorlecturer = 'Senior Lecturer'
    associateprof = 'Associate Prof'
    prof = 'Prof'

# A Lecturer Class to model the lecturers details

class Lecturer(User, Base, SerializerMixin):
    __tablename__ = 'lecturer'
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    department_id = Column('department_id', Integer, ForeignKey('department.id'))
    title = Column(Enum(LecturerTitle))
    position = Column(Enum(LecturerPosition))

    serialize_only = ('id', 'user_name', 'surname', 'first_name',
                      'email', 'user_type', 'department_id', 'title', 'position')

    __mapper_args__ = {
        'polymorphic_identity': UserType.Lecturer # Maps to Lecturer UserType
    }

    def __init__(self, user_name=None, surname=None, first_name=None, email=None, password=None, user_type=None, department_id=None, title=None, position=None):

        super(Lecturer, self).__init__(user_name, surname,
                                       first_name, email, password, user_type)

        self.department_id = department_id
        self.title = title
        self.position = position
