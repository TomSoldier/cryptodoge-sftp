from abc import abstractmethod

class Cipher:

    @abstractmethod
    def encrypt(self, plain: bytes):
        pass

    @abstractmethod
    def decrypt(self, cipher: bytes):
        pass