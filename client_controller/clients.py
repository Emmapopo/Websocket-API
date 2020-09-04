#This class defines the methods of all clients
from client_model.clients_abstract import ClientsAbstract
from client_model.client_abstract import ClientAbstract
from sess import session


class Clients(ClientsAbstract):
    def __init__(self, session):
        self.session = session
        self.clients = {}

    #This method is to add a new client to the client lists
    def add_client(self, client):
        if not isinstance(client, ClientAbstract):
            raise TypeError("client must be an instance of ClientAbstract")
        client.populate(self.session)
        self.clients[client.id] = client

    #This method is to delete a client from the client lists
    def delete_client(self, id):
        del self.clients[id]

    # #This method is get a client from the client lists based on the client's id
    def get_client(self, id):
        return self.clients[id]

    #This function is to save the message of a client. It calls the 'save' method in the Client class.
    def save_client_message(self, id, message, typ, conv_id, ts, message_status):
        self.clients[id].save(message, typ, conv_id, ts, message_status)
