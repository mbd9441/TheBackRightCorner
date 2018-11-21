import tkinter

"""
listview
    generates a view containing a list with headers inside the root window
"""
class dictview:
    window=None

    """
    parameters:
        window - the root window
        title - the title of the page, string
        columns - a list of columns to generate, array
        dictlist - a list of dictionaries containing all rows and fields from a query, array of dictionaries
    """
    def __init__(self, window, title):
        self.window=window

        self.subwindow=tkinter.Frame(self.window.frame, background=self.window.lightcolor)

        self.label = tkinter.Label(self.subwindow, text=title, background=self.window.lightcolor, font=("Courier", 20, 'bold'))
        self.label.pack(fill=tkinter.X)

        self.subwindow.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)