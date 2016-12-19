try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk  # Python 2.x

class KeyPad(tk.Frame):
    def __init__(self, *args, **kwargs):
        super(KeyPad, self).__init__(*args, **kwargs)
        # TODO: pass labels in?
        # TODO: label + action
        labels = [['1', '2', '3', 'A'],
                  ['4', '5', '6', 'B'],
                  ['7', '8', '9', 'C'],
                  ['*', '0', '#', 'D']]
        for row, rowlabels in enumerate(labels):
            self.rowconfigure(row, weight=1)
            # pad=...
            for column, label in enumerate(rowlabels):
                if row == 0:
                    self.columnconfigure(column, weight=1)
                button = tk.Button(self, text=label)
                # width=...
                button.grid(row=row, column=column, sticky='nsew')

        #def turn_red(self, event):
        #    event.widget["activeforeground"] = "red"
        #self.button.bind("<Enter>", self.turn_red)

class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        self.title('Key Pad')
        self['bg'] = 'green'
        pad = KeyPad(self)
        pad.pack(fill='both', expand=True)

app = MyApp()
app.mainloop()
