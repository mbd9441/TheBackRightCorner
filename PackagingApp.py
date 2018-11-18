import tkinter, psycopg2
"""""
    A bunch of bullshit
"""
class PackagingApp:
    master=None
    window=None
    dbconnector=None

    def __init__(self, master):
        master = master
        master.title("Packaging App")
        master.geometry("500x500")
        master.resizable(0,0)

        self.window = tkinter.Frame(self.master)
        self.window.pack()
        self.login_page()

        self.dbconnector=dbconnector()
    
    """
    clear()
    Clears the Window containing all widgets. Must be called at the beginning of every new view using 'master' window or else they will stack on each other.
    parameters: self, implied
    returns: N/A
    """
    def clear(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    """
    login_page()
    The first page the user sees; must use this to log in to the application
    Parameters: self, implied
    Returns: N/A
    """
    def login_page(self):
        self.clear()

        self.label = tkinter.Label(self.window, text="Login").grid(row=0, columnspan=2)

        self.enter_user_label = tkinter.Label(self.window, text="Email:").grid(row=1, column=0)

        self.enter_user = tkinter.Entry(self.window)
        self.enter_user.grid(row=1, column=1)

        self.enter_pass_label = tkinter.Label(self.window, text="Password:").grid(row=2, column=0)

        self.enter_pass = tkinter.Entry(self.window)
        self.enter_pass.grid(row=2, column=1)

        self.loginbutton = tkinter.Button(self.window, text="Submit", command=self.login_loginbutton).grid(row=3, columnspan=2)

        self.errorcode=tkinter.StringVar()
        self.error_label = tkinter.Label(self.window, textvariable=self.errorcode, fg='Red').grid(row=4, columnspan=2)

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

        userresult = dbconnector.makequery(self.dbconnector, "SELECT email, isemployee FROM account WHERE email='%s'" % (user_text,))
        print(userresult)

        if userresult is None:
            self.errorcode.set("Email not found")
        else:
            userdict={
                'email': userresult[0],
                'isemployee': userresult[1]
            }
            print(userdict)
            passresult=dbconnector.makequery(self.dbconnector, "SELECT password FROM account WHERE email='%s'" % (user_text,))
            if pass_text==passresult[0]:
                self.home_page(userdict)
            else:
                self.errorcode.set("Invalid Password")

    def home_page(self,userdict):
        self.clear()

        self.label = tkinter.Label(self.window, text="Welcome")
        self.label.pack()

        self.label = tkinter.Label(self.window, text=userdict['email'])
        self.label.pack()

        self.logout_button=tkinter.Button(self.window, text="Logout", command=self.logout).pack()
    
    def logout(self):
        self.login_page()



class dbconnector:
    connection=None
    def __init__(self):
        try:
            self.connection = psycopg2.connect("dbname='p32003g' user='p32003g' host='reddwarf.cs.rit.edu' password='Pheicothaequ7aeghohG'")
            print("Connection Successful")
        except:
            print("Connection Error")
    
    def __enter__(self):
        return self

    def makequery(self, query):
        print(query)
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return result

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

root = tkinter.Tk()
my_gui = PackagingApp(root)
root.mainloop()