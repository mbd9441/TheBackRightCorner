import tkinter

class homepage:
    window=None

    def __init__(self, window):
        self.window=window

    def home_page(self):
        self.subwindow=tkinter.Frame(self.window.frame)

        self.label = tkinter.Label(self.subwindow, text="Orders", background=self.window.frame.cget('background'), font=("Courier", 20, 'bold'))
        self.label.pack(fill=tkinter.X)

        if self.window.userdict['isemployee']:
            pass
        else:
            self.orders_customer()

        self.subwindow.pack(fill=tkinter.X)
    
    def orders_customer(self):
        self.displayorders=tkinter.Frame(self.subwindow, relief=tkinter.SUNKEN)

        self.scrollbar=tkinter.Scrollbar(self.displayorders)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.scrollframe=tkinter.Listbox(self.displayorders, yscrollcommand=self.scrollbar.set)

        self.scrollframe.grid_columnconfigure(0, weight=1)
        self.scrollframe.grid_columnconfigure(1, weight=1)
        self.scrollframe.grid_columnconfigure(2, weight=1)
        self.scrollframe.grid_columnconfigure(3, weight=1)

        self.tracking=tkinter.Label(self.scrollframe,text="Tracking Number").grid(row=0,column=0, sticky=tkinter.NSEW)
        self.deliverydate=tkinter.Label(self.scrollframe,text="DeliveryDate").grid(row=0,column=1, sticky=tkinter.NSEW)
        self.status=tkinter.Label(self.scrollframe,text="Status").grid(row=0,column=2, sticky=tkinter.NSEW)
        self.total=tkinter.Label(self.scrollframe,text="Total").grid(row=0,column=3, sticky=tkinter.NSEW)

        orderresult = self.window.dbconnector.makequery("select tracking_number,status,date from shipping_order WHERE account_ID =(SELECT id from account where account.email ='%s');" % (self.window.userdict['email']))
        for i in range(0,len(orderresult)):
            
            order = orderresult[i]
            print(order)
            orderdict={
                'tracking':str(order[0]),
                'deliverydate':str(order[2]),
                'status':str(order[1]),
                'total':str(0)
            }
            print(orderdict)
            field=0
            for key, value in orderdict.items():
                if key == 'tracking':
                    print(value)
                    self.trackingbutton=tkinter.Button(self.scrollframe,text=value, command=lambda value=value:self.window.order_page(value))
                    self.trackingbutton.grid(row=i+1, column=field, sticky=tkinter.NSEW)
                else:
                    self.currentfield=tkinter.Label(self.scrollframe,text=value).grid(row=i+1, column=field, sticky=tkinter.NSEW)
                field+=1
            
        self.scrollframe.pack(fill=tkinter.X)
        self.displayorders.pack(fill=tkinter.X)