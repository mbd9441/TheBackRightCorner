import tkinter, DBConnector, LoginPage, HomePage
"""""
    A bunch of bullshit
"""
class PackagingApp:
    master=None
    frame=None
    dbconnector=None

    def __init__(self, master):
        master = master
        master.title("Packaging App")
        master.geometry("500x500")
        master.resizable(0,0)

        self.dbconnector=DBConnector.dbconnector()

        self.frame = tkinter.Frame(self.master)
        self.frame.pack()

        self.login_page()

    """
    clear()
    Clears the Window containing all widgets. Must be called at the beginning of every new view using 'master' window or else they will stack on each other.
    parameters: self, implied
    returns: N/A
    """
    def clear(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def login_page(self):
        self.clear()
        loginpage=LoginPage.loginpage(self)
        loginpage.login_page()

    def home_page(self, userdict):
        self.clear()
        homepage=HomePage.homepage(self)
        homepage.home_page(userdict)

root = tkinter.Tk()
window = PackagingApp(root)

root.mainloop()