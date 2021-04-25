from abc import abstractmethod

class Cipher:

    '''
    header: unencrypted part of the message
    data: bytes to be encrypted
    '''
    @abstractmethod
    def encrypt(self, header: bytes, data: bytes):
        pass

    '''
    header: unencrypeted part of received message
    ciphertext: encrypted part of received message
    tag: tag part of message
    '''
    @abstractmethod
    def decrypt(self, nonce:bytes, header: bytes, ciphertext: bytes, tag: bytes):
        pass