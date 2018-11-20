import tkinter, DBConnector, LoginPage, ListView, SettingsPage, OrderPage
"""""
    A bunch of bullshit
"""
class PackagingApp:
    master=None
    frame=None
    dbconnector=None
    userdict=None
    lightcolor='#c29661'
    darkcolor='#9a7958'
    darkercolor='#7c6247'

    def __init__(self, master):
        master = master
        master.title("Packaging App")
        master.geometry("500x300")
        master.resizable(0,0)
        master.configure(background='#c29661')

        self.dbconnector=DBConnector.dbconnector()

        self.frame = tkinter.Frame(self.master, background=self.lightcolor)
        self.frame.pack(fill=tkinter.BOTH, expand=True)

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
        title="Orders"
        columns = ['Tracking #','Delivery Date','Status','Total']
        query = "select tracking_number, date, status, status from shipping_order WHERE account_ID =(SELECT id from account where account.email ='%s');" % (self.userdict['email'])
        dictlist=self.dbconnector.querydictlist(query, columns)
        homepage=ListView.listview(self, title, columns, dictlist)

    def order_page(self, orderid):
        self.clear()
        self.header(back=orderid)
        title="Order %s" % str(orderid)
        columns = []
        query = ''
        #dictlist=self.dbconnector.querydictlist(query, columns)
        dictlist={}
        homepage=ListView.listview(self, title, columns, dictlist)

    def settings_page(self):
        self.clear()
        self.header()
        settingspage=SettingsPage.settingspage(self)
        settingspage.settings_page()
    
    def header(self, **keyword_parameters):
        self.headerframe=tkinter.Frame(self.frame, background=self.darkcolor)

        self.logout_button=tkinter.Button(self.headerframe, text="Logout", command=lambda:self.login_page(), font=("Arial", 10, 'bold'), background=self.darkcolor, activebackground=self.darkercolor)
        self.logout_button.pack(side=tkinter.LEFT)

        self.settings=tkinter.Button(self.headerframe, text="Settings", command=lambda:self.settings_page(), font=("Arial", 10, 'bold'), background=self.darkcolor, activebackground=self.darkercolor)
        self.settings.pack(side=tkinter.LEFT)

        self.settings=tkinter.Button(self.headerframe, text="Orders", command=lambda:self.home_page(), font=("Arial", 10, 'bold'), background=self.darkcolor, activebackground=self.darkercolor)
        self.settings.pack(side=tkinter.LEFT)

        if ('back' in keyword_parameters):
            self.settings=tkinter.Button(self.headerframe, text="Back", command=lambda:self.home_page(), font=("Arial", 10, 'bold'), background=self.darkcolor, activebackground=self.darkercolor)
            self.settings.pack(side=tkinter.LEFT)

        self.label = tkinter.Label(self.headerframe, text=self.userdict['email'], font=("Arial", 10, 'bold'), background=self.darkcolor)
        self.label.pack(side=tkinter.RIGHT)

        self.headerframe.pack(fill=tkinter.X)

root = tkinter.Tk()
window = PackagingApp(root)
root.mainloop()