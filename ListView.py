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
    def __init__(self, window, title, columns, dictlist, **keyword_parameters):
        self.window=window
        self.columns=columns
        self.dictlist=dictlist
        self.subwindow=tkinter.Frame(self.window.frame, background=self.window.lightcolor)
        self.orderid=None
        self.orderdict=None
        if ('orderid' in keyword_parameters):
            self.orderid=keyword_parameters['orderid']
        if ('orderdict' in keyword_parameters):
            self.orderid=keyword_parameters['orderdict']

        self.label = tkinter.Label(self.subwindow, text=title, background=self.window.lightcolor, font=("Courier", 20, 'bold'))
        self.label.pack(fill=tkinter.X)

        if ('Package ' in title) or ('Settings' in title):
            self.build_dict_view()
        elif ('Extra' in title):
            self.extra_query_build()
        else:
            self.build_list_view()

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
    def build_list_view(self):
        self.headerwrapperpadding=tkinter.Frame(self.subwindow, background=self.window.darkcolor)
        self.headerwrapper=tkinter.Frame(self.headerwrapperpadding, background=self.window.darkcolor)

        self.displaylist=tkinter.Frame(self.subwindow)
        self.scrollbar=tkinter.Scrollbar(self.displaylist, background=self.window.darkcolor)
        self.scrollframe=tkinter.Listbox(self.displaylist, background=self.window.darkcolor, highlightthickness=0, borderwidth=2, relief=tkinter.SUNKEN)

        for col in range(0, len(self.columns)):
            self.headers=tkinter.Label(self.headerwrapper, text=self.columns[col], background=self.window.darkcolor, font=("Arial", 10, 'bold')).grid(row=0,column=col, sticky=tkinter.EW)
            self.scrollframe.grid_columnconfigure(col, weight=1, uniform="standard")
            self.headerwrapper.grid_columnconfigure(col, weight=1, uniform="standard")

        for i in range(0, len(self.dictlist)):
            field=0
            print(self.dictlist[i])
            for key, value in self.dictlist[i].items():
                if key == self.columns[0]:
                    link=None
                    if key == "Tracking #":
                        link = lambda value=value:self.window.order_page(value)
                    elif key == "Package":
                        link = lambda value=value:self.window.package_page(value, self.orderid)
                    elif key == "Package ID":
                        link = lambda value=value:self.window.package_page(value, None)
                    self.linkbutton=tkinter.Button(self.scrollframe,text=value, activebackground=self.window.gray, command=link) 
                    self.linkbutton.grid(row=i+1, column=field, sticky=tkinter.NSEW)
                else:
                    self.currentfield=tkinter.Label(self.scrollframe,text=value).grid(row=i+1, column=field, sticky=tkinter.NSEW)
                field+=1

        self.headerwrapper.pack(fill=tkinter.X, padx=(0,17))
        self.headerwrapperpadding.pack(side=tkinter.TOP, fill=tkinter.X, padx=10)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.scrollframe.pack(fill=tkinter.BOTH, expand=True)
        self.displaylist.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=10, pady=(0,10))
        self.scrollbar.config(command=self.scrollframe.yview)
        self.scrollframe.config(yscrollcommand=self.scrollbar.set)

    def build_dict_view(self):
        self.displaylist=tkinter.Frame(self.subwindow, background=self.window.darkcolor, relief=tkinter.SUNKEN, borderwidth=2)

        self.displaylist.grid_columnconfigure(0, weight=1)
        self.displaylist.grid_columnconfigure(1, weight=2)

        field=0
        for key, value in self.dictlist[0].items():
            self.currentfield=tkinter.Label(self.displaylist, text=key, background=self.window.darkcolor, anchor=tkinter.W, font=("Arial", 10, 'bold')).grid(row=field, column=0, sticky=tkinter.NSEW)
            self.currentfield=tkinter.Label(self.displaylist, text=value, anchor=tkinter.E).grid(row=field, column=1, sticky=tkinter.NSEW)
            field+=1

        self.displaylist.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=10, pady=(0,10))

    def extra_query_build(self):
        pass