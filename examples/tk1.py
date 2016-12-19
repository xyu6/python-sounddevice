import tkinter as tk

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('huhu')
        self.label = tk.Label(text="Hello, world")
        self.label.pack(padx=10, pady=10)
        tk.Label(text="Another label").pack()

app = SampleApp()
app.mainloop()
