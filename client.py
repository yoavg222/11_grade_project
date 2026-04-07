import socket
from tkinter import *
from GUI_submarines import page
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF



from constants import RSA_PUBLIC_KEY_REQUEST, RSA, DPH, PRIVATE_MSG, PUBLIC_MSG,DELIMITER,SERVER_IP,SERVER_PORT,NUM_OF_CUPS,HOME_BUTTON,GOOD_EMAIL_CODE,RSA_MSG,DH_MSG,DH_PUBLIC_KEY_MSG,DELIMITER2
GOOD_MSG = False
SIGN_IN = False
KEY_OK = False


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
    if from_server != RSA_MSG:
        return False,None

    recv_send_client.send_with_size(RSA_PUBLIC_KEY_REQUEST)
    server_public_key = recv_send_client.recv_by_size()
    print(server_public_key)

    encrypted_aes_key = encrypted_rsa(server_public_key, key)
    recv_send_client.send_with_size(encrypted_aes_key)

    return True,key

def check_digital_signature(rsa_public_key,msg,signature_msg):
    public_key_rsa = serialization.load_pem_public_key(rsa_public_key)
    try:
        public_key_rsa.verify(
            signature_msg,
            msg,
            padding.PSS(
                mgf = padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()

        )
        return True

    except Exception as err:
        print(err)
        return False


def df_key_exchange(recv_send_client):
    recv_send_client.send_with_size(DPH)
    recv_send_client.send_with_size(DH_PUBLIC_KEY_MSG)
    from_server = recv_send_client.recv_by_size().decode()
    if from_server != DH_MSG:
        return False

    parameters = recv_send_client.recv_by_size()
    parameters_object =serialization.load_pem_parameters(parameters)

    b_private = parameters_object.generate_private_key()
    b_public =b_private.public_key()

    b_public_pem = b_public.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    recv_send_client.send_with_size(b_public_pem)

    a_rsa_public_key =recv_send_client.recv_by_size()
    signature_msg_public_key  = recv_send_client.recv_by_size()
    signature_msg = signature_msg_public_key[:256]
    a_public = signature_msg_public_key[256:]

    authentication = check_digital_signature(a_rsa_public_key,a_public,signature_msg)

    if not authentication:
        return False,None
    a_public_object =serialization.load_pem_public_key(a_public)

    shared_key = b_private.exchange(a_public_object)
    derived_key = HKDF(
        algorithm=hashes.SHA256(), length=32, salt=None, info=b"handshake data",
    ).derive(shared_key)

    return True,derived_key




def main():

    client_socket = socket.socket()
    client_socket.connect((SERVER_IP, SERVER_PORT))

    if page(client_socket):
        print("we connected")

    client_socket.close()




if __name__ == "__main__":
    main()