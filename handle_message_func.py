#This code contains the HandleMessageClass with functions to handle all types of messages that a client can send

import asyncio
import sess
from sess import session
from sqlalchemy import and_
import json

from message_model.group_conv_mem import GroupConvMem
from message_model.personal_conv_mem import PersonalConvMem

from message_model.personal_conv_init import PersonalConvInit
from message_model.group_conv_init import GroupConvInit

from message_model.personal_message_model import PersonalMessage
from message_model.group_message_model import GroupMessage

from user_model import User
from client_controller.client import Client
from client_controller.clients import Clients
from client_controller.client import ClientAbstract
from client_controller.clients import ClientsAbstract

from platform_model.class_mem import ClassMem
from platform_model.class_message import ClassMessageSend, ClassMessageSendAttach, ClassMessageReply, ClassMessageReplyAttach
from platform_model.course_mem import CourseMem
from platform_model.course_message import CourseMessageSend, CourseMessageSendAttach, CourseMessageReply, CourseMessageReplyAttach

from user_model import User
from user_type import UserType

class HandleMessageFunc():
    def __init__(self, sender, clients, message, timestamp):
        self.sender  = sender
        self.clients = clients
        self.message = message
        self.timestamp = timestamp

   #Handles the sending of personal message 
    async def personal(self, user_id, typ, ts):
        conv_id = self.message['conv_id']
        recipient_id = session.query(PersonalConvMem.member_id).filter_by(conv_id=conv_id).all()
        recipient_id = [item for t in recipient_id for item in t]
        recipient_id.remove(int(user_id))   

        try:
            online_status = self.clients.get_client(str(recipient_id[0])) #Checks to see if the client is online so it can update the status as delivered
            print('online_status')
            message_status = 'delivered'

        except:
            message_status = 'sent' #If the client isn't online, it sets the message status as sent


        self.clients.save_client_message(user_id, self.message["msg"], typ, conv_id, ts, message_status)   #Save message to DB
        message_id = session.query(PersonalMessage.id).filter(and_(PersonalMessage.timestamp==ts,PersonalMessage.sender_id == user_id)).first()[0]
        self.message["message_id"] = message_id   #attach message_id to the message.
        self.message["timestamp"] = ts     #add timestamp to the message.

        # Sends message id to the sender back
        await self.clients.get_client(str(user_id)).send(json.dumps({"message_id": self.message["message_id"]}, indent=4, sort_keys=True, default=str))  

        try:
            for receiver in recipient_id:
                # sends message to the receiver
                await self.clients.get_client(str(receiver)).send(json.dumps(self.message, indent=4, sort_keys=True, default=str))

        except:
            pass


    #handles the group messages 
    async def group(self, user_id, typ, ts):
        conv_id = self.message['conv_id']
        recipient_id = session.query(GroupConvMem.member_id).filter_by(conv_id=conv_id).all()
        recipient_id = [item for t in recipient_id for item in t]
        print(recipient_id)
        recipient_id.remove(int(user_id))

        message_status = 'sent'   #For the group message, all sent messages are saved as 'sent'. No updating for delivered as seen

        self.clients.save_client_message(user_id, self.message["msg"], typ, conv_id, ts, message_status)
        message_id = session.query(GroupMessage.id).filter(and_(GroupMessage.timestamp == ts, GroupMessage.sender_id == user_id)).first()[0]
        self.message["message_id"] = message_id   #attach the message_is
        self.message["timestamp"] = ts   #attach the timestamp

        await self.clients.get_client(str(user_id)).send(json.dumps({'message_id':self.message["message_id"]})) #Sends message id to the sender back

        for receiver in recipient_id:
            # sends the message to a receiver that is online. If not, pass. The person will receive the message later through synchronization.
            try:
                await self.clients.get_client(str(receiver)).send(json.dumps(self.message, indent=4, sort_keys=True, default=str))
                session.query(GroupMessage).filter_by(id=message_id).update({'message_status':'delivered'})
                session.commit() 

            except:
                pass

    # Handles the 'seen' status message. Once a client sends this message, the personal message is set to seen. This functionality only works for Personal Message.
    def seen(self, message_id):
        session.query(PersonalMessage).filter_by(id=message_id).update({'message_status':'seen'})
        session.commit()


    async def init_personal(self, user_id):
        # Initializing a personal message {"conv_id": 5, "member": [1, 2], "type": "init_personal"}
        local_conv_id = self.message["conv_id"]
        mem = self.message["member"]

    
        # save the conversation id in the db
        session.add(PersonalConvInit(user_id, self.timestamp))

        # Get db conv_id
        db_conv_id = session.query(PersonalConvInit.conv_id).filter(and_(PersonalConvInit.timestamp == self.timestamp, PersonalConvInit.initiator_id == user_id)).first()[0]

        # send db_conv_id back to the sender so it can update it in their local db
        conv_id_update = {"local_conv_id": local_conv_id, "db_conv_id": db_conv_id, "type": "personal"}
        await self.clients.get_client(str(user_id)).send(json.dumps(conv_id_update))

        # save the members of a conv
        for i in mem:
            session.add(PersonalConvMem(db_conv_id, i))
        session.commit()

     
    async def init_group(self, user_id):
        # Initializing a personal message 
        # {"conv_id": 5, "member": [1, 2, 3], "group_name" : "Livescore", "description" : "A research group", "type": "init_group" }
        
        local_conv_id = self.message["conv_id"]
        mem = self.message["member"]
        group_name = self.message["group_name"]
        description = self.message["description"]


        # save the conversation id in the db
        session.add(GroupConvInit(user_id, group_name, description, self.timestamp))

        # Get db conv_id
        db_conv_id = session.query(GroupConvInit.conv_id).filter(and_(GroupConvInit.timestamp == self.timestamp, GroupConvInit.creator_id == user_id)).first()[0]

        # send db_conv_id back to the sender so it can update it in their local db
        conv_id_update = {"local_conv_id" : local_conv_id, "db_conv_id" : db_conv_id, "type": "group"}
        await self.clients.get_client(str(user_id)).send(json.dumps(conv_id_update))

        # save the members of a conv
        for i in mem:
            session.add(GroupConvMem(db_conv_id, i))
        session.commit()

    async def lec_class_assign(self, user_id):
        try:
            class_id = self.message['class_id']
            session.add(ClassMem(class_id, int(user_id)))
            session.commit()
            await self.clients.get_client(str(user_id)).send(json.dumps({"Status": "Successfully joined"}))

        except:
            await self.clients.get_client(str(user_id)).send(json.dumps({"Status": "Not successful"}))

    
    def confirm_user_lec(self, user_id):
        usertype = session.query(User.user_type).filter_by(id=user_id).first()[0]
        if usertype == UserType.Lecturer:
            x = 1
        else:
            x = 0

        return x

    async def send_class_message(self, user_id):
        class_id = self.message['class_id']
        title = self.message['title']
        content = self.message['content']
        files = self.message['attachments']
        user_id = int(user_id)

        # Get message recepients
        recipient_id = session.query(ClassMem.member_id).filter_by(class_id=class_id).all()
        recipient_id = [item for t in recipient_id for item in t]
        recipient_id.remove(int(user_id))
        print(recipient_id)

        # Save the message in the DB
        session.add(ClassMessageSend(user_id, class_id, title, content, self.timestamp))
        session.commit()

        # Get the message id from the database
        message_id = session.query(ClassMessageSend.id).filter(and_(ClassMessageSend.timestamp == self.timestamp, ClassMessageSend.sender_id == user_id)).first()[0]
        self.message['message_id'] = message_id

        # Save files if there are any
        if files != [] :
            for fil in files:
                session.add(ClassMessageSendAttach(message_id, fil))
                session.commit()

        # Sends message id to the sender back
        await self.clients.get_client(str(user_id)).send(json.dumps({"message_id": self.message["message_id"]}, indent=4, sort_keys=True, default=str))  

        # Send message back to the recievers
    
        for receiver in recipient_id:
            try:
                online = self.clients.get_client(str(receiver))
                await self.clients.get_client(str(receiver)).send(json.dumps(self.message, indent=4, sort_keys=True, default=str))

            except:
                continue

    


    async def reply_class_message (self, user_id):
        or_msg_id = self.message['message_id']
        print(type(or_msg_id))
        content = self.message['content']
        files = self.message['attachments']
        user_id = int(user_id)


        # Get message recepients
        class_id = session.query(ClassMessageSend.class_id).filter_by(id = or_msg_id).first()[0]
        recipient_id = session.query(ClassMem.member_id).filter_by(class_id=class_id).all()
        recipient_id = [item for t in recipient_id for item in t]
        recipient_id.remove(int(user_id))
        print(recipient_id)

        # Save the message in the DB
        model = ClassMessageReply(or_msg_id, user_id, content, self.timestamp)
        session.add(model)
        session.commit()

         # Get the message id from the database
        message_id = session.query(ClassMessageReply.id).filter(and_(ClassMessageReply.timestamp == self.timestamp, ClassMessageReply.sender_id == user_id)).first()[0]
        self.message['message_id'] = message_id

        # Save files if there are any
        if files != [] :
            for fil in files:
                session.add(ClassMessageReplyAttach(message_id, fil))
                session.commit()

        # Sends message id to the sender back
        await self.clients.get_client(str(user_id)).send(json.dumps({"message_id": self.message["message_id"]}, indent=4, sort_keys=True, default=str))  

        # Send message back to the recievers
        for receiver in recipient_id:
            try:
                online = self.clients.get_client(str(receiver))
                await self.clients.get_client(str(receiver)).send(json.dumps(self.message, indent=4, sort_keys=True, default=str))

            except:
                continue



    async def send_course_message(self, user_id):
        course_id = self.message['course_id']
        title = self.message['title']
        content = self.message['content']
        files = self.message['attachments']
        user_id = int(user_id)

        # Get message recepients
        recipient_id = session.query(CourseMem.member_id).filter_by(course_id=course_id).all()
        recipient_id = [item for t in recipient_id for item in t]
        recipient_id.remove(int(user_id))

        # Save the message in the DB
        # session.add(CourseMessageSend(user_id, course_id, title, content, self.timestamp))
        # session.commit()

        model = CourseMessageSend(user_id, course_id, title, content, self.timestamp)
        session.add(model)
        session.commit

        # Get the message id from the database
        message_id = session.query(CourseMessageSend.id).filter(and_(CourseMessageSend.timestamp == self.timestamp, CourseMessageSend.sender_id == user_id)).first()[0]
        self.message['message_id'] = message_id

        # Save files if there are any
        if files != [] :
            for fil in files:
                session.add(CourseMessageSendAttach(message_id, fil))
                session.commit()

        # Sends message id to the sender back
        await self.clients.get_client(str(user_id)).send(json.dumps({"message_id": self.message["message_id"]}, indent=4, sort_keys=True, default=str))  

        # Send message back to the recievers
        for receiver in recipient_id:
            try:
                online = self.clients.get_client(str(receiver))
                await self.clients.get_client(str(receiver)).send(json.dumps(self.message, indent=4, sort_keys=True, default=str))

            except:
                continue

    

    async def reply_course_message (self, user_id):
        or_msg_id = self.message['message_id']
        content = self.message['content']
        files = self.message['attachments']
        user_id = int(user_id)


        # Get message recepients
        course_id = session.query(CourseMessageSend.course_id).filter_by(id = or_msg_id).first()[0]
        recipient_id = session.query(CourseMem.member_id).filter_by(course_id=course_id).all()
        recipient_id = [item for t in recipient_id for item in t]
        recipient_id.remove(int(user_id))

        # Save the message in the DB
        session.add(CourseMessageReply(or_msg_id, user_id, content, self.timestamp))
        session.commit()

         # Get the message id from the database
        message_id = session.query(CourseMessageReply.id).filter(and_(CourseMessageReply.timestamp == self.timestamp, CourseMessageReply.sender_id == user_id)).first()[0]
        self.message['message_id'] = message_id

        # Save files if there are any
        if files != [] :
            for fil in files:
                session.add(CourseMessageReplyAttach(message_id, fil))
                session.commit()

        # Sends message id to the sender back
        await self.clients.get_client(str(user_id)).send(json.dumps({"message_id": self.message["message_id"]}, indent=4, sort_keys=True, default=str))  

        # Send message back to the recievers
        for receiver in recipient_id:
            try:
                online = self.clients.get_client(str(receiver))
                await self.clients.get_client(str(receiver)).send(json.dumps(self.message, indent=4, sort_keys=True, default=str))

            except:
                continue
    
    
    









    







