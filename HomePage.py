import tkinter

class homepage:
    window=None

    def __init__(self, window):
        self.window=window

    def home_page(self,userdict):
        self.window.clear()

        self.label = tkinter.Label(self.window.frame, text="Welcome")
        self.label.pack()

        self.label = tkinter.Label(self.window.frame, text=userdict['email'])
        self.label.pack()

        self.logout_button=tkinter.Button(self.window.frame, text="Logout", command=self.logout).pack()
    
    def logout(self):
        self.window.login_page()