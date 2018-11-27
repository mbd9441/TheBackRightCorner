import tkinter
from time import gmtime, strftime

"""
"""
class updateview:
    window=None
    columns=[]
    dictlist=[]

    """
     """
    def __init__(self, window, packageid, title):
        self.window=window
        self.packageid=packageid
        self.update_location_page(title)
        


    """

    """
    def update_location_page(self, title):
        self.subwindow=tkinter.Frame(self.window.frame, background=self.window.frame.cget('background'))

        self.label = tkinter.Label(self.subwindow, text=title, background=self.window.lightcolor, font=("Courier", 20, 'bold'))
        self.label.pack(fill=tkinter.X)

        self.updatecontainer=tkinter.Frame(self.subwindow)

        self.updatecontainer.grid_columnconfigure(0, weight=1, uniform="standard")
        self.updatecontainer.grid_columnconfigure(1, weight=1, uniform="standard")
        
        self.dropdownlabel=tkinter.Label(self.updatecontainer, text="Location Type", anchor=tkinter.W)
        self.dropdownlabel.grid(row=0, column=0, sticky=tkinter.NSEW)

        self.variable = tkinter.StringVar(self.updatecontainer)
        self.variable.set("Shipping Center") # default value

        self.locationchoice = tkinter.OptionMenu(self.updatecontainer, self.variable, "Truck", "Shipping Center", "Plane")
        self.locationchoice.grid(row=0, column=1, sticky=tkinter.NSEW)

        self.number=tkinter.Label(self.updatecontainer, text="Location ID", anchor=tkinter.W)
        self.number.grid(row=1, column=0, sticky=tkinter.NSEW)

        self.enter_number = tkinter.Entry(self.updatecontainer)
        self.enter_number.grid(row=1, column=1, sticky=tkinter.NSEW)

        self.desc=tkinter.Label(self.updatecontainer, text="Description", anchor=tkinter.W)
        self.desc.grid(row=2, column=0, sticky=tkinter.NSEW)

        self.enter_desc = tkinter.Entry(self.updatecontainer)
        self.enter_desc.grid(row=2, column=1, sticky=tkinter.NSEW)

        self.updatecontainer.pack(fill=tkinter.BOTH)

        self.submitbutton=tkinter.Button(self.subwindow, text="Submit", font=("Arial", 10, 'bold'), background=self.window.darkcolor, activebackground=self.window.darkercolor, command=self.update_submit).pack()
        self.subwindow.pack()

    """
    login_loginbutton()
    The function called by the loginbutton in the login page. Gets the text from the Username and Password fields
    If there is an error, it updates the text in errorcode displayed on the login page inside error_label
    Parameters: self, implied
    Returns: N/A
    """
    def update_submit(self):
        packageid=self.packageid
        locationtype=self.variable.get()
        enter_number=self.enter_number.get()
        enter_desc=self.enter_desc.get()
        currenttime=strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print(currenttime)

        if (locationtype=='Shipping Center'):
            insertquery='INSERT INTO package_location (\"package.id\", time, description, \"shipping_center.id\") VALUES (%s, \'%s\', \'%s\', %s)' % (packageid, currenttime, enter_desc, enter_number)
            self.window.dbconnector.insertquery(insertquery)
        elif (locationtype=='Truck'):
            insertquery='INSERT INTO package_location (\"package.id\", time, description, \"truck.id\") VALUES (%s, \'%s\', \'%s\', %s)' % (packageid, currenttime, enter_desc, enter_number)
            self.window.dbconnector.insertquery(insertquery)
        elif (locationtype=='Plane'):
            insertquery='INSERT INTO package_location (\"package.id\", time, description, \"plane.id\") VALUES (%s, \'%s\', \'%s\', %s)' % (packageid, currenttime, enter_desc, enter_number)
            self.window.dbconnector.insertquery(insertquery)
        else:
            print('error')
        print(locationtype, enter_number, enter_desc)
        self.window.location_history_page(packageid)