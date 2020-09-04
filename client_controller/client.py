#This is the client class that defines the methods a client can call.
from client_model.client_abstract import ClientAbstract
from user_model import User
from sess import session
from message_model.personal_message_model import PersonalMessage
from message_model.group_message_model import GroupMessage

class Client(ClientAbstract):
    #The client is initialized with his user_id and connection
    def __init__(self, id, conn):
        self.id = id
        self.conn = conn

    # This function hits the database to get the details of the client.
    def populate(self, session):

        # self.user_name = session.query(User.user_name).filter_by(id=self.id).first()[0]
        # self.email = session.query(User.email).filter_by(id=self.id).first()[0]

        self.firstname = session.query(User.first_name).filter_by(id=self.id).first()[0]
        self.surname = session.query(User.surname).filter_by(id=self.id).first()[0]

        self.fullname = self.firstname + ' ' + self.surname

    # This functions is used to save the message a client sents to the database
    def save(self, message, typ, conv_id, ts, message_status):
        
        if typ == 'group':
            session.add(GroupMessage(self.id, conv_id, message, ts, message_status))   # In this case, recipient_id is the recipient_group_id
        elif typ == 'personal':
            session.add(PersonalMessage(self.id, conv_id, message, ts, message_status))
   
        session.commit()

    #This function is used to send a message to the receiver
    async def send(self, message):
        await self.conn.send(message)
