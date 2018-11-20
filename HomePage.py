import tkinter

class homepage:
    window=None

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

        self.headerwrapper.pack(fill=tkinter.X, padx=(0,17))
        self.headerwrapperpadding.pack(side=tkinter.TOP, fill=tkinter.X, padx=10)
        self.displayorders.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=10, pady=(0,10))
        self.subwindow.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        self.scrollbar.config(command=self.scrollframe.yview)
        self.headerwrapper.grid_columnconfigure(0, weight=1, uniform="standard")
        self.headerwrapper.grid_columnconfigure(1, weight=1, uniform="standard")
        self.headerwrapper.grid_columnconfigure(2, weight=1, uniform="standard")
        self.headerwrapper.grid_columnconfigure(3, weight=1, uniform="standard")

    
    def orders_customer(self):
        self.scrollframe=tkinter.Listbox(self.displayorders, yscrollcommand=self.scrollbar.set, highlightthickness=0, background=self.window.darkcolor)

        self.tracking=tkinter.Label(self.headerwrapper,text="Tracking #", background=self.window.darkcolor).grid(row=0,column=0, sticky=tkinter.EW)
        self.deliverydate=tkinter.Label(self.headerwrapper,text="Delivery Date", background=self.window.darkcolor).grid(row=0,column=1, sticky=tkinter.EW)
        self.status=tkinter.Label(self.headerwrapper,text="Status", background=self.window.darkcolor).grid(row=0,column=2, sticky=tkinter.EW)
        self.total=tkinter.Label(self.headerwrapper,text="Total", background=self.window.darkcolor).grid(row=0,column=3, sticky=tkinter.EW)

        orderbook=self.queryorderscustomer()

        for i in range(0, len(orderbook)):
            field=0
            for key, value in orderbook[i].items():
                if key == 'tracking':
                    self.trackingbutton=tkinter.Button(self.scrollframe,text=value, background=self.window.lightcolor, activebackground=self.window.darkcolor, command=lambda value=value:self.window.order_page(value))
                    self.trackingbutton.grid(row=i+1, column=field, sticky=tkinter.NSEW)
                else:
                    self.currentfield=tkinter.Label(self.scrollframe,text=value, background=self.window.lightcolor).grid(row=i+1, column=field, sticky=tkinter.NSEW)
                field+=1

        self.scrollframe.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        self.scrollframe.grid_columnconfigure(0, weight=1, uniform="standard")
        self.scrollframe.grid_columnconfigure(1, weight=1, uniform="standard")
        self.scrollframe.grid_columnconfigure(2, weight=1, uniform="standard")
        self.scrollframe.grid_columnconfigure(3, weight=1, uniform="standard")

    def queryorderscustomer(self):
        orderresult = self.window.dbconnector.makequery("select tracking_number,status,date from shipping_order WHERE account_ID =(SELECT id from account where account.email ='%s');" % (self.window.userdict['email']))
        orderbook=[]
        for i in range(0,len(orderresult)):
            order = orderresult[i]
            orderdict={
                'tracking':str(order[0]),
                'deliverydate':str(order[2]),
                'status':str(order[1]),
                'total':str(0)
            }
            orderbook.append(orderdict)
        return orderbook