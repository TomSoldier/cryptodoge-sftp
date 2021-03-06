import os

from Crypto.Cipher import AES
from utils.communication.cipher import Cipher

class AesGcmCipher(Cipher):

    def __init__(self, key: bytes):
        self.key = key
    '''
    :header: unencrypted part of the message
    :data: bytes to be encrypted
    :return returns nonce, header, ciphertext, tag in that order
    '''
    def encrypt(self, header: bytes, data: bytes):
        cipher = AES.new(self.key, AES.MODE_GCM)
        cipher.update(header)

        ciphertext, tag = cipher.encrypt_and_digest(data)

        return cipher.nonce, header, ciphertext, tag

    '''
    :header: unencrypeted part of received message
    :ciphertext: encrypted part of received message
    :tag: tag part of message
    :return plaintext
    '''
    def decrypt(self, nonce:bytes, header: bytes, ciphertext: bytes, tag: bytes):
        try:
            cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
            cipher.update(header)
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext
        except ValueError:
            print("Incorrect decryption")