#This defines the abstract clients class. A abstract class defines the structure to be followed in terms of abstract methods. There's no implementation in an abstarct class.
class ClientsAbstract:
    def __init__(self):
        pass

    def add_client(self, client):
        pass

    def delete_client(self, id):
        pass

    def get_client(self, id):
        pass

    def save_client_message(self, id, message):
        pass
