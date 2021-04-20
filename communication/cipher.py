from abc import abstractmethod
from Crypto.Cipher import AES

class Cipher:

    @abstractmethod
    def encrypt(self, plain: bytes):
        pass

    @abstractmethod
    def decrypt(self, cipher: bytes):
        pass