import tkinter

class receiptpage:

    def __init__(self, master, orderid):
        self.win=tkinter.Toplevel()
        self.window=master
        columns=['First Name', 'Last Name', 'Email']
        query = "select first_name, last_name, email from account where id=(select account_id from shipping_order where tracking_number=%s)" % (orderid)
        self.header=self.window.dbconnector.querydictlist(query, columns)[0]
        print(self.header)
        for items in columns:
            self.headerbill=tkinter.Label(self.window, text=self.header[items])
            print(items)
        self.headerbill.pack()