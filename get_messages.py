
# This function is to retreive the undelivered messages for a client once s/he connects
import sess
from sess import session
from sqlalchemy import and_
import asyncio
import json

from user_model import User

from message_model.group_conv_mem import GroupConvMem
from message_model.personal_conv_mem import PersonalConvMem
from message_model.status import MessageStatus

from message_model.personal_message_model import PersonalMessage
from message_model.group_message_model import GroupMessage

# This functions get conversation_id a user is part of. 
def get_personal_conv_ids(user_id):
    conv_ids = session.query(PersonalConvMem.conv_id).filter_by(member_id=user_id).all()
    conv_ids = [item for t in conv_ids for item in t]
    return conv_ids

def get_personal_messages(conv_id, user_id):
    #Limited to check Personal Message Table (The != indicates it should no select messages that he was the sender)
    messages = session.query(PersonalMessage).filter(and_(PersonalMessage.conv_id==conv_id,PersonalMessage.message_status == 'sent', PersonalMessage.sender_id != user_id)).all()
    return messages

def get_sender_name(id):   #The is heere is the user_id
    firstname = session.query(User.first_name).filter_by(id=id).first()[0]
    surname = session.query(User.surname).filter_by(id=id).first()[0]
    fullname = firstname + ' ' + surname
    return fullname

#This function updates the status of a message to delivered once the reciever gets it to their end.
def update_status(message_id):
    session.query(PersonalMessage).filter_by(id=message_id).update({'message_status': MessageStatus.delivered})
    

#This code is used to send the undelievered message
async def send_undelivered_personal_messages(messages, websocket):
    for message in messages:
        message = message.__dict__
        # del message['_sa_instance_state']
        del message['message_status']
        
        sender_id = message['sender_id']
        fullname = get_sender_name(sender_id)  # get sender name

        message['sender'] = fullname 

        await websocket.send(json.dumps(message, indent=4, sort_keys=True, default=str))
        update_status(message['id'])     #Update message_id

    

