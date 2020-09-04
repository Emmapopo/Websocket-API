from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql
from user_model import User
import datetime

# A class to define the group conversation initialization table. 
class GroupConvInit(Base):
    __tablename__ = 'group_conv_init'
    conv_id = Column('conv_id', Integer, primary_key=True)
    creator_id = Column('creator_id', Integer, ForeignKey(User.id))
    group_name = Column('group_name', String(200), nullable=False)
    description = Column('description', String(2000), nullable=False)
    timestamp = Column(mysql.DATETIME(fsp=6), default=datetime.datetime.utcnow)

    def __init__(self, creator_id=None, group_name=None, description=None, timestamp=None):
        self.creator_id = creator_id
        self.group_name = group_name
        self.description = description
        self.timestamp = timestamp
