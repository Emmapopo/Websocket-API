from sqlalchemy import *
from model.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql
import datetime

from user_model import User
from .course_model import Course
from model.lecturer_model import Lecturer

# A course to define the sending of course messages.


class CourseMessageSend(Base):
    __tablename__ = 'course_message_send'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    sender_id = Column('sender_id', Integer, ForeignKey('lecturer.id'))
    course_id = Column('course_id', Integer, ForeignKey('course.id'))
    title = Column('title', String(500), nullable=False)
    content = Column('content', String(5000), nullable=False)
    timestamp = Column(mysql.DATETIME(fsp=6), default=datetime.datetime.utcnow)


    def __init__(self, sender_id=None, course_id=None, title=None, content=None, timestamp=None):
        self.sender_id = sender_id
        self.course_id = course_id
        self.title = title
        self.content = content
        self.timestamp = timestamp
        # self.message_status = message_status


class CourseMessageSendAttach(Base):
    __tablename__ = 'course_message_send_attach'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    message_id = Column('message_id', Integer, ForeignKey('course_message_send.id'))
    file_link = Column('file_link', String(500),  nullable=False)

    def __init__(self, message_id=None, file_link=None):
        self.message_id = message_id
        self.file_link = file_link


# A course to define the reply of course messages.
class CourseMessageReply(Base):
    __tablename__ = 'course_message_reply'
    id = Column('id', Integer, primary_key=True)
    original_message_id = Column('original_message_id', Integer, ForeignKey('course_message_send.id'))
    sender_id = Column('sender_id', Integer, ForeignKey('user.id'))
    content = Column('content', String(5000), nullable=False)
    timestamp = Column(mysql.DATETIME(fsp=6), default=datetime.datetime.utcnow)
    # message_type = Column('message_type', Enum(MessageType))

    def __init__(self, original_message_id=None, sender_id=None, content=None, timestamp=None):
        self.original_message_id = original_message_id
        self.sender_id = sender_id
        self.content = content
        self.timestamp = timestamp


class CourseMessageReplyAttach(Base):
    __tablename__ = 'course_message_reply_attach'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    message_id = Column('message_id', Integer, ForeignKey('course_message_reply.id'))
    file_link = Column('file_link', String(500), nullable=False)

    def __init__(self, message_id=None, file_link=None):
        self.message_id = message_id
        self.file_link = file_link
