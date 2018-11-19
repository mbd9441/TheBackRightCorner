import tkinter, DBConnector, LoginPage, HomePage, SettingsPage, OrderPage
"""""
    A bunch of bullshit
"""
class PackagingApp:
    master=None
    frame=None
    dbconnector=None
    userdict=None

    def __init__(self, master):
        master = master
        master.title("Packaging App")
        master.geometry("400x300")
        master.resizable(0,0)
        master.configure(background='#c29661')

        self.dbconnector=DBConnector.dbconnector()

        self.frame = tkinter.Frame(self.master, background='#c29661')
        self.frame.pack(fill=tkinter.BOTH)

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

    """
    """
    def login_page(self):
        self.clear()
        loginpage=LoginPage.loginpage(self)
        loginpage.login_page()

    """
    """
    def home_page(self):
        self.clear()
        self.header()
        homepage=HomePage.homepage(self)
        homepage.home_page()

    def order_page(self, orderid):
        self.clear()
        print("packagingapp orderid " + orderid)
        self.header(back=orderid)
        orderpage=OrderPage.orderpage(self)
        orderpage.order_page(orderid)

    def settings_page(self):
        self.clear()
        self.header()
        settingspage=SettingsPage.settingspage(self)
        settingspage.settings_page()
    
    def header(self, **keyword_parameters):
        self.headerframe=tkinter.Frame(self.frame, background='#9a7958')

        self.logout_button=tkinter.Button(self.headerframe, text="Logout", command=lambda:self.login_page(), background='#9a7958', activebackground='#7c6247')
        self.logout_button.pack(side=tkinter.LEFT)

        self.settings=tkinter.Button(self.headerframe, text="Settings", command=lambda:self.settings_page(), background='#9a7958', activebackground='#7c6247')
        self.settings.pack(side=tkinter.LEFT)

        self.settings=tkinter.Button(self.headerframe, text="Orders", command=lambda:self.home_page(), background='#9a7958', activebackground='#7c6247')
        self.settings.pack(side=tkinter.LEFT)

        if ('back' in keyword_parameters):
            self.settings=tkinter.Button(self.headerframe, text="Back", command=lambda:self.home_page(), background='#9a7958', activebackground='#7c6247')
            self.settings.pack(side=tkinter.LEFT)

        self.label = tkinter.Label(self.headerframe, text=self.userdict['email'], background=self.headerframe.cget('background'))
        self.label.pack(side=tkinter.RIGHT)

        self.headerframe.pack(fill=tkinter.X)

root = tkinter.Tk()
window = PackagingApp(root)
root.mainloop()