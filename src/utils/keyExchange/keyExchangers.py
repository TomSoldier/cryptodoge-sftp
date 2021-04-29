import os
import sys

PACKAGE_PARENT = '../..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from network.netinterface import network_interface
from diffiehellman.diffiehellman import DiffieHellman
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Hash import SHA512

class KeyExchanger:
    def __init__(self, network_interface: network_interface):
        self.interface = network_interface
        self.keyGen = DiffieHellman(key_length=256)

    def _calcNameConcatKey(self):
        self.keyGen.generate_public_key()
        sugKeyInt = self.keyGen.public_key

        name = bytes(self.interface.own_addr, "ascii")
        paddedName = bytes(32 - len(name))
        paddedName = b''.join([name, paddedName])

        # CHANGE: sugkey is 32 byte long in documentation, now it is 2^10 bytes long
        sugKey = sugKeyInt.to_bytes(1024, "big")

        return b''.join([paddedName, sugKey])
    pass


class ClientKeyExchanger(KeyExchanger):
    def __init__(self,
                 network_interface: network_interface,
                 publicSignatureKey: RsaKey,
                 serverAddress: str):
        super().__init__(network_interface)
        self.serverAddress = serverAddress
        self.publicSignatureKey = publicSignatureKey


    def clientExchangeKey(self):

        # 32 byte name; 1024 byte sugKey
        msg = super()._calcNameConcatKey()
        self.interface.send_msg(self.serverAddress, msg)

        # it is assumed, that the server has responded to the message with their part of the key:
        name, serverSugKey, body, signature = self.__waitServerResponse()

        self._verifySignature(body, signature)

        serverSugKeyInt = int.from_bytes(serverSugKey, "big")
        self.keyGen.generate_shared_secret(serverSugKeyInt)
        shared_key = self.keyGen.shared_key
        return bytes.fromhex(shared_key)

    def __waitServerResponse(self):
        status, resp = self.interface.receive_msg(blocking=True)
        name = resp[0:32]
        sugKey = resp[32:32+1024]
        body = resp[0: 32+1024]
        # CHANGE: signature size has been changed to 128 bytes, because of security length considerations
        signature = resp[-128:]

        return name, sugKey, body, signature

    def _verifySignature(self, body: bytes, signature: bytes):
        verifier = pkcs1_15.new(self.publicSignatureKey)

        hasher = SHA512.new()
        hasher.update(body)

        verifier.verify(hasher, signature)


class ServerKeyExchanger(KeyExchanger):
    def __init__(self,
                 network_interface: network_interface,
                 privateSignatureKey: RsaKey,
                 clientAddress: str,
                 clientSugKey: bytes):
        super().__init__(network_interface)
        self.privateSignatureKey = privateSignatureKey
        self.clientAddress = clientAddress
        self.clientSugKey = clientSugKey

    def serverExchangeKey(self):
        nameConcatSugKey = super()._calcNameConcatKey()

        # 32 byte name; 1024 byte sugKey; 32 byte signature
        msg = self._sign(nameConcatSugKey)

        self.interface.send_msg(self.clientAddress, msg)

        clientSugKeyInt = int.from_bytes(self.clientSugKey, "big")
        self.keyGen.generate_shared_secret(clientSugKeyInt)
        shared_key = self.keyGen.shared_key
        return bytes.fromhex(shared_key)

    def _sign(self, body):
        signer = pkcs1_15.new(self.privateSignatureKey)

        hasher = SHA512.new()
        hasher.update(body)

        signature = signer.sign(hasher)

        signed = b''.join([body, signature])

        return signed