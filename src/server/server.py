import os
import sys
import getopt
from Crypto.PublicKey import RSA
import time
import pickle as pkl

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# noinspection PyUnresolvedReferences
from network.netinterface import network_interface
# noinspection PyUnresolvedReferences
from utils.keyExchange.keyExchangers import ServerKeyExchanger

NET_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..\\network\\traffic\\'))
OWN_ADDR = 'B'
print(NET_PATH)
# ------------
# main program
# ------------

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

# TODO: these were only added for convenience, should be removed in a future commit
NET_PATH = "../network/files/"
OWN_ADDR = "A"
# TODO_END

if (NET_PATH[-1] != '/') and (NET_PATH[-1] != '\\'):
    NET_PATH += '/'

if not os.access(NET_PATH, os.F_OK):
    print('Error: Cannot access path ' + NET_PATH)
    sys.exit(1)

if len(OWN_ADDR) > 1:
    OWN_ADDR = OWN_ADDR[0]

if OWN_ADDR not in network_interface.addr_space:
    print('Error: Invalid address ' + OWN_ADDR)
    sys.exit(1)

global privKey
global pubKey
if not os.path.exists("privKey.pem"):
    privKey=RSA.generate(1024)
    pubKey=privKey.public_key()
    with open("privKey.pem", "wb") as handle:
        handle.write(privKey.export_key('PEM'))
else:
    with open("privKey.pem", "r") as handle:
        privKey = RSA.import_key(handle.read())

if not os.path.exists("../client/pubKey.pem"):
    with open("../client/pubKey.pem", "wb") as handle:
        handle.write(pubKey.export_key("PEM"))
# main loop
netif = network_interface(NET_PATH, OWN_ADDR)
print('Main loop started...')

def handleExchange(msg):
    if len(msg) != 32+1024:
        return False
    exchangeSource = msg[0:32]
    zero = bytes.fromhex("00")
    i = 31
    while exchangeSource[i] == 0:
        i -= 1
    exchangeSource = exchangeSource[:i + 1].decode("ascii")

    exchanger = ServerKeyExchanger(netif, privKey, exchangeSource, msg[32:])
    symKey = exchanger.serverExchangeKey()
    print(symKey)
    return True


while True:
    status, msg = netif.receive_msg(blocking=True)
    if handleExchange(msg):
        continue

