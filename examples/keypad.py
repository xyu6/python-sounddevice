try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk  # Python 2.x

class KeyPad(tk.Frame):
    def __init__(self, *args, **kwargs):
        super(KeyPad, self).__init__(*args, **kwargs)
        # TODO: pass labels in?
        # TODO: label + action?
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
                button.bind('<Button-1>', self.mouse_down_event)
                button.bind('<ButtonRelease-1>', self.mouse_up_event)
                button.grid(row=row, column=column, sticky='nsew')

    def activate(self, widget):
        # TODO: get default colors during initialization?
        widget.oldcolor = widget['background']
        widget.oldactivecolor = widget['activebackground']
        widget['background'] = 'red'
        widget['activebackground'] = 'red'

    def deactivate(self, widget):
        widget['background'] = widget.oldcolor
        widget['activebackground'] = widget.oldactivecolor

    def key_event(self, event):
        print(event.char)
        # TODO: call mouse_down_event and shortly after, mouse_up_event?

    def mouse_down_event(self, event):
        self.activate(event.widget)

    def mouse_up_event(self, event):
        self.deactivate(event.widget)

class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(MyApp, self).__init__(*args, **kwargs)
        self.title('Key Pad')
        pad = KeyPad(self)
        pad.pack(fill='both', expand=True)
        self.bind('<Key>', pad.key_event)

app = MyApp()
app.mainloop()
