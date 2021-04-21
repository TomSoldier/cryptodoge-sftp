import os
import sys
import getopt
import time
from ..network.netinterface import network_interface

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
netif = network_interface(NET_PATH, OWN_ADDR)
print('Main loop started...')
while True:
    status, msg = netif.receive_msg(blocking=True)
    print(msg.decode('utf-8'))
