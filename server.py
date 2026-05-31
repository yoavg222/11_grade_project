import pickle
import socket
import threading
import smtplib
import ssl
import time
from email.message import EmailMessage
import random

from roomGame import Room
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from hasherClass import SecureHasher
from class_tcp_by_size import recvSend
from users import Users
from rsaClass import RSA
from dhClass import DH
from serverThread import workerThread
from constants import SERVER_IP, SERVER_PORT, PICKLE_PATH, DELIMITER, ERROR_MSG_LOG_REG, REG_SUCCESSFUL, LOG_SUCCESSFUL, \
    FOR_PASSWORD, FOR_SUCCESSFUL, EMAIL_MESSAGE_SEND, RSA_MSG, DH_MSG, EMAIL_SENDER, EMAIL_PASSWORD, \
    REG_MSG, RSA_PUBLIC_KEY_MSG, RSA_FIRST, LOG_MSG, FOR_MSG, GOOD_EMAIL_CODE, HOME_BUTTON, DH_FIRST,DH_PUBLIC_KEY_MSG,GET_USER,JOIN_MSG,JON_MSG_OK,TUR,ATT,HIT,MIS


#global variables
all_to_die = False
game_start = False
players = []
num_players = 0
players_lock = threading.Lock()
game_lock = threading.Lock()
#from classes
users_SQL =Users()
rsa_session = RSA()


def game_logic(player1, player2):
    p1: recvSend = player1
    p2: recvSend = player2

    room = Room(p1, p2)
    num = room.who_first()

    if num == 1:
        first = p1
        second = p2
    else:
        first = p2
        second = p1

    first.send_with_size("FIR| chose 3 places")
    second.send_with_size("SEC| chose 3 places")

    first.set_timeout(60)
    second.set_timeout(60)

    try:
        place_first = first.recv_by_size().decode().split(DELIMITER)
        place_second = second.recv_by_size().decode().split(DELIMITER)

        first_places = room.add_place_to_lst(place_first)
        second_places = room.add_place_to_lst(place_second)
    except Exception as e:
        print(f"Error in game_logic: {e}")
        return

    p1_ships = first_places
    p2_ships = second_places

    current_player = first
    opponent = second


    boards = {id(first): p2_ships, id(second): p1_ships}

    current_player.send_with_size(TUR)

    while len(p1_ships) > 0 and len(p2_ships) > 0:
        data = current_player.recv_by_size().decode().split(DELIMITER)

        if data[0] == ATT:
            attack_pos = data[1]
            target_ships = boards[id(current_player)]

            if attack_pos in target_ships:
                target_ships.remove(attack_pos)
                msg_to_all = f"{HIT}{DELIMITER}{attack_pos}"
            else:
                msg_to_all = f"{MIS}{DELIMITER}{attack_pos}"

            current_player.send_with_size(msg_to_all)
            opponent.send_with_size(msg_to_all)


            if len(p1_ships) == 0 or len(p2_ships) == 0:
                break

            current_player, opponent = opponent, current_player
            current_player.send_with_size(TUR)

    if len(p1_ships) == 0:
        second.send_with_size("WIN")
        first.send_with_size("LOS")
    else:
        first.send_with_size("WIN")
        second.send_with_size("LOS")



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
    global players
    global num_players
    global game_start
    have_key = False
    connected = False
    want_exit = False

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
    users_SQL.add_user_by_socket_dict(recv_send_server,sock)

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

        data = recv_send_server.recv_by_size().decode()
        data_lst = data.split(DELIMITER)

        to_send = ""
        if data_lst[0] == JOIN_MSG:
            with players_lock:
                players.append(sock)
                num_players+=1
            while True:
                if len(players) == 2:
                    break
                time.sleep(1)
            to_send = JON_MSG_OK


        recv_send_server.send_with_size(to_send)
        game_lock.acquire()
        if not game_start:
            player1 = players[0]
            player2 = players[1]

            recv_send_p1 = users_SQL.find_by_socket(player1)
            recv_send_p2 = users_SQL.find_by_socket(player2)

            t = workerThread(game_logic,recv_send_p1,recv_send_p2)
            t.start()

        game_start = True
        game_lock.release()
        return










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