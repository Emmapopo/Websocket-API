#This defines the abstract client class. A abstract class defines the structure to be followed in terms of abstract methods. There's no implementation in an abstarct class.
class ClientAbstract:
    def __init__(self, id, conn):
        pass

    def populate(self, session):
        pass

    def save(self, session, message):
        pass

    async def send(self, message):
        pass
