from tkinter import *
from PIL import ImageTk, Image


class LoginForm:
    def __init__(self, window):
        # build the window
        self.window = window
        self.window.geometry("1166x718")
        self.window.state("zoomed")
        self.window.resizable(0, 0)


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

        #forgot password
        self.forgot_button = Button(self.lgn_frame,text = "Forgot Password ?",font=("yu gothic ui", 13, "bold underline"),fg = "black",width = 25,bd = 0,bg = "white",activebackground="white",cursor = "hand2")
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





def page():
    window = Tk()
    LoginForm(window)
    window.mainloop()


if __name__ == "__main__":
    page()