import tkinter

class homepage:
    window=None
    columns=['Tracking #','Delivery Date','Status','Total']

    def __init__(self, window):
        self.window=window

    def home_page(self):
        self.subwindow=tkinter.Frame(self.window.frame, background=self.window.lightcolor)

        self.label = tkinter.Label(self.subwindow, text="Orders", background=self.window.lightcolor, font=("Courier", 20, 'bold'))
        self.label.pack(fill=tkinter.X)

        self.headerwrapperpadding=tkinter.Frame(self.subwindow, background=self.window.darkcolor)
        self.headerwrapper=tkinter.Frame(self.headerwrapperpadding, background=self.window.darkcolor)

        self.displayorders=tkinter.Frame(self.subwindow)
        self.scrollbar=tkinter.Scrollbar(self.displayorders, background=self.window.darkcolor)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        if self.window.userdict['isemployee']:
            pass
        else:
            self.orders_customer()

        self.scrollbar.config(command=self.scrollframe.yview)
        self.headerwrapper.pack(fill=tkinter.X, padx=(0,17))
        self.headerwrapperpadding.pack(side=tkinter.TOP, fill=tkinter.X, padx=10)
        self.displayorders.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=10, pady=(0,10))
        self.subwindow.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

    
    def orders_customer(self):
        self.scrollframe=tkinter.Listbox(self.displayorders, yscrollcommand=self.scrollbar.set, highlightthickness=0, background=self.window.darkcolor)

        for col in range(0, len(self.columns)):
            self.tracking=tkinter.Label(self.headerwrapper,text=self.columns[col], background=self.window.darkcolor, font=("Arial", 10, 'bold')).grid(row=0,column=col, sticky=tkinter.EW)
            self.scrollframe.grid_columnconfigure(col, weight=1, uniform="standard")
            self.headerwrapper.grid_columnconfigure(col, weight=1, uniform="standard")

        query = "select tracking_number, date, status, status from shipping_order WHERE account_ID =(SELECT id from account where account.email ='%s');" % (self.window.userdict['email'])
        queryarray=self.queryorderscustomer(query)
        print(queryarray)
        for i in range(0, len(queryarray)):
            field=0
            for key, value in queryarray[i].items():
                if key == 'Tracking #':
                    self.trackingbutton=tkinter.Button(self.scrollframe,text=value, background=self.window.lightcolor, activebackground=self.window.darkcolor, command=lambda value=value:self.window.order_page(value))
                    self.trackingbutton.grid(row=i+1, column=field, sticky=tkinter.NSEW)
                else:
                    self.currentfield=tkinter.Label(self.scrollframe,text=value, background=self.window.lightcolor).grid(row=i+1, column=field, sticky=tkinter.NSEW)
                field+=1

        self.scrollframe.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

    def queryorderscustomer(self, query):
        queryresult = self.window.dbconnector.makequery(query)
        queryarray=[]
        for i in range(0,len(queryresult)):
            row = queryresult[i]
            rowdict={}
            for j in range(0,len(row)):
                rowdict[self.columns[j]]=str(row[j])
            queryarray.append(rowdict)
        return queryarray