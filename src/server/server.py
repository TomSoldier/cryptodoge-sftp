import getopt
import os
import sys
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Hash import MD5
from logic.ClientInfo import Clients,ClientInfo
from users import users

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from utils.communication.MessageCompiler import MessageCompiler


# noinspection PyUnresolvedReferences
from network.netinterface import network_interface
# noinspection PyUnresolvedReferences
from utils.keyExchange.keyExchangers import ServerKeyExchanger
from logic.processor import Processor

class Server:

    def __init__(self,
                 netPath: str = "../network/files/",
                 ownAddr: str = "A"):
        self.netPath = netPath
        self.ownAddr = ownAddr
        self.clients = Clients()

        self.init()

        self.initKeys()

    def init(self):
        '''try:
            opts, args = getopt.getopt(sys.argv[1:], shortopts='hp:a:', longopts=[
                'help', 'path=', 'addr='])
        except getopt.GetoptError:
            print('Usage: python receiver.py -p <network path> -a <own addr>')
            sys.exit(1)
        
        for opt, arg in opts:
            if opt == '-h' or opt == '--help':
                print('Usage: python receiver.py -p <network path> -a <own addr>')
                sys.exit(0)
            elif opt == '-p' or opt == '--path':
                NET_PATH = arg
            elif opt == '-a' or opt == '--addr':
                OWN_ADDR = arg
        '''
        if (self.netPath[-1] != '/') and (self.netPath[-1] != '\\'):
            self.netPath += '/'

        if not os.path.exists(self.netPath):
            os.makedirs(self.netPath)

        if len(self.ownAddr) > 1:
            self.ownAddr = self.ownAddr[0]

        if self.ownAddr not in network_interface.addr_space:
            print('Error: Invalid address ' + self.ownAddr)
            sys.exit(1)

        self.netif = network_interface(self.netPath, self.ownAddr)

    def initKeys(self):
        if not os.path.exists("privKey.pem"):
            self.privKey = RSA.generate(1024)
            self.pubKey = self.privKey.public_key()
            with open("privKey.pem", "wb") as handle:
                handle.write(self.privKey.export_key('PEM'))
        else:
            with open("privKey.pem", "r") as handle:
                self.privKey = RSA.import_key(handle.read())

        if not os.path.exists("../client/pubKey.pem"):
            with open("../client/pubKey.pem", "wb") as handle:
                handle.write(self.pubKey.export_key("PEM"))

    def handleExchange(self, msg):
        if len(msg) != 32+1024:
            return False
        try:
            msg[0:32].decode("ascii")
        except:
            return False
        exchangeSource = msg[0:32]
        zero = bytes.fromhex("00")
        i = 31
        while exchangeSource[i] == 0:
            i -= 1
        exchangeSource = exchangeSource[:i + 1].decode("ascii")

        exchanger = ServerKeyExchanger(self.netif, self.privKey, exchangeSource, msg[32:])
        self.symKey: bytes = exchanger.serverExchangeKey()
        self.handleClientInfo(self.symKey,exchangeSource)
        return True

    def handleClientInfo(self, symKey:bytes, clientAddr):
        # Generate Client parameters, and save them
        sessionID = get_random_bytes(16)    
        msgComp = MessageCompiler(symKey, sessionID)
        self.clients.add(clientAddr, sessionID, msgComp)
        # Send SessionID to client
        sidTransferMessage = msgComp.compileFirstMessage()
        self.netif.send_msg(clientAddr, sidTransferMessage)

    def login(self, session: ClientInfo, msg: str):
        print(msg)
        parts = msg.split(' ')
        username = parts[1].split('=')[1]
        passwd = parts[2].split('=')[1].encode('ascii')
        if username not in users.users:
            return False

        h = MD5.new()
        h.update(passwd)
        if h.hexdigest() == users.users[username]:
            session.userName = username
            self.processor = Processor(username)
            return True
        return False

    def run(self):
        print('Main loop started...')
        while True:
            status, msg = self.netif.receive_msg(blocking=True)
            if self.handleExchange(msg):
                continue
            SID = msg[16:32]
            session = self.clients.getBySID(SID)
            d_cmd, d_msg = session.msgCompiler.decompile(msg)

            if d_cmd == b'lgn':
                result = self.login(session, d_msg.decode('ascii'))
                msgs = session.msgCompiler.compile(str(result).encode('ascii'), b'lgn')
                for m in msgs:
                    self.netif.send_msg(session.address, m)
            if d_cmd == b'ext':
                self.clients.removeBySID(SID)

            else:
                try:
                    if d_cmd == b'upl' or d_cmd == b'dnl':
                        origCmd = d_cmd
                        status, msg = self.netif.receive_msg(blocking=True)
                        d_cmd, tmpMsg = session.msgCompiler.decompile(msg)
                        while d_cmd.decode("ascii") != "end":
                            d_msg += tmpMsg
                            status, msg = self.netif.receive_msg(blocking=True)
                            d_cmd, tmpMsg = session.msgCompiler.decompile(msg)
                        d_cmd = origCmd
                    ret = self.processor.process(d_msg.decode('ascii'))
                    if ret is not None:
                        retMsg = session.msgCompiler.compile(ret, d_cmd)
                        for m in retMsg:
                            self.netif.send_msg(session.address, m)
                except Exception as ex:
                    msgs = session.msgCompiler.compile(str(ex).encode('ascii'), b'err')
                    for m in msgs:
                        self.netif.send_msg(session.address, m)




try:
    opts, args = getopt.getopt(sys.argv[1:], shortopts='hp:a:', longopts=[
        'help', 'path=', 'addr='])
except getopt.GetoptError:
    print('Usage: python server.py -p <network path> -a <own addr>')
    sys.exit(1)

for opt, arg in opts:
    if opt == '-h' or opt == '--help':
        print('Usage: python server.py -p <network path> -a <own addr>')
        sys.exit(0)
    elif opt == '-p' or opt == '--path':
        NET_PATH = arg
    elif opt == '-a' or opt == '--addr':
        OWN_ADDR = arg

for u in users.users:
    if not os.path.exists(u):
        os.mkdir(u)

if ('NET_PATH' in locals() or 'NET_PATH' in globals()) and ('OWN_ADDR' in locals() or 'OWN_ADDR' in globals()):
    Server(NET_PATH, OWN_ADDR).run()
elif ('NET_PATH' not in locals() and 'NET_PATH' not in globals()) and ('OWN_ADDR' in locals() or 'OWN_ADDR' in globals()):
    Server(ownAddr=OWN_ADDR).run()
elif ('NET_PATH' in locals() or 'NET_PATH' in globals()) and ('OWN_ADDR' not in locals() and 'OWN_ADDR' not in globals()):
    Server(NET_PATH).run()
else:
    Server().run()

