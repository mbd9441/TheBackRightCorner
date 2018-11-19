import tkinter

class loginpage:
    window=None

    def __init__(self, window):
        self.window=window

    """
    login_page()
    The first page the user sees; must use this to log in to the application
    Parameters: self, implied
    Returns: N/A
    """
    def login_page(self):
        self.subwindow=tkinter.Frame(self.window.frame, background=self.window.frame.cget('background'))

        self.label = tkinter.Label(self.subwindow, text="Login", font=("Courier", 40, 'bold'), background=self.subwindow.cget('background')).grid(row=0, columnspan=2)

        self.enter_user_label = tkinter.Label(self.subwindow, text="Email:", anchor=tkinter.W, background='#9a7958').grid(row=1, column=0, sticky=tkinter.EW)

        self.enter_user = tkinter.Entry(self.subwindow)
        self.enter_user.grid(row=1, column=1)

        self.enter_pass_label = tkinter.Label(self.subwindow, text="Password:", anchor=tkinter.W, background='#9a7958').grid(row=2, column=0, sticky=tkinter.EW)

        self.enter_pass = tkinter.Entry(self.subwindow)
        self.enter_pass.grid(row=2, column=1)

        self.loginbutton = tkinter.Button(self.subwindow, text="Submit", background='#9a7958', activebackground='#7c6247', command=self.login_loginbutton).grid(row=3, columnspan=2)

        self.errorcode=tkinter.StringVar()
        self.error_label = tkinter.Label(self.subwindow, textvariable=self.errorcode, fg='Red', background=self.subwindow.cget('background')).grid(row=4, columnspan=2)

        self.subwindow.pack()

    """
    login_loginbutton()
    The function called by the loginbutton in the login page. Gets the text from the Username and Password fields
    If there is an error, it updates the text in errorcode displayed on the login page inside error_label
    Parameters: self, implied
    Returns: N/A
    """
    def login_loginbutton(self):
        user_text=self.enter_user.get()
        pass_text=self.enter_pass.get()

        print(user_text)
        print(pass_text)

        userresult = self.window.dbconnector.makequery("SELECT email, isemployee FROM account WHERE email='%s'" % (user_text,))
        print(userresult)

        if userresult is None:
            self.errorcode.set("Email not found")
        else:
            self.window.userdict={
                'email': userresult[0][0],
                'isemployee': userresult[0][1]
            }
            print(self.window.userdict)
            passresult=self.window.dbconnector.makequery("SELECT password FROM account WHERE email='%s'" % (user_text,))
            if pass_text==passresult[0][0]:
                self.window.home_page()
            else:
                self.errorcode.set("Invalid Password")