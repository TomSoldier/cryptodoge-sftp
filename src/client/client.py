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

'''NET_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..\\network\\traffic\\'))
print(NET_PATH)'''

# TODO: these were only added for convenience, should be removed in a future commit
NET_PATH = "../network/files/"
OWN_ADDR = "B"
# TODO_END


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
        NET_PATH = arg
    elif opt == '-a' or opt == '--addr':
        OWN_ADDR = arg

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

global pubKey
if not os.path.exists("pubKey.pem"):
    raise FileNotFoundError("File containing public key can't be found.")
else:
    with open("pubKey.pem", "r") as handle:
        pubKey = RSA.import_key(handle.read())



# main loop
print('Main loop started')
serverAddr = 'A'
validator = Validator()
netif = network_interface(NET_PATH, OWN_ADDR)

exchange = ClientKeyExchanger(
                 netif,
                 pubKey,
                 serverAddr)
symKey = exchange.clientExchangeKey()
print(symKey)

while True:
    msg = input('# ')

    if(msg == 'exit'):
        break

    if(msg == "help"):
        validator.help()

    try:
        if(validator.validate(msg)):
            netif.send_msg(serverAddr, msg.encode('utf-8'))
    except InputError as err:
        print(err.message)
