import os
import sys
from typing import List

PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from utils.communication.MessageCompiler import MessageCompiler

class ClientInfo():
    def __init__(self,
                 address: str,
                 sessionID: bytes,
                 msgCompiler: MessageCompiler,
                 userName: str = ""):
        self.address = address
        self.sessionID = sessionID
        self.msgCompiler = msgCompiler
        self.userName = userName
        self.banned = False

class Clients():
    
    def __init__(self):
        # ClientInfo list
        self.clients: List[ClientInfo] = []

    def add(self,
            address,
            sessionID: bytes,
            msgCompiler: MessageCompiler):
        self.clients.append(ClientInfo(address,sessionID,msgCompiler, ''))

    def getBySID(self, sessionID: bytes):
        for el in self.clients:
            if el.sessionID == sessionID:
                return el

    def getByAddr(self, address: str):
        for el in self.clients:
            if el.address == address:
                return el
