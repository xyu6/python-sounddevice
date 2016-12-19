import tkinter as tk

class SampleApp(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.label = tk.Label(text="Hello, world")
        self.label.pack(padx=10, pady=10)

app = SampleApp()
app.mainloop()
