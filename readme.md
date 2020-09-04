This the Websocket API

To setup:
1) Run the requirement.txt file
2) Set the environment variables:
    a) mysql_host
    b) mysql_password
    c) mysql_user
    d) db_name - (Database name)

3) Run the ws.py file

The Websocket API is used for real-time connection between clients

To make a connection to the websocket:
1) Enter the URI : ws://localhost:3128   and make a connection            In this case, '3128' is the port the websocket is running on. 
2) The first message to be sent is the user id. It then returns "user id <id> received"

Once a connection is made, it returns all the pending messages yet to be delivered. 

TO SEND A MESSAGE
Here are the accepted format for the messages:

There are 5 types of messages that can be sent


1) Initializing a Personal message
Initializing a personal message is of the form: {"conv_id": 5, "member": [1, 2], "type": "init_personal"}
where:
"conv_id" is the local conv_id saved by the client on their device
"member" is a list of the user_ids of the two people in the conversation
"type" will always be "init_personal" for this message type. 

Then it returns to the client:
{"local_conv_id": 5, "db_conv_id": 1, "type": "personal"}
where "local_conv_id" is the conversation id that was sent, and
db_conv_id  is the conversation id that it was saved in the database
"type" is personal so it can check in the personal db.

Thereafter, the client can update his/her local device with the correct conversation id. 


2) Sending a Personal Message
Personal message is of the form:  {"msg": "A simple message", "conv_id": 2, "type": "personal"}

where:
 "msg" is the message to be sent
 "conv_id" is the local conversation id
 "type" is the type which is personal for sending personal messages.

 To the client, it returns:
 {
    "message_id": 1
 }

 To the receiver, it sends:
 {
    "conv_id": 2,
    "message_id": 1,
    "msg": "A simple message",
    "sender": "Dakola Timmy",
    "timestamp": "2020-08-25 11:53:30.923631",
    "type": "personal"
 }




3) Initializing a Group message
Initializing a group message {"conv_id": 5, "member": [1, 2, 3], "group_name" : "Livescore", "description" : "A research group", "type": "init_group" }

where:
"conv_id" is the local conv_id the sender uses to save the group on their local device
"member" is a list of user id of people in the group
"group_name" is the name of the group
"description" is a brief description of what the group is about
"type" is "init_group" for initializing a group message.

Once the client sends the message, it returns

{"local_conv_id": 5, "db_conv_id": 1, "type": "group"}
where "local_conv_id" is the conversation id that was sent, and
db_conv_id  is the conversation id that it was saved in the database
"type" is group so it can check in the group db.



4) Sending a Group Message
Group message is of the form: 
{"msg": "A simple message", "conv_id": 2, "type": "group"}

where:

 "msg" is the message to be sent
 "conv_id" is the local conversation id
 "type" is the type which is group for sending personal messages.

to the client, it returns:

{"message_id": 6}
This is the message id in the database so it can update it. 


To members of the group that are online, it sends:

{
    "conv_id": 2,
    "message_id": 6,
    "msg": "A simple message",
    "sender": "Dakola Timmy",
    "timestamp": "2020-08-25 12:11:11.674772",
    "type": "group"
}

NOTE: For users that are not online, they will not receive the message. Later I will implement synchronization to handle that. 




5) Sending Seen Notification [for personal message]

Once a user sends a message, if the recipient is online, it saves the message as delivered. 
If the recipient is offline it saves the message as sent. 

Now, when the recipient comes online, s/he automatically receives all the personal messages that are yet to be delivered. The message status is then updated as delivered in the database. 

Now, when a receiver opens a message to read, it sends a seen notofication to the web server so it can be updated in the database. 

Seen notification is of the form: {"message_id": [74, 75], "type": "seen"}
where:
"message_id" is a list of all the messages that have been opened
"seen" is just the type of message to dinstiguish it from other message types. 

Then it updates the message statuses as seen in the database.



