from pepper import pepper_users
import os
import hashlib

class SecureHasher:
    def __init__(self):
        self.pepper = pepper_users
        self.salt_length = 16


    def hash_salt_pepper_password(self,password):

        salt_bytes = os.urandom(16)
        salt_hex = salt_bytes.hex()

        password_hash = hashlib.sha256((salt_hex + password + self.pepper).encode())
        return password_hash.hexdigest(),salt_bytes.hex()
