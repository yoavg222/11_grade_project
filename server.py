import pickle
import socket
import threading
import smtplib
import ssl
from email.message import EmailMessage
import random

from hasherClass import SecureHasher
from class_tcp_by_size import recvSend
from users import Users
from rsaClass import RSA
from constants import SERVER_IP, SERVER_PORT, PICKLE_PATH, DELIMITER, ERROR_MSG_LOG_REG,REG_SUCCESSFUL,LOG_SUCCESSFUL,FOR_PASSWORD,FOR_SUCCESSFUL,EMAIL_MESSAGE_SEND,KEY_SUCCESSFUL,RSA_MSG,DHP_MSG,EMAIL_SENDER,EMAIL_PASSWORD,REG_MSG,RSA_PUBLIC_KEY_MSG,RSA_FIRST,LOG_MSG


#global variables
all_to_die = False
have_key = False
connected = False
want_exit = False

#from classes
users_SQL =Users()

def rsa_key_exchange(recv_send_server):
    data = recv_send_server.recv_by_size().decode()
    if data == RSA_PUBLIC_KEY_MSG:
        rsa_session = RSA()
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


    while not want_exit:
        pass


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



    # try:
    #     with open(PICKLE_PATH, "wb") as file:
    #         pickle.dump(users_SQL.users_dict, file)
    # except Exception as e:
    #     print(f"Error in pickle: {e}")
    # finally:
    server_socket.close()
    print("bye")









if __name__ == "__main__":
    main()