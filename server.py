import pickle
import socket
import threading

from class_tcp_by_size import recvSend
from users import Users
from rsaClass import RSA


# const
SERVER_IP = "192.168.1.119"
SERVER_PORT = 12342
PICKLE_PATH = "C:\\School_11_Grade\\DataBase\\Users_DataBase.pkl"

ERROR_MSG_LOG_REG = "ERR|error try again"
REG_SUCCESSFUL = "OKR|good register"
LOG_SUCCESSFUL = "OKL|good login"
FOR_PASSWORD = "FOR|enter new password"
FOR_SUCCESSFUL = "FOR|good change password"
EmailMessage_SEND = "EML| we send a code to your email enter him"
email_sender = "assafgruengard@gmail.com"
email_password = "gkybysjdxnbjvowc"
KEY_SUCCESSFUL = "KEY|we have a key"
RSA_MSG = "RSA|OK"
DHP_MSG = "DPH|OK"

#global variables
all_to_die = False
have_key = False
connected = False
want_exit = False

#from classes
users_SQL =Users()

def rsa_key_exchange(recv_send_server):
    data = recv_send_server.recv_by_size().decode()
    if data == "RSA|send me your public key":
        rsa_session = RSA()
        recv_send_server.send_with_size(rsa_session.public_key_to_send())

        encrypted_rsa_key = recv_send_server.recv_by_size()
        aes_key = rsa_session.decrypt_message_rsa(encrypted_rsa_key)

        return aes_key

    else:
        recv_send_server.send_with_size(ERROR_MSG_LOG_REG)


def handle_client(sock,addr,i):

    global all_to_die
    global have_key
    global connected

    recv_send_server = recvSend(sock,None)
    key = b""
    while not have_key:

        data = recv_send_server.recv_by_size()
        key_exchange = data.decode()

        if key_exchange == "RSA":
            recv_send_server.send_with_size(RSA_MSG)
            key_aes = rsa_key_exchange(recv_send_server)
            print(key_aes.hex())
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
            users_SQL = pickle.load(file)

    except Exception as e:
        print(f"Error to find Users_DataBase.pkl{e}")
        users_SQL = {}





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



    try:
        with open(PICKLE_PATH, "wb") as file:
            pickle.dump(users_SQL.users_dict, file)
    except Exception as e:
        print(f"Error in pickle: {e}")
    finally:
        server_socket.close()
        print("bye")









if __name__ == "__main__":
    main()