import getopt
import os
import sys
from Crypto.PublicKey import RSA

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# noinspection PyUnresolvedReferences
from network.netinterface import network_interface
# noinspection PyUnresolvedReferences
from utils.keyExchange.keyExchangers import ServerKeyExchanger

class Server:

    def __init__(self,
                 netPath: str = "../network/files/",
                 ownAddr: str = "A"):
        self.netPath = netPath
        self.ownAddr = ownAddr

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
        self.symKey = exchanger.serverExchangeKey()
        return True

    def run(self):
        print('Main loop started...')
        while True:
            status, msg = self.netif.receive_msg(blocking=True)
            if self.handleExchange(msg):
                continue


try:
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

try:
    Server(NET_PATH, OWN_ADDR).run()
except:
    try:
        Server(NET_PATH).run()
    except:
        Server(ownAddr=OWN_ADDR).run()