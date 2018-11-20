import tkinter

class settingspage:
    window=None

    def __init__(self, window):
        self.window=window

    def settings_page(self):
        self.subwindow=tkinter.Frame(self.window.frame)

        self.label = tkinter.Label(self.subwindow, text="Settings", background=self.window.lightcolor, font=("Courier", 20, 'bold'))
        self.label.pack(fill=tkinter.X)

        self.subwindow.pack(fill=tkinter.X)