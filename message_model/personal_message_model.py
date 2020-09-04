from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql
import datetime
from .status import MessageStatus
from user_model import User
from .personal_conv_init import PersonalConvInit

# A class to define the personal message table.
class PersonalMessage(Base):
    __tablename__ = 'personal_message'
    id = Column('id', Integer, primary_key=True)
    sender_id = Column('sender_id', Integer, ForeignKey('user.id'))
    conv_id = Column('conv_id', Integer, ForeignKey('personal_conv_init.conv_id'))
    message = Column('message', String(2000), nullable=False)
    timestamp = Column(mysql.DATETIME(fsp=6), default=datetime.datetime.utcnow)
    message_status = Column('message_status', Enum(MessageStatus))


    def __init__(self, sender_id=None, conv_id=None, message=None, timestamp=None, message_status=None):
        self.sender_id = sender_id
        self.conv_id = conv_id
        self.message = message
        self.timestamp = timestamp
        self.message_status = message_status

