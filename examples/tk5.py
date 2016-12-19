try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk  # Python 2.x

class Navbar(tk.Frame):
    pass
class Toolbar(tk.Frame):
    pass
class Statusbar(tk.Frame): pass
class Main(tk.Frame): pass

class MainApplication(tk.Frame):
    def __init__(self, parent=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.statusbar = Statusbar(self)
        self.toolbar = Toolbar(self)
        self.navbar = Navbar(self)
        self.main = Main(self)
        tk.Label(self.main, text='haha')

        self.statusbar.pack(side="bottom", fill="x")
        self.toolbar.pack(side="top", fill="x")
        self.navbar.pack(side="left", fill="y")
        self.main.pack(side="right", fill="both", expand=True)

app = MainApplication()
app.mainloop()
