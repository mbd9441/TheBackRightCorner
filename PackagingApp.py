import tkinter, DBConnector, LoginPage, ListView, UpdateView
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
        self.columns = ['Package','Delivery Date','Status']

        footerquery = "select tracking_number, date, status from shipping_order WHERE account_ID = %s;" % (orderid)
        footerdictlist=self.dbconnector.querydictlist(footerquery, self.columns)

        ordertotalquery="select * from total_order_cost(%s)" % (orderid)
        ordertotalresult=self.dbconnector.makequery(ordertotalquery)[0][0]

        footerdictlist[0]['Total']=ordertotalresult

        self.columns.append('Total')

        self.footer(footerdictlist=footerdictlist[0])

        query = "select id, delivery_date, 'false' as status, cost+shipping_cost as total from package where \"shipping_order.tracking_number\"=%s;" % orderid
        dictlist=self.dbconnector.querydictlist(query, self.columns)
        orderpage=ListView.listview(self, title, self.columns, dictlist, orderid=orderid)

    def receipt(self, orderid):
        receipt = Receipt.receiptpage(orderid)

    def package_page(self, packageid, orderid):
        self.clear()
        if(self.userdict['shippingcenter']):
            self.header(back=None)
        else:
            self.header(back=orderid)
        title="Package %s" % str(packageid)
        self.columns=['Cost', 'Shipping Cost', 'Total', 'International', 'Hazardous']
        query = "select cost, shipping_cost, cost + shipping_cost as total, international, hazardous from package where id=%s;" % packageid
        dictlist=self.dbconnector.querydictlist(query, self.columns)[0]
        self.columns=['Shipping Center', 'Plane', 'Truck', 'Description', 'Updated']
        packagequery = "select \"shipping_center.id\", \"plane.id\", \"truck.id\", description, time from curr_location(%s)" % packageid
        dictlist2=self.dbconnector.querydictlist(packagequery, self.columns)[0]
        dictlist.update(dictlist2)
        if (dictlist['Shipping Center'] == 'None'):
            del dictlist['Shipping Center']
        if (dictlist['Plane'] == 'None'):
            del dictlist['Plane']
        if (dictlist['Truck'] == 'None'):
            del dictlist['Truck']
        footer=self.footer(package=packageid)
        packagepage=ListView.listview(self, title, self.columns, [dictlist])

    def location_history_page(self, packageid):
        self.clear()
        self.header(back="package." + packageid)
        title="Location History"
        self.columns=['Shipping Center', 'Plane', 'Truck', 'Description', 'Updated']
        query = "select \"shipping_center.id\", \"plane.id\", \"truck.id\", description, time from package_location where \"package.id\" = %s" % packageid
        dictlist=self.dbconnector.querydictlist(query, self.columns)
        if self.userdict['shippingcenter'] is not None:
            footer=self.footer(footerbutton='Update Location', package=packageid)
        locationpage=ListView.listview(self, title, self.columns, dictlist, idbutton=False)

    def update_location(self, packageid):
        self.clear()
        self.header()
        title="Update Location for Package %s" % (packageid)
        updatelocation=UpdateView.updateview(self, packageid, title)

    def settings_page(self):
        self.clear()
        self.header()
        title="Settings"
        self.columns=['First Name','Last Name', 'Email', 'Phone']
        query= "select first_name, last_name, email, phone_number from account where id = %s" % (self.userdict['id'])
        dictlist=self.dbconnector.querydictlist(query, self.columns)
        if self.userdict['shippingcenter'] is not None:
            dictlist[0]['Shipping Center']=self.userdict['shippingcenter']
            footer=self.footer(footerbutton='Extra Queries')
        else:
            footer=self.footer(footerbutton='Settings')
        settingspage=ListView.listview(self, title, self.columns, dictlist)

    def credit_card_page(self):
        self.clear()
        self.header(back='settings')
        title="Credit Cards"
        self.columns=['Card Number', 'Expiration Date']
        query= "select RIGHT(CAST(card_number as varchar), 4), expiration_date from credit_card where \"account.ID\" = %s" % (self.userdict['id'])
        dictlist=self.dbconnector.querydictlist(query, self.columns)
        creditcardpage=ListView.listview(self, title, self.columns, dictlist, idbutton=False)

    def address_page(self):
        self.clear()
        self.header(back='settings')
        title="Addresses"
        self.columns=['Number', 'Apartment', 'Street', 'Territory', 'State', 'Zip', 'Country']
        query= "select number, apartment, street, city, territory, zip_code, country from address where \"account.ID\" = %s" % (self.userdict['id'])
        dictlist=self.dbconnector.querydictlist(query, self.columns)
        creditcardpage=ListView.listview(self, title, self.columns, dictlist, idbutton=False)

    def extra_queries(self):
        self.clear()
        self.header(back='settings')
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

    def most_shipping_spent(self):
        self.clear()
        self.header(back='extraqueries')
        title = "Customer"
        self.columns=['First Name','Last Name', 'Cost']
        query = 'select account.first_name, account.last_name, most_shipping_spent.cost from most_shipping_spent() inner join account on account.id=most_shipping_spent.id'
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
            elif (keyword_parameters['back'] == 'settings'):
                link=lambda:self.settings_page()
            elif ("package" in keyword_parameters['back']):
                packageid=keyword_parameters['back'].split('.')[1]
                query='select \"shipping_order.tracking_number\" from package where id=%s' % (packageid)
                orderid=str(self.dbconnector.makequery(query)[0][0])
                link=lambda packageid=packageid:self.package_page(packageid, orderid)
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
                    self.currentfield=tkinter.Label(self.footerwrapper,text='', background=self.lightcolor).grid(row=0, column=i, sticky=tkinter.NSEW)
                else:
                    self.currentfield=tkinter.Label(self.footerwrapper,text=value, background=self.lightcolor).grid(row=0, column=i, sticky=tkinter.NSEW)
                self.footerwrapper.grid_columnconfigure(i, weight=1, uniform="standard")
                i+=1
            self.footerwrapper.pack(fill=tkinter.X, padx=(0,17))
            self.footerwrapperpadding.pack(side=tkinter.BOTTOM, fill=tkinter.X, padx=10, pady=(0,10))

        elif ('footerbutton' in keyword_parameters):
            if keyword_parameters['footerbutton']=='Extra Queries':
                footerbutton=tkinter.Button(self.footerwrapper, text="Extra Queries", command=self.extra_queries, font=("Arial", 10, 'bold'), background=self.darkcolor, activebackground=self.darkercolor)
                footerbutton.pack()
            elif keyword_parameters['footerbutton']=='Settings':
                footerbutton=tkinter.Button(self.footerwrapper, text="Credit Cards", command=self.credit_card_page, font=("Arial", 10, 'bold'), background=self.darkcolor, activebackground=self.darkercolor)
                footerbutton.pack(side=tkinter.LEFT)
                footerbutton=tkinter.Button(self.footerwrapper, text="Addresses", command=self.address_page, font=("Arial", 10, 'bold'), background=self.darkcolor, activebackground=self.darkercolor)
                footerbutton.pack(side=tkinter.RIGHT)
            elif keyword_parameters['footerbutton']=='Update Location':
                packageid=keyword_parameters['package']
                link=lambda packageid=packageid:self.update_location(packageid)
                footerbutton=tkinter.Button(self.footerwrapper, text="Update Location", command=link, font=("Arial", 10, 'bold'), background=self.darkcolor, activebackground=self.darkercolor)
                footerbutton.pack()
            self.footerwrapper.pack(fill=tkinter.X)
            self.footerwrapperpadding.pack(side=tkinter.BOTTOM, fill=tkinter.X, padx=10, pady=(0,10))
        elif ('package' in keyword_parameters):
            packageid=keyword_parameters['package']
            link=lambda packageid=packageid:self.location_history_page(packageid)
            footerbutton=tkinter.Button(self.footerwrapper, text="Location History", command=link, font=("Arial", 10, 'bold'), background=self.darkcolor, activebackground=self.darkercolor)
            footerbutton.pack()
            self.footerwrapper.pack(fill=tkinter.X)
            self.footerwrapperpadding.pack(side=tkinter.BOTTOM, fill=tkinter.X, padx=10, pady=(0,10))


root = tkinter.Tk()
window = PackagingApp(root)
root.mainloop()