try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk  # Python 2.x

class KeyPad(tk.Frame):
    def __init__(self, *args, **kwargs):
        super(KeyPad, self).__init__(*args, **kwargs)
        #self.label = tk.Label(text='Hello, world')
        #self.label.pack(padx=10, pady=10)
        relief = 'raised'  # default?
        #relief = 'ridge'
        #relief = 'groove'
        #relief = 'flat'
        #relief = 'sunken'
        labels = [['1', '2', '3', 'A'],
                  ['4', '5', '6', 'B'],
                  ['7', '8', '9', 'C'],
                  ['*', '0', '#', 'D']]
        for row, rowlabels in enumerate(labels):
            for column, label in enumerate(rowlabels):
                button = tk.Button(self, text=label, width=1, relief=relief)
                button.grid(row=row, column=column)
        #button.pack(padx=10, pady=10, fill=tk.X, expand=True)
        # tk.BOTH, tk.NONE
        #button.grid(row=2, column=1)
        #button = tk.Button(text='2', width=10, relief=relief)
        #button.grid(row=1, column=0)
        # columnspan=3
        # sticky=tk.W+tk.E
        #self.rowconfigure(0, pad=3)
        #self.columnconfigure(0, pad=3)
        #def turn_red(self, event):
        #    event.widget["activeforeground"] = "red"
        #self.button.bind("<Enter>", self.turn_red)

class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        self.title('hohoho')
        self['bg'] = 'green'
        # use width x height + x_offset + y_offset (no spaces!)
        #self.geometry("300x150+150+50")
        # or set x, y position only
        #self.geometry("+150+50")
        pad = KeyPad(master=self)
        pad.pack()
        #container = tk.Frame(self)
        #pad = KeyPad(container)
        #pad.pack()
        #pad.pack(padx=5, ipady=5)
        #pad.pack(padx=5, ipady=5)
        #pad = KeyPad(container)
        #pad.pack()

app = MyApp()
app.mainloop()
