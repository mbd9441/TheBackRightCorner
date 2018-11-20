import tkinter

"""
listview
    generates a view containing a list with headers inside the root window
"""
class listview:
    window=None
    columns=[]
    dictlist=[]

    """
    parameters:
        window - the root window
        title - the title of the page, string
        columns - a list of columns to generate, array
        dictlist - a list of dictionaries containing all rows and fields from a query, array of dictionaries
    """
    def __init__(self, window, title, columns, dictlist, orderid=None):
        self.window=window
        self.columns=columns
        self.dictlist=dictlist
        self.subwindow=tkinter.Frame(self.window.frame, background=self.window.lightcolor)
        self.orderid=orderid

        self.label = tkinter.Label(self.subwindow, text=title, background=self.window.lightcolor, font=("Courier", 20, 'bold'))
        self.label.pack(fill=tkinter.X)

        if self.window.userdict['isemployee']:
            pass
        else:
            self.build_list_view(self.dictlist)

        self.subwindow.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

    """
    build_list_view
        builds the actual list and headers themselves
    parameters:
        self - listview objst, implied
        dictlist - a list of dictionaries built to generate the list view based on their field
    returns:
        N/A
    """
    def build_list_view(self, dictlist):
        self.headerwrapperpadding=tkinter.Frame(self.subwindow, background=self.window.darkcolor)
        self.headerwrapper=tkinter.Frame(self.headerwrapperpadding, background=self.window.darkcolor)

        self.displayorders=tkinter.Frame(self.subwindow)
        self.scrollbar=tkinter.Scrollbar(self.displayorders, background=self.window.darkcolor)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.scrollframe=tkinter.Listbox(self.displayorders, yscrollcommand=self.scrollbar.set, highlightthickness=0, background=self.window.darkcolor)

        for col in range(0, len(self.columns)):
            self.tracking=tkinter.Label(self.headerwrapper,text=self.columns[col], background=self.window.darkcolor, font=("Arial", 10, 'bold')).grid(row=0,column=col, sticky=tkinter.EW)
            self.scrollframe.grid_columnconfigure(col, weight=1, uniform="standard")
            self.headerwrapper.grid_columnconfigure(col, weight=1, uniform="standard")

        for i in range(0, len(dictlist)):
            field=0
            print(dictlist[i])
            for key, value in dictlist[i].items():
                if key == self.columns[0]:
                    link=None
                    if key == "Tracking #":
                        link = lambda value=value:self.window.order_page(value)
                    elif key == "Package":
                        link = lambda value=value:self.window.package_page(value, self.orderid)
                    self.linkbutton=tkinter.Button(self.scrollframe,text=value, background=self.window.lightcolor, activebackground=self.window.darkcolor, command=link)
                    self.linkbutton.grid(row=i+1, column=field, sticky=tkinter.NSEW)
                else:
                    self.currentfield=tkinter.Label(self.scrollframe,text=value, background=self.window.lightcolor).grid(row=i+1, column=field, sticky=tkinter.NSEW)
                field+=1

        self.scrollframe.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        self.scrollbar.config(command=self.scrollframe.yview)
        self.headerwrapper.pack(fill=tkinter.X, padx=(0,17))
        self.headerwrapperpadding.pack(side=tkinter.TOP, fill=tkinter.X, padx=10)
        self.displayorders.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=10, pady=(0,10))