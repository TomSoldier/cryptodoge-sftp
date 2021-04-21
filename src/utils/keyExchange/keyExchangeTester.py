from keyExchangers import ClientKeyExchanger, ServerKeyExchanger
from src.network.netinterface import network_interface
from Crypto.PublicKey import RSA

def test():
    private = RSA.generate(1024)
    public = private.public_key()

    clientNetwork = network_interface("C", "C")
    serverNetwork = network_interface("S", "S")

    c = ClientKeyExchanger(clientNetwork, public, "S")
    cBody = c._calcNameConcatKey()

    s = ServerKeyExchanger(serverNetwork, private, "C", cBody[-1024:])

    nameConcatSugKey = s._calcNameConcatKey()

    # 32 byte name; 1024 byte sugKey; 32 byte signature
    msg = s._sign(nameConcatSugKey)

    clientSugKeyInt = int.from_bytes(s.clientSugKey, "big")
    s.keyGen.generate_shared_secret(clientSugKeyInt)

    ## server sends to client

    name = msg[0:32]
    serverSugKey = msg[32:32 + 1024]
    body = msg[0: 32 + 1024]
    signature = msg[-128:]

    c._verifySignature(body, signature)

    serverSugKeyInt = int.from_bytes(serverSugKey, "big")
    c.keyGen.generate_shared_secret(serverSugKeyInt)

    if s.keyGen.shared_key == c.keyGen.shared_key:
        print("Keys are identical")
        print("signature verification has succeeded")
test()