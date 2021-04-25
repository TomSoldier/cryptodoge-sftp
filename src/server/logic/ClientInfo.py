import os
import sys

PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from utils.communication.MessageCompiler import MessageCompiler

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