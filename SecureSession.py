from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os


class SecureSession_AES:
    def __init__(self,key,aad = b""):
        self.aes_key = AESGCM(key)
        self.aad = aad


    def encrypt(self,plaintext):
        nonce = os.urandom(12)
        ciphertext = self.aes_key.encrypt(nonce,plaintext,self.aad)
        return nonce + ciphertext

    def decrypt(self,data):
        nonce = data[:12]
        ciphertext = data[12:]
        return self.aes_key.decrypt(nonce,ciphertext,self.aad)

