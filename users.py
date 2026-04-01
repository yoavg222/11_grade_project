__author__ = 'Yoav'
import threading
import hashlib
import time
import pickle

from pepper import pepper_users
from constants import PICKLE_PATH

class Users:
    def __init__(self):
        self.lock_users_dict = threading.Lock()
        self.lock_email_dict = threading.Lock()
        self.users_dict = {}
        self.EmailInProcess = {}
        self.cleanup_thread = threading.Thread(target=self.cleanup_emails, daemon=True)
        self.cleanup_thread.start()
        self.data_base_path = PICKLE_PATH


    def cleanup_emails(self):
        while True:
            time.sleep(300)

            current_time = time.time()
            self.lock_email_dict.acquire()
            try:
                to_delete = [email for email,data in self.EmailInProcess.items() if current_time - data["code"][1]>300]

                for email in to_delete:
                    del self.EmailInProcess[email]


            finally:
                self.lock_email_dict.release()



    def SaveUser(self,name,password,salt,email,cups):
        self.lock_users_dict.acquire()
        try:
            with open(self.data_base_path,"rb") as file:
                self.users_dict = pickle.load(file)
        except Exception as e:
            print("first user")
        finally:
            self.users_dict[name] = {"password":password,"salt":salt,"email":email,"cups":cups}
        with open(self.data_base_path,"wb") as file:
            pickle.dump(self.users_dict,file)
        self.lock_users_dict.release()



    def SaveEmail(self,email,code):
        self.lock_email_dict.acquire()
        self.EmailInProcess[email] = {"code":[code,time.time()]}

        self.lock_email_dict.release()


    def IsPasswordOK(self,name,password):
        self.lock_users_dict.acquire()
        try:
            if (self.users_dict[name]["password"]) == hashlib.sha256((self.users_dict[name]["salt"] + password + pepper_users).encode()).hexdigest():
                self.lock_users_dict.release()
                return True
            self.lock_users_dict.release()
            return False
        except Exception as err:
            self.lock_users_dict.release()
            return False


    def IsUserExist(self,name):
        self.lock_users_dict.acquire()
        try:
            name = self.users_dict[name]
            self.lock_users_dict.release()
            return True

        except Exception as e:
            self.lock_users_dict.release()
            return False


    def IsEmailInProcess(self,email):
        self.lock_email_dict.acquire()
        try:
            email = self.EmailInProcess[email]
            self.lock_email_dict.release()
            return True


        except Exception as e:
            self.lock_email_dict.release()
            return False


