import tkinter

class orderpage:
    window=None

    def __init__(self, window):
        self.window=window

    def order_page(self, orderid):
        print("order_page orderid " + orderid)
        self.subwindow=tkinter.Frame(self.window.frame)

        self.label = tkinter.Label(self.subwindow, text="Order %s" % str(orderid), background=self.window.frame.cget('background'), font=("Courier", 20, 'bold'))
        self.label.pack(fill=tkinter.X)
            
        self.subwindow.pack(fill=tkinter.X)