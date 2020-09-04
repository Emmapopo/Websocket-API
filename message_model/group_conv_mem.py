from sqlalchemy import *
from .base import Base
from sqlalchemy.orm import relationship
from user_model import User
from .group_conv_init import GroupConvInit

# A class to define the group conversation member table.

class GroupConvMem(Base):
    __tablename__ = 'group_conv_mem'
    id = Column('id', Integer, primary_key=True)
    conv_id = Column('conv_id', Integer, ForeignKey('group_conv_init.conv_id'))
    member_id = Column('member_id', Integer, ForeignKey('user.id'))

    def __init__(self, conv_id=None, member_id=None):
        self.conv_id = conv_id
        self.member_id = member_id
