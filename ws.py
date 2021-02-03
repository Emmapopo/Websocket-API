# Make sure you split classes into appropriate files

import asyncio
import websockets
from websockets import exceptions
from multiprocessing.dummy import Pool
import json
import datetime
import MySQLdb
import sess
from sqlalchemy.orm import sessionmaker
from sess import session

from client_controller.client import Client
from client_controller.clients import Clients
from client_controller.client import ClientAbstract
from client_controller.clients import ClientsAbstract

from handle_message_func import HandleMessageFunc

from get_messages import *



class WS(object):
    def __init__(self, clients):
        if not isinstance(clients, ClientsAbstract):
            raise TypeError("clients must be an instance of ClientsAbstract")
        self.clients = clients

    # @asyncio.coroutine
    async def handler(self, websocket, path):
        # the client will send back user id on connection open
        user_id = str(await websocket.recv())
        user_id_int = int(user_id)
        self.clients.add_client(Client(user_id, websocket))
        await websocket.send("user id " + user_id + " received")

        # This step is to look for all undelivered message and deliver it to the client
        conv_ids = get_personal_conv_ids(user_id_int)
        for conv_id in conv_ids:
            messages = get_personal_messages(conv_id, user_id_int)
        
            if messages != []:
                await send_undelivered_personal_messages(messages, websocket)

        session.commit()  #Commit all changes made to the database

        # This step is to look for all the undelivered message sent by lecturers to the class
              

        while True:
            try:
                message = await websocket.recv()
                ts = datetime.datetime.now()

                # Handle message
                message = json.loads(message)   #Jsonify the message
                asyncio.gather(self.handleMessage(user_id, self.clients.get_client(user_id), message, ts))    #Handle the message
                    
                print("got here")

            except exceptions.ConnectionClosedError as error:
                print("connection closed from client")
                self.clients.delete_client(user_id)
                break
            

    
    async def handleMessage(self, user_id, client, message, ts):
        # Personal message is of the form {"msg": "A simple message", "conv_id": 2, "type": "personal"}
        # Group message is of the form {"msg": "A simple message", "conv_id": 2, "type": "group"}
        # seen notification is of the form {"message_id": [74, 75], "type": "seen"}
        # Initializing a personal message {"conv_id": 5, "member": [1, 2], "type": "init_personal"}
        # Initializing a group message {"conv_id": 5, "member": [1, 2, 3], "group_name" : "Livescore", "description" : "A research group", "type": "init_group" }
        
        # Lecturer assigning as a class adviser is of the form {"class_id": 1, "type": "lec_class_assign"}
        # Lecturer sending message to a class {"class_id" : 1, "title" : "test questions", "content": "submit your assignment on time", "attachments": ["http://123jh", "http://23jloo"], "type": "send_class_message"}
        # Replying a lecturer's message is of the form {"message_id" : 1, "content": "What textbook sir?", "attachments": ["http://123jh", "http://23jloo"], "type": "reply_class_message"}

        # Lecturer sending message to a course is of the form {"course_id" : 1, "title" : "test questions", "content": "submit your assignment on time", "attachments": ["http://123jh", "http://23jloo"], "type": "send_course_message"}
        # Replying a lecturer's message is of the form {"message_id" : 1, "content": "What textbook sir?", "attachments": ["http://123jh", "http://23jloo"], "type": "reply_course_message"}
        
        typ = message['type']  #what type of message is it?
        message["sender"] = client.fullname # adding the sender id to message

        A = HandleMessageFunc(client, self.clients, message, ts)  # call the handlefunc class

        if typ == 'personal':
            await A.personal(user_id, typ, ts)

        elif typ == 'group':
            await A.group(user_id, typ, ts)  

        elif typ == 'seen':
            msg_id = message['message_id']
            for i in msg_id:
                A.seen(i)   

        elif typ == 'init_personal':
            await A.init_personal(user_id)

        elif typ == 'init_group':
            await A.init_group(user_id)

        elif typ == 'lec_class_assign':
            await A.lec_class_assign(user_id)

        elif typ == 'send_class_message':        
            if A.confirm_user_lec(user_id) == 1: # This line of code confirms that it is a lecturer sending the command
                await A.send_class_message(user_id)  # This line of code allows the lecturer to send the class message

        elif typ == 'reply_class_message':
            await A.reply_class_message(user_id)  # This line allows anybody to reply to the lecturer's message

        elif typ == 'send_course_message':
            if A.confirm_user_lec(user_id) == 1: # This line of code confirms that it is a lecturer sending the command
                await A.send_course_message(user_id)

        elif typ == 'reply_course_message':
            await A.reply_course_message(user_id)  # This line allows anybody to reply to the lecturer's message
            

        await asyncio.sleep(5)  # you can remove this. This is just to simulate a function that takes long
        print("finished async")



LISTEN_ADDRESS = ('0.0.0.0', 3128)

server = WS(Clients(session))
start_server = websockets.serve(server.handler, *LISTEN_ADDRESS)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
