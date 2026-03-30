__author__ = 'Yoav'
import threading
import hashlib
from pepper import pepper_users
import time

class Users:
    def __init__(self):
        self.lock_users_dict = threading.Lock()
        self.lock_email_dict = threading.Lock()
        self.users_dict = {}
        self.EmailInProcess = {}
        self.cleanup_thread = threading.Thread(target=self.cleanup_emails, daemon=True)
        self.cleanup_thread.start()

    def hash_password(self,password,salt):
        pass

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



    def SaveUser(self,name,password,salt,email):
        self.lock_users_dict.acquire()
        self.users_dict[name] = {"password":password,"salt":salt,"email":email}
        self.lock_users_dict.release()



    def SaveEmail(self,email,code):
        self.lock_email_dict.acquire()
        self.EmailInProcess[email] = {"code":[code,time.time()]}

        self.lock_email_dict.release()


    def IsPasswordOK(self,name,password):
        self.lock_users_dict.acquire()
        try:
            if self.users_dict[name]["password"] == (hashlib.sha256((self.users_dict[name]["salt"]+password+pepper_users).encode())).hexdigest():
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


