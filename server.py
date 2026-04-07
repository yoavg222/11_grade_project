import pickle
import socket
import threading
import smtplib
import ssl
from email.message import EmailMessage
import random
import hashlib
from typing import final

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from hasherClass import SecureHasher
from class_tcp_by_size import recvSend
from users import Users
from rsaClass import RSA
from dhClass import DH
from constants import SERVER_IP, SERVER_PORT, PICKLE_PATH, DELIMITER, ERROR_MSG_LOG_REG, REG_SUCCESSFUL, LOG_SUCCESSFUL, \
    FOR_PASSWORD, FOR_SUCCESSFUL, EMAIL_MESSAGE_SEND, KEY_SUCCESSFUL, RSA_MSG, DH_MSG, EMAIL_SENDER, EMAIL_PASSWORD, \
    REG_MSG, RSA_PUBLIC_KEY_MSG, RSA_FIRST, LOG_MSG, FOR_MSG, GOOD_EMAIL_CODE, HOME_BUTTON, DH_FIRST,DH_PUBLIC_KEY_MSG,DELIMITER2,GET_USER


#global variables
all_to_die = False
have_key = False
connected = False
want_exit = False

#from classes
users_SQL =Users()
rsa_session = RSA()

def encrypt_with_rsa_digital_signature(rsa_private_key,signature):
    final_signature = rsa_private_key.sign(
        signature,padding.PSS(
            mgf = padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return final_signature



def digital_signature(public_key_dh):
    rsa_private_key = rsa_session.private_key
    rsa_public_key = rsa_session.public_key
    signature = encrypt_with_rsa_digital_signature(rsa_private_key,public_key_dh)

    return signature,rsa_public_key


def dh_key_exchange(recv_send_server):
    data = recv_send_server.recv_by_size().decode()
    if data == DH_PUBLIC_KEY_MSG:
        dh_session = DH()

        to_send_parameters = dh_session.ready_to_send()
        recv_send_server.send_with_size(to_send_parameters)

        client_public_key = recv_send_server.recv_by_size()
        public_key = dh_session.create_keys()
        public_key_digital_signature,rsa_public_key = digital_signature(public_key)

        pem_public = rsa_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format = serialization.PublicFormat.SubjectPublicKeyInfo
        )
        print(len(public_key_digital_signature))
        recv_send_server.send_with_size(pem_public)
        to_send = public_key_digital_signature+public_key
        print(to_send)
        recv_send_server.send_with_size(to_send)

        print(public_key_digital_signature)

        shared_key = dh_session.create_shared_key(client_public_key)

        print(shared_key)
        return shared_key





def rsa_key_exchange(recv_send_server):
    data = recv_send_server.recv_by_size().decode()
    if data == RSA_PUBLIC_KEY_MSG:
        recv_send_server.send_with_size(rsa_session.public_key_to_send())

        encrypted_rsa_key = recv_send_server.recv_by_size()
        aes_key = rsa_session.decrypt_message_rsa(encrypted_rsa_key)

        return aes_key

    else:
        recv_send_server.send_with_size(ERROR_MSG_LOG_REG)


def send_email(email_receiver):


    em = EmailMessage()
    em["From"] = EMAIL_SENDER
    em["To"] = email_receiver
    em["Subject"] = "Enter a code"
    email_body = random.randint(1000,9999)
    code = email_body

    users_SQL.SaveEmail(email_receiver,code)

    em.set_content(str(email_body))
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context)as smtp:
            smtp.login(EMAIL_SENDER,EMAIL_PASSWORD)
            smtp.send_message(em)
            return True,code

    except Exception as e:
        print(f"error in the send email: {e}")
        return False

def handle_client(sock,addr,i):

    global all_to_die
    global have_key
    global connected
    global want_exit

    hasher = SecureHasher()
    print(f"client {addr} connected")
    recv_send_server = recvSend(sock,None)
    key = b""
    while not have_key:

        data = recv_send_server.recv_by_size()
        key_exchange = data.decode()

        if key_exchange == RSA_FIRST:
            recv_send_server.send_with_size(RSA_MSG)
            key_aes = rsa_key_exchange(recv_send_server)
            key = key_aes
            print(key_aes.hex())
            have_key = True


        if key_exchange == DH_FIRST:
            recv_send_server.send_with_size(DH_MSG)
            key_aes = dh_key_exchange(recv_send_server)
            key = key_aes
            have_key = True


    recv_send_server = recvSend(sock,key)


    while not connected:
        if all_to_die:
            break

        data = recv_send_server.recv_by_size().decode()
        print(data)

        if data == "":
            print(f"client number{i} disconnected")
            want_exit = True
            break
        data = data.split(DELIMITER)
        if data[0] == REG_MSG:
            recv_send_server.send_with_size(EMAIL_MESSAGE_SEND)
            email_send,code = send_email(data[4])
            if email_send:
                client_code = recv_send_server.recv_by_size().decode()
                print(client_code)
                if users_SQL.IsUserExist(data[1]):
                    recv_send_server.send_with_size(ERROR_MSG_LOG_REG)
                    break
                if int(client_code) == code and data[2] == data[3]:
                    recv_send_server.send_with_size(REG_SUCCESSFUL)
                    hash_password,salt = hasher.hash_salt_pepper_password(data[2])
                    users_SQL.SaveUser(data[1],hash_password,salt,data[4],0)

            else:
                recv_send_server.send_with_size(ERROR_MSG_LOG_REG)

        elif data[0] == LOG_MSG:
            print(type(users_SQL))

            if users_SQL.IsUserExist(data[1]) and users_SQL.IsPasswordOK(data[1], data[2]):
                recv_send_server.send_with_size(LOG_SUCCESSFUL + " " + data[1] + " " + data[2])
                break
            else:
                recv_send_server.send_with_size(ERROR_MSG_LOG_REG)



        elif data[0] == FOR_MSG:
            email = data[1]
            user = users_SQL.user_by_email(email)
            if user is None:
                recv_send_server.send_with_size(ERROR_MSG_LOG_REG)
                continue

            send,code = send_email(email)
            if send:
                recv_send_server.send_with_size(EMAIL_MESSAGE_SEND)

            code_from_client = recv_send_server.recv_by_size().decode()

            if int(code_from_client) != code:
                recv_send_server.send_with_size(EMAIL_MESSAGE_SEND)
                continue

            recv_send_server.send_with_size(GOOD_EMAIL_CODE)
            recv_send_server.send_with_size(FOR_PASSWORD)

            from_client = recv_send_server.recv_by_size().decode()
            if from_client == HOME_BUTTON:
                continue

            from_client_lst = from_client.split(DELIMITER)
            if from_client_lst[0] == FOR_MSG:
                user_new_password = from_client_lst[1]
                user_new_password_confirm = from_client_lst[2]

                if user_new_password != user_new_password_confirm:
                    recv_send_server.send_with_size(ERROR_MSG_LOG_REG)
                    continue

                new_password,new_salt = hasher.hash_salt_pepper_password(user_new_password)
                users_SQL.SaveUser(user,new_password,new_salt,users_SQL.users_dict[user]["email"],users_SQL.users_dict[user]["cups"])
                recv_send_server.send_with_size(FOR_SUCCESSFUL)
                continue

            else:
                recv_send_server.send_with_size(ERROR_MSG_LOG_REG)
                continue




    while not want_exit:
        print("connected")
        data = recv_send_server.recv_by_size().decode()
        data_lst = data.split(DELIMITER)
        if data_lst[0] == GET_USER:
            user = users_SQL.find_user(data_lst[1])
            to_send = f"{GET_USER}{DELIMITER}{user["cups"]}"
            recv_send_server.send_with_size(to_send)
        break


    sock.close()



def main():
    global users_SQL
    global all_to_die

    server_socket = socket.socket()
    server_socket.bind((SERVER_IP,SERVER_PORT))
    server_socket.listen(2)

    try:
        with open(PICKLE_PATH,"rb") as file:
            users = pickle.load(file)

            for k,v in users.items():
                users_SQL.SaveUser(k,users[k]["password"],users[k]["salt"],users[k]["email"],users[k]["cups"])

    except Exception as e:
        print(f"Error to find Users_DataBase.pkl{e}")
        users_SQL =Users()
        print(users_SQL)




    threads = []
    i = 1

    while True:
        print("wait...")
        c,a = server_socket.accept()
        t = threading.Thread(target = handle_client,args = (c,a,i))
        t.start()

        threads.append(t)
        i+=1

        if i>1000:
            break

    all_to_die = True
    for t in threads:
        t.join()



    server_socket.close()
    print("bye")






if __name__ == "__main__":
    main()