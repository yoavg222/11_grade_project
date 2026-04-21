from tkinter import *
from PIL import ImageTk, Image

from class_tcp_by_size import recvSend
from constants import user_name, LOG_MSG, DELIMITER, REG_MSG, NUM_OF_CUPS,GOOD_EMAIL_CODE,FOR_MSG,FOR_SUCCESSFUL,FOR_PASSWORD,GET_USER,RSA




class LoginForm:
    def __init__(self, window,network_client):
        # build the window
        self.window = window
        self.window.geometry("1166x718")
        self.window.state("zoomed")
        self.window.resizable(0, 0)
        self.network = recvSend(network_client,None)
        self.client_socket = network_client



        # background image
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()

        self.bg_frame = Image.open("C:\\Users\\user\\Downloads\\img6.png")
        self.bg_frame = self.bg_frame.resize((width, height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(self.bg_frame)

        self.bg_panel = Label(self.window, image=photo, bd=0)
        self.bg_panel.image = photo
        self.bg_panel.place(x=0, y=0, relwidth=1, relheight=1)


        #login frame
        self.lgn_frame = Frame(self.window,bg = "white",width = "950",height=600)
        self.lgn_frame.place(x = 200,y = 70)

        self.txt = "WELCOME"
        self.heading = Label(self.lgn_frame,text = self.txt,font = ("yu gothic ui",25,"bold"),bg = "white",fg = "black")
        self.heading.place(x = 80,y = 30,width = 300,height = 30)

        #left side image
        self.side_image = Image.open("C:\\Users\\user\\Downloads\\img4.png")
        resized_image = self.side_image.resize((250, 470))
        photo = ImageTk.PhotoImage(resized_image)
        self.side_image_label = Label(self.lgn_frame, image=photo,bg="white",borderwidth=0,highlightthickness=0)
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)


        #sign in img
        self.sign_in_image = Image.open("C:\\Users\\user\\Downloads\\img5.png")
        resized_image = self.sign_in_image.resize((80, 80))
        photo = ImageTk.PhotoImage(resized_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg="black")
        self.side_image_label.image = photo
        self.side_image_label.place(x=700, y=100)

        self.sign_in_label = Label(self.lgn_frame,text = "Sign In",bg = "white",font = ("yu gothic ui",13,"bold"),fg = "black")
        self.sign_in_label.place(x = 715,y = 190)

        #username
        self.username_label = Label(self.lgn_frame,text = "Username",bg = "white",font = ("yu gothic ui",13,"bold"),fg = "black")
        self.username_label.place(x = 550,y = 250)

        self.username_entry = Entry(self.lgn_frame,highlightthickness=0,relief=FLAT,bg ="white",fg = "black",font = ("yu gothic ui",12,"bold"))
        self.username_entry.place(x = 625,y = 285,width = 270)
        self.username_line = Canvas(self.lgn_frame,width = 300,height=2.0,bg = "black",highlightthickness=0)
        self.username_line.place(x = 550,y = 309)


        #username icon
        self.username_icon = Image.open("C:\\Users\\user\\Downloads\\img7.png")
        resized_image = self.username_icon.resize((25, 25))
        photo = ImageTk.PhotoImage(resized_image)
        self.username_icon = Label(self.lgn_frame, image=photo,bg = "black")
        self.username_icon.image = photo
        self.username_icon.place(x=550, y=278)



        #password
        self.password_label = Label(self.lgn_frame,text = "Password",bg = "white",font = ("yu gothic ui",13,"bold"),fg = "black")
        self.password_label.place(x = 550,y = 330)

        self.password_entry = Entry(self.lgn_frame,highlightthickness=0,relief=FLAT,bg ="white",fg = "black",font = ("yu gothic ui",12,"bold"),show = "*")
        self.password_entry.place(x = 625,y = 365,width = 270)
        self.password_line = Canvas(self.lgn_frame,width = 300,height=2.0,bg = "black",highlightthickness=0)
        self.password_line.place(x = 550,y = 390)


        #password icon
        self.password_icon = Image.open("C:\\Users\\user\\Downloads\\img8.png")
        resized_image = self.password_icon.resize((25, 25))
        photo = ImageTk.PhotoImage(resized_image)
        self.password_icon = Label(self.lgn_frame, image=photo,bg = "black")
        self.password_icon.image = photo
        self.password_icon.place(x=550, y=360)


        #login button
        self.lgn_btn_img = Image.open("C:\\Users\\user\\Downloads\\img10.png")
        resized_btn = self.lgn_btn_img.resize((250, 60))
        self.btn_photo = ImageTk.PhotoImage(resized_btn)

        self.login_btn = Button(self.lgn_frame, image=self.btn_photo, text="LOGIN", font=("yu gothic ui", 13, "bold"),
                                compound="center", fg="white", bd=0, bg="white", activebackground="white",
                                cursor="hand2")
        self.login_btn.image = self.btn_photo
        self.login_btn.place(x=550, y=450)

        self.login_btn.config(command=self.handle_login)

        #forgot password
        self.forgot_button = Button(self.lgn_frame,text = "Forgot Password ?",font=("yu gothic ui", 13, "bold underline"),fg = "black",width = 25,bd = 0,bg = "white",activebackground="white",cursor = "hand2",command=self.forget_password_handle)
        self.forgot_button.place(x = 550,y =510 )

        #sign Up
        self.sign_label = Label(self.lgn_frame,text = "No account yet?",font=("yu gothic ui", 11, "bold"),background="white",fg = "black")
        self.sign_label.place(x = 550,y = 560)

        self.signup_button = Image.open("C:\\Users\\user\\Downloads\\img12.png")
        resized_btn = self.signup_button.resize((85, 60))
        photo = ImageTk.PhotoImage(resized_btn)
        self.signup_button_label = Button(self.lgn_frame,image=photo,bg = "white",activebackground="white",cursor="hand2",bd = 0)
        self.signup_button_label.image = photo
        self.signup_button_label.place(x = 670,y = 555,width = 111,height = 35)

        self.signup_button_label.config(command = self.clear_screen)

        #show/hide password
        self.show_image = Image.open("C:\\Users\\user\\Downloads\\img13.png")
        resized_btn = self.show_image.resize((30, 30))
        self.photo_show = ImageTk.PhotoImage(resized_btn)
        self.show_button = Button(self.lgn_frame, image=self.photo_show, bg="black", activebackground="black",
                                          cursor="hand2", bd=0,highlightthickness=0,command=self.show)
        self.show_button.image = self.photo_show
        self.show_button.place(x=860,y=350)

        self.hide_image = Image.open("C:\\Users\\user\\Downloads\\img14.png")
        resized_btn = self.hide_image.resize((30, 30))
        self.photo_hide = ImageTk.PhotoImage(resized_btn)


        #radio button
        self.var_key = StringVar()
        radio1 = Radiobutton(self.window,text ="RSA",variable = self.var_key,value = "RSA")
        radio1.pack(pady = (300,5))

        radio2= Radiobutton(self.window, text="Diffie-Hellman", variable=self.var_key, value="Diffie-Hellman")
        radio2.pack(pady=(5, 10))

    def show(self):
        self.hide_button = Button(self.lgn_frame, image=self.photo_show, bg="black", activebackground="black",
                                    cursor="hand2", bd=0, highlightthickness=0,command=self.hide)
        self.hide_button.image = self.photo_show
        self.hide_button.place(x=860, y=350)
        self.password_entry.config(show = "")

    def hide(self):
        self.show_button = Button(self.lgn_frame, image=self.photo_hide, bg="black", activebackground="black",
                                  cursor="hand2", bd=0, highlightthickness=0, command=self.show)
        self.show_button.image = self.photo_hide
        self.show_button.place(x=860, y=350)

        self.password_entry.config(show="*")


    def handle_login(self):
        from client import rsa_key_exchange, create_aes_key,df_key_exchange
        username = self.username_entry.get()
        password = self.password_entry.get()
        key_exchange = self.var_key.get()
        if not username or not password or not key_exchange:
            print("Enter username and password and select key exchange ")
            return

        if key_exchange == RSA:
            key = create_aes_key()
            success,key = rsa_key_exchange(key,self.network)

            if success:
                self.network = recvSend(self.client_socket,key)
            else:
                print("Error")
                return

        if key_exchange == "Diffie-Hellman":
            success, key_df = df_key_exchange(self.network)
            if success:
                self.network = recvSend(self.client_socket,key_df)
            else:
                print("Error")
                return


        to_send = f"{LOG_MSG}{DELIMITER}{username}{DELIMITER}{password}"

        try:
            self.network.send_with_size(to_send.encode())
            response = self.network.recv_by_size().decode()
            print(f"Server says: {response}")

            if "good login" in response:
                print("Successful Login")
                self.opening_page(username)

            else:
                print("Login failed")

        except Exception as e:
            print(f"Error communicating with server: {e}")


    def clear_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.open_register_screen()


    def open_register_screen(self):

        self.reg_frame = Frame(self.window, bg="white", width=950, height=600)
        self.reg_frame.place(x=200, y=70)

        # password
        self.reg_pass_label = Label(self.reg_frame, text="Password", bg="white",
                                    font=("yu gothic ui", 13, "bold"), fg="black")
        self.reg_pass_label.place(x=550, y=330)
        self.reg_pass_entry = Entry(self.reg_frame, highlightthickness=0, relief=FLAT,
                                    bg="white", fg="black", font=("yu gothic ui", 12, "bold"), show="*")
        self.reg_pass_entry.place(x=625, y=365, width=270)
        self.reg_pass_line = Canvas(self.reg_frame, width=300, height=2.0, bg="black", highlightthickness=0)
        self.reg_pass_line.place(x=550, y=390)

        # password icon
        img_path = "C:\\Users\\user\\Downloads\\img8.png"
        raw_img = Image.open(img_path)
        resized_img = raw_img.resize((25, 25))
        photo_icon_pass = ImageTk.PhotoImage(resized_img)

        self.reg_pass_icon_label = Label(self.reg_frame, image=photo_icon_pass, bg="black")
        self.reg_pass_icon_label.image = photo_icon_pass
        self.reg_pass_icon_label.place(x=550, y=360)

        # confirm password

        self.confirm_password_label = Label(self.reg_frame, text="Confirm Password", bg="white",
                                            font=("yu gothic ui", 13, "bold"), fg="black")
        self.confirm_password_label.place(x=550, y=410)
        self.confirm_password_entry = Entry(self.reg_frame, highlightthickness=0, relief=FLAT,
                                            bg="white", fg="black", font=("yu gothic ui", 12, "bold"), show="*")
        self.confirm_password_entry.place(x=625, y=445, width=270)
        self.confirm_password_line = Canvas(self.reg_frame, width=300, height=2.0, bg="black", highlightthickness=0)
        self.confirm_password_line.place(x=550, y=470)

        # confirm password icon
        img_path = "C:\\Users\\user\\Downloads\\img8.png"
        raw_img = Image.open(img_path)
        resized_img = raw_img.resize((25, 25))
        photo_icon_conf = ImageTk.PhotoImage(resized_img)

        self.reg_conf_icon_label = Label(self.reg_frame, image=photo_icon_conf, bg="black")
        self.reg_conf_icon_label.image = photo_icon_conf
        self.reg_conf_icon_label.place(x=550, y=440)

        # username
        self.reg_user_label = Label(self.reg_frame, text="Username", bg="white",
                                    font=("yu gothic ui", 13, "bold"), fg="black")
        self.reg_user_label.place(x=550, y=250)
        self.reg_user_entry = Entry(self.reg_frame, highlightthickness=0, relief=FLAT,
                                    bg="white", fg="black", font=("yu gothic ui", 12, "bold"))
        self.reg_user_entry.place(x=625, y=285, width=270)
        self.reg_user_line = Canvas(self.reg_frame, width=300, height=2.0, bg="black", highlightthickness=0)
        self.reg_user_line.place(x=550, y=310)

        # username icon
        self.username_icon_reg_img = Image.open("C:\\Users\\user\\Downloads\\img7.png")
        resized_image_user = self.username_icon_reg_img.resize((25, 25))
        photo_user = ImageTk.PhotoImage(resized_image_user)
        self.username_icon_reg_label = Label(self.reg_frame, image=photo_user, bg="black")
        self.username_icon_reg_label.image = photo_user
        self.username_icon_reg_label.place(x=550, y=278)

        # emil
        self.reg_email_label = Label(self.reg_frame, text="Email", bg="white",
                                     font=("yu gothic ui", 13, "bold"), fg="black")
        self.reg_email_label.place(x=550, y=170)
        self.reg_email_entry = Entry(self.reg_frame, highlightthickness=0, relief=FLAT,
                                     bg="white", fg="black", font=("yu gothic ui", 12, "bold"))
        self.reg_email_entry.place(x=625, y=205, width=270)
        self.reg_email_line = Canvas(self.reg_frame, width=300, height=2.0, bg="black", highlightthickness=0)
        self.reg_email_line.place(x=550, y=230)

        # email icon
        self.email_icon_reg_img = Image.open("C:\\Users\\user\\Downloads\\img16.png")
        resized_image_email = self.email_icon_reg_img.resize((25, 25))
        photo_email = ImageTk.PhotoImage(resized_image_email)

        self.email_icon_label = Label(self.reg_frame, image=photo_email, bg="white")
        self.email_icon_label.image = photo_email
        self.email_icon_label.place(x=550, y=200)

        # left side image
        self.side_image = Image.open("C:\\Users\\user\\Downloads\\img4.png")
        resized_image_side = self.side_image.resize((250, 470))
        photo_side = ImageTk.PhotoImage(resized_image_side)
        self.side_image_label = Label(self.reg_frame, image=photo_side, bg="white", borderwidth=0, highlightthickness=0)
        self.side_image_label.image = photo_side
        self.side_image_label.place(x=5, y=100)

        # reg frame
        self.txt = "WELCOME"
        self.heading = Label(self.reg_frame, text=self.txt, font=("yu gothic ui", 25, "bold"), bg="white", fg="black")
        self.heading.place(x=80, y=30, width=300, height=30)

        # sign in img
        self.sign_in_image_reg = Image.open("C:\\Users\\user\\Downloads\\img5.png")
        resized_image_sign = self.sign_in_image_reg.resize((80, 80))
        photo_sign = ImageTk.PhotoImage(resized_image_sign)
        self.sign_in_icon_label = Label(self.reg_frame, image=photo_sign, bg="black")
        self.sign_in_icon_label.image = photo_sign
        self.sign_in_icon_label.place(x=700, y=80)

        self.sign_in_label = Label(self.reg_frame, text="Sign Up", bg="white", font=("yu gothic ui", 13, "bold"),
                                   fg="black")
        self.sign_in_label.place(x=715, y=170)

        # register button
        self.reg_btn_img = Image.open("C:\\Users\\user\\Downloads\\img17.png")
        resized_btn_reg = self.reg_btn_img.resize((200, 60))
        self.reg_btn_photo = ImageTk.PhotoImage(resized_btn_reg)

        self.register_btn = Button(self.reg_frame, image=self.reg_btn_photo, text="", font=("yu gothic ui", 13, "bold"),
                                   compound="center", fg="white", bd=0, bg="white", activebackground="white",
                                   cursor="hand2")
        self.register_btn.image = self.reg_btn_photo
        self.register_btn.place(x=550, y=500)

        self.register_btn.config(command=self.handle_register)

        # back button
        self.back_btn_img = Image.open("C:\\Users\\user\\Downloads\\img19.png")
        resized_btn_back = self.back_btn_img.resize((80, 80))
        self.back_btn_photo = ImageTk.PhotoImage(resized_btn_back)

        self.back_button_widget = Button(self.reg_frame, image=self.back_btn_photo, text="",
                                         font=("yu gothic ui", 13, "bold"),
                                         compound="center", fg="white", bd=0, bg="white", activebackground="white",
                                         cursor="hand2")
        self.back_button_widget.image = self.back_btn_photo
        self.back_button_widget.place(x=800, y=490)

        self.back_button_widget.config(command=self.return_to_login)



    def handle_register(self):

        username = self.reg_user_entry.get()
        password = self.reg_pass_entry.get()
        email = self.reg_email_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not username or not password or not email or not confirm_password:
            print("Enter username and password")
            return

        to_send = f"{REG_MSG}{DELIMITER}{username}{DELIMITER}{password}{DELIMITER}{confirm_password}{DELIMITER}{email}{DELIMITER}{NUM_OF_CUPS}"
        try:
            self.network.send_with_size(to_send.encode())
            response = self.network.recv_by_size().decode()
            print(f"Server saya:{response}")

            if "EML" in response:
                self.email_code_page("register")


        except Exception as e:
            print(f"Error communicating with server: {e}")



    def return_to_login(self):
        self.clear_screen()
        self.__init__(self.window, self.network)


    def email_code_page(self,type_of_request):
        self.clear_screen()
        self.code_frame = Frame(self.window, bg="white", width=950, height=600)
        self.code_frame.place(x=200, y=70)

        code_btn_img = Image.open("C:\\Users\\user\\Downloads\\img10.png")
        resized_code_btn = code_btn_img.resize((250, 60))
        self.code_btn_photo = ImageTk.PhotoImage(resized_code_btn)

        Label(self.code_frame, text="ENTER CODE", font=("yu gothic ui", 25, "bold"), bg="white", fg="black").place(x=80,y=30)
        Label(self.code_frame, text="Verification Code", bg="white", font=("yu gothic ui", 13, "bold"),
              fg="black").place(x=550, y=170)

        self.code_entry = Entry(self.code_frame, highlightthickness=0, relief=FLAT, bg="white", fg="black",
                                font=("yu gothic ui", 12, "bold"))
        self.code_entry.place(x=550, y=205, width=300)

        Canvas(self.code_frame, width=300, height=2.0, bg="black", highlightthickness=0).place(x=550, y=230)



        self.send_code_btn = Button(self.code_frame, image=self.code_btn_photo, text="SEND",
                                    font=("yu gothic ui", 13, "bold"), compound="center", fg="white", bd=0, bg="white",
                                    activebackground="white", cursor="hand2", command=lambda:self.submit_code(type_of_request))
        self.send_code_btn.image = self.code_btn_photo
        self.send_code_btn.place(x=550, y=300)



        # back button
        self.back_btn_img = Image.open("C:\\Users\\user\\Downloads\\img19.png")
        resized_btn_back = self.back_btn_img.resize((80, 80))
        self.back_btn_photo = ImageTk.PhotoImage(resized_btn_back)

        self.back_button_widget = Button(self.code_frame, image=self.back_btn_photo, text="",
                                         font=("yu gothic ui", 13, "bold"),
                                         compound="center", fg="white", bd=0, bg="white", activebackground="white",
                                         cursor="hand2")
        self.back_button_widget.image = self.back_btn_photo
        self.back_button_widget.place(x=800, y=490)

        self.back_button_widget.config(command=self.return_to_login)


    def submit_code(self,type_of_request):
        code = self.code_entry.get()
        self.network.send_with_size(code.encode())

        response = self.network.recv_by_size().decode()
        if type_of_request == "register":
            if "OKR" in response:
                print("good registry")
                self.return_to_login()
        else:
            if response == GOOD_EMAIL_CODE:
                response = self.network.recv_by_size().decode()
                if response == FOR_PASSWORD:
                    self.forget_password_page()



    def forget_password_page(self):

        # forget password page
        self.clear_screen()
        self.forget_password_frame = Frame(self.window, bg="white", width=950, height=600)
        self.forget_password_frame.place(x=200, y=70)

        code_btn_img = Image.open("C:\\Users\\user\\Downloads\\img10.png")
        resized_code_btn = code_btn_img.resize((250, 60))
        self.code_btn_photo = ImageTk.PhotoImage(resized_code_btn)

        Label(self.forget_password_frame, text="ENTER NEW PASSWORD", font=("yu gothic ui", 25, "bold"), bg="white",
              fg="black").place(x=80,
                                y=30)
        Label(self.forget_password_frame, text="Password", bg="white", font=("yu gothic ui", 13, "bold"),
              fg="black").place(x=550, y=170)

        self.new_password_entry = Entry(self.forget_password_frame, highlightthickness=0, relief=FLAT, bg="white",
                                        fg="black",
                                        font=("yu gothic ui", 12, "bold"))
        self.new_password_entry.place(x=550, y=205, width=300)

        Canvas(self.forget_password_frame, width=300, height=2.0, bg="black", highlightthickness=0).place(x=550, y=230)

        Label(self.forget_password_frame, text="Confirm Password", bg="white", font=("yu gothic ui", 13, "bold"),
              fg="black").place(x=550, y=270)

        self.confirm_password_entry = Entry(self.forget_password_frame, highlightthickness=0, relief=FLAT, bg="white",
                                            fg="black",
                                            font=("yu gothic ui", 12, "bold"))
        self.confirm_password_entry.place(x=550, y=305, width=300)

        Canvas(self.forget_password_frame, width=300, height=2.0, bg="black", highlightthickness=0).place(x=550, y=330)

        self.change_password_button = Button(self.forget_password_frame, image=self.code_btn_photo, text="CHANGE",
                                             font=("yu gothic ui", 13, "bold"), compound="center", fg="white", bd=0,
                                             bg="white",
                                             activebackground="white", cursor="hand2",
                                             command=self.change_password)
        self.change_password_button.image = self.code_btn_photo
        self.change_password_button.place(x=550, y=490)

        # back button
        self.back_btn_img = Image.open("C:\\Users\\user\\Downloads\\img19.png")
        resized_btn_back = self.back_btn_img.resize((80, 80))
        self.back_btn_photo = ImageTk.PhotoImage(resized_btn_back)

        self.back_button_widget = Button(self.forget_password_frame, image=self.back_btn_photo, text="",
                                         font=("yu gothic ui", 13, "bold"),
                                         compound="center", fg="white", bd=0, bg="white", activebackground="white",
                                         cursor="hand2")
        self.back_button_widget.image = self.back_btn_photo
        self.back_button_widget.place(x=800, y=490)

        self.back_button_widget.config(command=self.return_to_login)




    def forget_password_handle(self):
        self.clear_screen()

        self.forget_frame = Frame(self.window, bg="white", width=950, height=600)
        self.forget_frame.place(x=200, y=70)

        Label(self.forget_frame, text="FORGOT PASSWORD", font=("yu gothic ui", 25, "bold"),
              bg="white", fg="black").place(x=80, y=30)

        Label(self.forget_frame, text="Enter Your Email", bg="white", font=("yu gothic ui", 13, "bold"),
              fg="black").place(x=550, y=170)

        self.user_email_entry = Entry(self.forget_frame, highlightthickness=0, relief=FLAT,
                                      bg="white", fg="black", font=("yu gothic ui", 12, "bold"))
        self.user_email_entry.place(x=550, y=205, width=300)

        Canvas(self.forget_frame, width=300, height=2.0, bg="black", highlightthickness=0).place(x=550, y=230)

        email_icon_img = Image.open("C:\\Users\\user\\Downloads\\img16.png")
        resized_email_icon = email_icon_img.resize((25, 25))
        self.email_icon_photo = ImageTk.PhotoImage(resized_email_icon)

        self.email_icon_label = Label(self.forget_frame, image=self.email_icon_photo, bg="white")
        self.email_icon_label.image = self.email_icon_photo
        self.email_icon_label.place(x=515, y=200)

        forget_btn_img = Image.open("C:\\Users\\user\\Downloads\\img17.png")
        resized_forget_btn = forget_btn_img.resize((200, 60))
        self.forget_btn_photo = ImageTk.PhotoImage(resized_forget_btn)

        self.send_email_btn = Button(self.forget_frame, image=self.forget_btn_photo, text="",
                                     font=("yu gothic ui", 13, "bold"), compound="center", fg="white",
                                     bd=0, bg="white", activebackground="white", cursor="hand2",
                                     command=lambda: self.submit_forgot_password())


        self.send_email_btn.image = self.forget_btn_photo
        self.send_email_btn.place(x=550, y=300)

        back_btn_img = Image.open("C:\\Users\\user\\Downloads\\img19.png")
        resized_back_btn = back_btn_img.resize((60, 60))
        self.back_btn_photo = ImageTk.PhotoImage(resized_back_btn)

        self.back_to_lgn_btn = Button(self.forget_frame, image=self.back_btn_photo, bd=0, bg="white",
                                      activebackground="white", cursor="hand2", command=self.return_to_login)
        self.back_to_lgn_btn.image = self.back_btn_photo
        self.back_to_lgn_btn.place(x=820, y=295)


    def change_password(self):
        new_password = self.new_password_entry.get()
        new_password_confirm = self.confirm_password_entry.get()

        to_send = f"{FOR_MSG}{DELIMITER}{new_password}{DELIMITER}{new_password_confirm}"
        self.network.send_with_size(to_send.encode())

        response = self.network.recv_by_size().decode()

        if response == FOR_SUCCESSFUL:
            self.__init__(self.window,self.network)




    def submit_forgot_password(self):
        email = self.user_email_entry.get()

        if not email or "@" not in email:
            print("Error: Please enter a valid email address")
            return

        to_send = f"{FOR_MSG}{DELIMITER}{email}"
        self.network.send_with_size(to_send.encode())

        response = self.network.recv_by_size().decode()
        if "EML" in response:
            self.email_code_page("forget password")



    def opening_page(self,username):
        #user
        to_send = f"{GET_USER}{DELIMITER}{username}"
        self.network.send_with_size(to_send)
        from_server = self.network.recv_by_size().decode()

        num_of_cups = from_server.split(DELIMITER)[1]

        #background image
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()

        self.bg_frame = Image.open("C:\\Users\\user\\Downloads\\img20.png")
        self.bg_frame = self.bg_frame.resize((width, height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(self.bg_frame)

        self.bg_panel = Label(self.window, image=photo, bd=0)
        self.bg_panel.image = photo
        self.bg_panel.place(x=0, y=0, relwidth=1, relheight=1)

        #frame
        self.opening_page_frame = Frame(self.window, bg="white", width=500, height=500)
        self.opening_page_frame.place(x=100, y=50)

        #username on screen
        self.username_icon_reg_img = Image.open("C:\\Users\\user\\Downloads\\img7.png")
        resized_image_user = self.username_icon_reg_img.resize((35,35))
        photo_user = ImageTk.PhotoImage(resized_image_user)
        self.username_icon_reg_label = Label(self.opening_page_frame, image=photo_user, bg="black")
        self.username_icon_reg_label.image = photo_user
        self.username_icon_reg_label.place(x=0, y=10)

        Label(self.opening_page_frame, text=username, font=("yu gothic ui", 10, "bold"),
              bg="white", fg="black").place(x=40, y=17)

        #num of cups on screen
        self.cups_icon_reg_img = Image.open("C:\\Users\\user\\Downloads\\img21.png")
        resized_image_user = self.cups_icon_reg_img.resize((35, 35))
        photo_user = ImageTk.PhotoImage(resized_image_user)
        self.cups_icon_reg_label = Label(self.opening_page_frame, image=photo_user, bg="black")
        self.cups_icon_reg_label.image = photo_user
        self.cups_icon_reg_label.place(x=0, y=55)

        Label(self.opening_page_frame, text=num_of_cups, font=("yu gothic ui", 10, "bold"),
              bg="white", fg="black").place(x=40, y=62)

        #start game button
        start_game_btn = Image.open("C:\\Users\\user\\Downloads\\img22.png")
        resized_back_btn = start_game_btn.resize((120, 120))
        self.start_game_btn_photo = ImageTk.PhotoImage(resized_back_btn)

        self.start_game = Button(self.opening_page_frame, image=self.start_game_btn_photo, bd=0, bg="white",
                                      activebackground="white", cursor="hand2", command=self.wait_screen)
        self.start_game.image = self.start_game_btn_photo
        self.start_game.place(x=150, y=250)


    def wait_screen(self):
        pass








def page(network_client):
    window = Tk()
    LoginForm(window,network_client)
    window.mainloop()

