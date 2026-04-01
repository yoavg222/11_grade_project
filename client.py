import socket

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from class_tcp_by_size import recvSend
from constants import REG_MSG, LOG_MSG, FOR_MSG, RSA_PUBLIC_KEY_REQUEST, RSA, DPH, PRIVATE_MSG, PUBLIC_MSG,DELIMITER,SERVER_IP,SERVER_PORT,NUM_OF_CUPS
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
    if from_server != "RSA|OK":
        return False

    recv_send_client.send_with_size(RSA_PUBLIC_KEY_REQUEST)
    server_public_key = recv_send_client.recv_by_size()
    print(server_public_key)

    encrypted_aes_key = encrypted_rsa(server_public_key, key)
    recv_send_client.send_with_size(encrypted_aes_key)

    return True

def agree_on_aes_key(recv_send_client,key):
    global KEY_OK


    while not KEY_OK:
        radio_button = input("Diffie-hellman or RSA")
        if radio_button =="RSA" or radio_button == "rsa":
            success = rsa_key_exchange(key,recv_send_client)

            if success:
                return True
            return False

def sign_in_client(recv_send_client):
    global SIGN_IN
    global GOOD_MSG

    while not SIGN_IN:

        data = input("enter: register or login or forget password")
        while not GOOD_MSG:
            if data != "register" and data != "login" and data != "forget password":
                continue
            else:
                break

        if data == "register":
            user_name_password = input("enter: user_name,password,checkPassword,email")
            user_pass = user_name_password.split(" ")
            to_send = REG_MSG+DELIMITER+user_pass[0]+DELIMITER+user_pass[1]+DELIMITER+user_pass[2]+DELIMITER+user_pass[3]+DELIMITER+NUM_OF_CUPS
            print(to_send)

            recv_send_client.send_with_size(to_send)
            from_server = recv_send_client.recv_by_size()
            if "EML" in from_server.decode():
                print(from_server.split(DELIMITER.encode())[1].decode())
                code = input("enter the code:")
                recv_send_client.send_with_size(code.encode())
                from_server = recv_send_client.recv_by_size()

                if "OKR" in from_server.decode():
                    print("good registry")

        elif data == "login":
            user_name_password = input("enter: user_name,password")
            user_lst = user_name_password.split(" ")
            to_send = LOG_MSG+DELIMITER+user_lst[0]+DELIMITER+user_lst[1]
            recv_send_client.send_with_size(to_send)
            from_server = recv_send_client.recv_by_size().decode()
            print(from_server)
            if "good login" in from_server:
                user_name = from_server.split(" ")[2]
                user_password = from_server.split(" ")[3]
                break

def main():


    client_socket = socket.socket()
    client_socket.connect((SERVER_IP, SERVER_PORT))

    recv_send_client = recvSend(client_socket,None)
    key = create_aes_key()
    print(key.hex())
    if agree_on_aes_key(recv_send_client,key):
        print("agree on an aes key with the server")
    else:
        client_socket.close()

    recv_send_client = recvSend(client_socket,key)
    if sign_in_client(recv_send_client):
        print("we connected")



    client_socket.close()









if __name__ == "__main__":
    main()