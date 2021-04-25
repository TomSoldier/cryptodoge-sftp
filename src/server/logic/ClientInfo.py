from src.utils.communication.MessageCompiler import MessageCompiler

class ClientInfo():
    def __init__(self,
                 address,
                 sessionID: bytes,
                 msgCompiler: MessageCompiler):
        self.address = address
        self.sessionID = sessionID
        self.msgCompiler = msgCompiler

class Clients():
    
    def __init__(self):
        # ClientInfo list
        self.clients = []

    def add(self,
            address,
            sessionID: bytes,
            msgCompiler: MessageCompiler):
        self.clients.append(ClientInfo(address,sessionID,msgCompiler))

    def getBySID(sessionID):
        pass

    def getByAddr(address):
        pass