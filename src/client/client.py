import os
import sys
import getopt
import time

from ..utils.validation.validator import Validator
from ..utils.validation.error import InputError
from ..network.netinterface import network_interface

NET_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..\\network\\traffic\\'))
print(NET_PATH)
OWN_ADDR = 'A'

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


# main loop
print('Main loop started')
destination = 'B'
validator = Validator()
netif = network_interface(NET_PATH, OWN_ADDR)

while True:
    msg = input('# ')

    if(msg == 'exit'):
        break

    if(msg == "help"):
        validator.help()

    try:
        if(validator.validate(msg)):
            netif.send_msg(destination, msg.encode('utf-8'))
    except InputError as err:
        print(err.message)
