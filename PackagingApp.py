import tkinter, DBConnector, LoginPage, ListView
"""""
    A bunch of bullshit
"""
class PackagingApp:
    master=None
    frame=None
    dbconnector=None
    userdict=None
    columns=[]
    lightcolor='#c29661'
    darkcolor='#9a7958'
    darkercolor='#7c6247'
    gray='#a0a0a0'

    def __init__(self, master):
        master = master
        master.title("Packaging App")
        master.geometry("600x400")
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
        self.columns=None
        title=''
        query=''
        if self.userdict['shippingcenter'] is not None:
            title="Packages at %s" % (self.userdict['shippingcenter'])
            self.columns = ['Package ID','Delivery Date', 'Updated', 'Location']
            query = "select package.id, package.delivery_date, package_location.time, package_location.description from package inner join package_location on package.id = package_location.\"package.id\" where package_location.\"shipping_center.id\"= %s" % (self.userdict['shippingcenter'])
        else:
            title="Orders"
            self.columns = ['Tracking #','Delivery Date','Status','Total']
            query = "select tracking_number, date, status, 0 from shipping_order WHERE account_ID = %s" % (self.userdict['id'])
        dictlist=self.dbconnector.querydictlist(query, self.columns)
        homepage=ListView.listview(self, title, self.columns, dictlist)

    def order_page(self, orderid):
        self.clear()
        self.header(back=None)
        title="Order %s" % str(orderid)
        self.columns = ['Package','Delivery Date','Status','Total']

        footerquery = "select tracking_number, date, status, 0 from shipping_order WHERE account_ID = %s;" % orderid
        footerdictlist=self.dbconnector.querydictlist(footerquery, self.columns)[0]
        self.footer(footerdictlist=footerdictlist)

        query = "select id, delivery_date, 'false' as status, cost+shipping_cost as total from package where \"shipping_order.tracking_number\"=%s;" % orderid
        dictlist=self.dbconnector.querydictlist(query, self.columns)
        orderpage=ListView.listview(self, title, self.columns, dictlist, orderid=orderid)
    
    def package_page(self, packageid, orderid):
        self.clear()
        self.header(back=orderid)
        title="Package %s" % str(packageid)
        self.columns=['Cost', 'Shipping Cost', 'Total', 'International', 'Hazardous']
        query = "select cost, shipping_cost, cost + shipping_cost as total, international, hazardous from package where id=%s;" % packageid
        dictlist=self.dbconnector.querydictlist(query, self.columns)
        packagepage=ListView.listview(self, title, self.columns, dictlist)

    def settings_page(self):
        self.clear()
        self.header()
        title="Settings"
        self.columns=['First Name','Last Name', 'Email', 'Phone']
        query= "select first_name, last_name, email, phone_number from account where id = %s" % (self.userdict['id'])
        dictlist=self.dbconnector.querydictlist(query, self.columns)
        if self.userdict['shippingcenter'] is not None:
            dictlist[0]['Shipping Center']=self.userdict['shippingcenter']
            footer=self.footer(footerbutton=True)
        settingspage=ListView.listview(self, title, self.columns, dictlist)

    def extra_queries(self):
        self.clear()
        self.header()
        title="Extra Queries"
        self.columns=['Description', 'Parameter', 'Submit']
        extraqueriespage=ListView.listview(self, title, self.columns, [])

    def extra_query_page(self, title, columns, dictlist):
        self.clear()
        self.header(back='extraqueries')
        self.columns=columns
        extraquerypage=ListView.listview(self,title,self.columns,dictlist)

    def crashed_truck_packages(self, truckid):
        self.clear()
        self.header(back='extraqueries')
        title = "Truck %s" % (truckid)
        self.columns=['Package ID', 'First Name', 'Last Name']
        query = "select * from truck_crash(%s)" % (truckid)
        dictlist=self.dbconnector.querydictlist(query, self.columns)
        extraquerypage=ListView.listview(self,title,self.columns,dictlist)

    def crashed_truck_last_delivered(self, truckid):
        self.clear()
        self.header(back='extraqueries')
        title = "Truck %s" % (truckid)
        self.columns=['Package ID', 'Time']
        query = "select \"package.id\", time from last_truck_delivery(%s)" % (truckid)
        dictlist=self.dbconnector.querydictlist(query, self.columns)
        extraquerypage=ListView.listview(self,title,self.columns,dictlist)

    def customer_most_packages(self):
        self.clear()
        self.header(back='extraqueries')
        title = "Customer"
        self.columns=['First Name','Last Name', 'Email', 'Phone']
        query = "select first_name, last_name, email, phone_number from account where id = most_shipped_account()"
        dictlist=self.dbconnector.querydictlist(query, self.columns)
        extraquerypage=ListView.listview(self,title,self.columns,dictlist)

    def street_most_customers(self):
        self.clear()
        self.header(back='extraqueries')
        title = "Street"
        self.columns=['Street','City','Zip Code']
        query = "select street, city, zip_code from street_most_customers()"
        dictlist=self.dbconnector.querydictlist(query, self.columns)
        extraquerypage=ListView.listview(self,title,self.columns,dictlist)

    def header(self, **keyword_parameters):
        link=None
        self.headerframe=tkinter.Frame(self.frame, background=self.darkcolor)

        self.logout_button=tkinter.Button(self.headerframe, text="Logout", command=lambda:self.login_page(), font=("Arial", 10, 'bold'), background=self.darkcolor, activebackground=self.darkercolor)
        self.logout_button.pack(side=tkinter.LEFT)

        self.settings=tkinter.Button(self.headerframe, text="Settings", command=lambda:self.settings_page(), font=("Arial", 10, 'bold'), background=self.darkcolor, activebackground=self.darkercolor)
        self.settings.pack(side=tkinter.LEFT)

        self.settings=tkinter.Button(self.headerframe, text="Orders", command=lambda:self.home_page(), font=("Arial", 10, 'bold'), background=self.darkcolor, activebackground=self.darkercolor)
        self.settings.pack(side=tkinter.LEFT)

        if ('back' in keyword_parameters):
            if (keyword_parameters['back'] is None):
                link=lambda:self.home_page()
            elif (keyword_parameters['back'] == 'extraqueries'):
                link=lambda:self.extra_queries()
            else:
                orderid=keyword_parameters['back']
                link=lambda orderid=orderid:self.order_page(orderid)
            self.settings=tkinter.Button(self.headerframe, text="Back", command=link, font=("Arial", 10, 'bold'), background=self.darkcolor, activebackground=self.darkercolor)
            self.settings.pack(side=tkinter.LEFT)

        self.label = tkinter.Label(self.headerframe, text=self.userdict['email'], font=("Arial", 10, 'bold'), background=self.darkcolor)
        self.label.pack(side=tkinter.RIGHT)

        self.headerframe.pack(fill=tkinter.X)

    def footer(self, **keyword_parameters):
        footerdictlist=None
        footerbutton=None
        self.footerwrapperpadding=tkinter.Frame(self.frame, background=self.lightcolor)
        self.footerwrapper=tkinter.Frame(self.footerwrapperpadding, background=self.lightcolor)
        if ('footerdictlist' in keyword_parameters):
            footerdictlist=keyword_parameters['footerdictlist']
            i=0
            for key, value in footerdictlist.items():
                if key == "Package":
                    self.currentfield=tkinter.Label(self.headerwrapper,text='', background=self.lightcolor).grid(row=0, column=i, sticky=tkinter.NSEW)
                else:
                    self.currentfield=tkinter.Label(self.headerwrapper,text=value, background=self.lightcolor).grid(row=0, column=i, sticky=tkinter.NSEW)
                self.footerwrapper.grid_columnconfigure(i, weight=1, uniform="standard")
                i+=1
        elif ('footerbutton' in keyword_parameters):
            footerbutton=tkinter.Button(self.footerwrapper, text="Extra Queries", command=self.extra_queries, font=("Arial", 10, 'bold'), background=self.darkcolor, activebackground=self.darkercolor)
            footerbutton.pack()
        self.footerwrapper.pack(fill=tkinter.X, padx=(0,17))
        self.footerwrapperpadding.pack(side=tkinter.BOTTOM, fill=tkinter.X, padx=10)

root = tkinter.Tk()
window = PackagingApp(root)
root.mainloop()