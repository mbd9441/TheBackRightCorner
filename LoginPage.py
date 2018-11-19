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
        self.window.clear()

        self.label = tkinter.Label(self.window.frame, text="Login").grid(row=0, columnspan=2)

        self.enter_user_label = tkinter.Label(self.window.frame, text="Email:").grid(row=1, column=0)

        self.enter_user = tkinter.Entry(self.window.frame)
        self.enter_user.grid(row=1, column=1)

        self.enter_pass_label = tkinter.Label(self.window.frame, text="Password:").grid(row=2, column=0)

        self.enter_pass = tkinter.Entry(self.window.frame)
        self.enter_pass.grid(row=2, column=1)

        self.loginbutton = tkinter.Button(self.window.frame, text="Submit", command=self.login_loginbutton).grid(row=3, columnspan=2)

        self.errorcode=tkinter.StringVar()
        self.error_label = tkinter.Label(self.window.frame, textvariable=self.errorcode, fg='Red').grid(row=4, columnspan=2)

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
            userdict={
                'email': userresult[0],
                'isemployee': userresult[1]
            }
            print(userdict)
            passresult=self.window.dbconnector.makequery("SELECT password FROM account WHERE email='%s'" % (user_text,))
            if pass_text==passresult[0]:
                self.window.home_page(userdict)
            else:
                self.errorcode.set("Invalid Password")