from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from .user_model import User
from .user_type import UserType


# A mentor class to model mentor details
class Mentor(User, Base, SerializerMixin):
    __tablename__ = 'mentor'
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    profession = Column('profession', String(50), nullable=True)
    company = Column('company', String(50), nullable=True)
    title = Column('title', String(50), nullable=True)

    serialize_only = ('id', 'user_name', 'surname', 'first_name',
                      'email', 'user_type', 'profession', 'company', 'title')

    __mapper_args__ = {
        'polymorphic_identity': UserType.Mentor # Maps to Mentor User Type
    }

    def __init__(self, user_name=None, surname=None, first_name=None, email=None, password=None, user_type=None, profession=None, company=None, title=None):
        super(Mentor, self).__init__(user_name, surname,
                                     first_name, email, password, user_type)

        self.profession = profession
        self.company = company
        self.title = title
