from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql
import datetime
from user_model import User
from .class_model import Class

# A class to define the sending of class messages.
class ClassMessageSend(Base):
    __tablename__ = 'class_message_send'
    id = Column('id', Integer, primary_key=True)
    sender_id = Column('sender_id', Integer, ForeignKey('user.id'))
    class_id = Column('class_id', Integer, ForeignKey('class.id'))
    title = Column ('title', String(500), nullable=False)
    content = Column('content', String(5000), nullable=False)
    timestamp = Column(mysql.DATETIME(fsp=6), default=datetime.datetime.utcnow)
    # message_type = Column('message_type', Enum(MessageType))

    def __init__(self, sender_id=None, class_id = None, title=None, content=None, timestamp=None):
        self.sender_id = sender_id
        self.class_id = class_id
        self.title = title
        self.content = content
        self.timestamp = timestamp
        # self.message_status = message_status

class ClassMessageSendAttach(Base):
    __tablename__ = 'class_message_send_attach'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    message_id = Column('message_id', Integer, ForeignKey('class_message_send.id'))
    file_link = Column('file_link', String(500), nullable=False)

    def __init__ (self, message_id = None, file_link = None):
        self.message_id = message_id
        self.file_link = file_link


# A class to define the reply of class messages.
class ClassMessageReply(Base):
    __tablename__ = 'class_message_reply'
    id = Column('id', Integer, primary_key=True)
    original_message_id = Column('original_message_id', Integer, ForeignKey('class_message_send.id'))
    sender_id = Column('sender_id', Integer, ForeignKey('user.id'))
    content = Column('content', String(5000), nullable=False)
    timestamp = Column(mysql.DATETIME(fsp=6), default=datetime.datetime.utcnow)
    # message_type = Column('message_type', Enum(MessageType))

    def __init__(self, original_message_id = None, sender_id=None, content=None, timestamp=None):
        self.original_message_id = original_message_id
        self.sender_id = sender_id
        self.content = content
        self.timestamp = timestamp
    


class ClassMessageReplyAttach(Base):
    __tablename__ = 'class_message_reply_attach'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    message_id = Column('message_id', Integer, ForeignKey('class_message_reply.id'))
    file_link = Column('file_link', String(500), nullable=False)

    def __init__(self, message_id=None, file_link=None):
        self.message_id = message_id
        self.file_link = file_link