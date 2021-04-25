import os
import sys
import getopt
from Crypto.PublicKey import RSA

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# noinspection PyUnresolvedReferences
from utils.validation.validator import Validator
# noinspection PyUnresolvedReferences
from utils.validation.error import InputError
# noinspection PyUnresolvedReferences
from network.netinterface import network_interface
# noinspection PyUnresolvedReferences
from utils.keyExchange.keyExchangers import ClientKeyExchanger

from utils.communication.MessageCompiler import MessageCompiler


class Client:
    def __init__(self,
                 netPath: str = "../network/files/",
                 ownAddr: str = "B",
                 serverAddr: str = "A"):
        self.netPath = netPath
        self.ownAddr = ownAddr
        self.serverAddr = serverAddr
        self.validator = Validator()
        self.pubKey = None
        self.symKey = None

        self.init()

        self.initKeys()

    def init(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], shortopts='hp:a:', longopts=[
                'help', 'path=', 'addr='])
        except getopt.GetoptError:
            print('Usage: python client.py -p <network path> -a <own addr>')
            sys.exit(1)

        for opt, arg in opts:
            if opt == '-h' or opt == '--help':
                print('Usage: python sender.py -p <network path> -a <own addr>')
                sys.exit(0)
            elif opt == '-p' or opt == '--path':
                self.netPath = arg
            elif opt == '-a' or opt == '--addr':
                self.ownAddr = arg

        if (self.netPath[-1] != '/') and (self.netPath[-1] != '\\'):
            self.netPath += '/'

        if not os.access(self.netPath, os.F_OK):
            print('Error: Cannot access path ' + self.netPath)
            sys.exit(1)

        if len(self.ownAddr) > 1:
            self.ownAddr = self.ownAddr[0]

        if self.ownAddr not in network_interface.addr_space:
            print('Error: Invalid address ' + self.ownAddr)
            sys.exit(1)

        self.netif = network_interface(self.netPath, self.ownAddr)

    def initKeys(self):
        if not os.path.exists("pubKey.pem"):
            raise FileNotFoundError("File containing public key can't be found.")
        else:
            with open("pubKey.pem", "r") as handle:
                self.pubKey = RSA.import_key(handle.read())

    def exchangeKeys(self):
        exchange = ClientKeyExchanger(
            self.netif,
            self.pubKey,
            self.serverAddr)
        self.symKey = exchange.clientExchangeKey()
        status, msg = self.netif.receive_msg(blocking=True)
        SID = msg[16:32]
        self.messageCompiler = MessageCompiler(self.symKey, SID)
        cmd, decryptedSID = self.messageCompiler.decompile(msg)
        zero = (0).to_bytes(3, "big")
        if SID != decryptedSID or cmd != zero:
            raise ValueError("SID in message doesnt match SID in header.")



    def run(self):
        print('Main loop started')
        self.exchangeKeys()
        while True:
            msg = input('# ')

            if msg == 'exit':
                break

            if msg == "help":
                self.validator.help()

            try:
                if self.validator.validate(msg):
                    self.netif.send_msg(self.serverAddr, msg.encode('utf-8'))
            except InputError as err:
                print(err.message)


Client().run()
