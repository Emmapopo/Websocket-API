import enum

# A class to define the enums of the message status. 
class MessageStatus(enum.Enum):
    sent = 0
    delivered = 1
    seen = 2
