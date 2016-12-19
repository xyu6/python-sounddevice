try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk  # Python 2.x

class KeyPad(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        #self.label = tk.Label(text='Hello, world')
        #self.label.pack(padx=10, pady=10)
        button = tk.Button(text='abc', width=5, relief='ridge',
                           command=lambda: print('haha'))
        #button.pack(padx=10, pady=10, fill=tk.X, expand=True)
        # tk.BOTH, tk.NONE

class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('hohoho')
        self['bg'] = 'green'
        # use width x height + x_offset + y_offset (no spaces!)
        #self.geometry("300x150+150+50")
        # or set x, y position only
        #self.geometry("+150+50")
        #self.memory = 0
        KeyPad(master=self)
        #pad = KeyPad(master=self)
        # pack() seems to be unnecessary?
        #pad.pack(padx=5, ipady=5)

app = MyApp()
app.mainloop()
