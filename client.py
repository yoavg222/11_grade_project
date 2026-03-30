import socket

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from class_tcp_by_size import recvSend

# const
REG_MSG = "REG"
LOG_MSG = "LOG"
FOR_MSG = "FOR"
GOOD_MSG = False
SIGN_IN = False
KEY_OK = False
RSA_PUBLIC_KEY_REQUEST = "RSA|send me your public key"
RSA = "RSA"
DPH = "DPH"
input_data = ""
PRIVATE_MSG = "PRV"
PUBLIC_MSG = "PUB"
DELIMITER = "|"
user_name = ""
user_password = ""

SERVER_IP = "192.168.1.119"
SERVER_PORT = 12342


def create_aes_key():
    key = AESGCM.generate_key(bit_length=256)
    return key


def encrypted_rsa(server_public_key,aes_key):
    server_public_key = serialization.load_pem_public_key(server_public_key)
    encrypted_msg = server_public_key.encrypt(
        aes_key,padding.OAEP(
            mgf= padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None
        )
    )
    return encrypted_msg

def rsa_key_exchange(key,recv_send_client):
    recv_send_client.send_with_size(RSA)
    from_server = recv_send_client.recv_by_size().decode()
    if from_server != "RSA|OK":
        return False

    recv_send_client.send_with_size(RSA_PUBLIC_KEY_REQUEST)
    server_public_key = recv_send_client.recv_by_size()
    print(server_public_key)

    encrypted_aes_key = encrypted_rsa(server_public_key, key)
    recv_send_client.send_with_size(encrypted_aes_key)

def agree_on_aes_key(recv_send_client,key):
    global KEY_OK

    while not KEY_OK:
        radio_button = input("Diffie-hellman or RSA")
        if radio_button =="RSA" or radio_button == "rsa":
            success = rsa_key_exchange(key,recv_send_client)

            if success:
                return True
            return False


def main():

    client_socket = socket.socket()
    client_socket.connect((SERVER_IP, SERVER_PORT))

    recv_send_client = recvSend(client_socket,None)
    key = create_aes_key()
    print(key.hex())
    if agree_on_aes_key(recv_send_client,key):
        print("good")


    client_socket.close()









if __name__ == "__main__":
    main()