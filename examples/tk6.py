try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk  # Python 2.x

root = tk.Tk()
fr1 = tk.Frame(root)
fr1.pack()
btn1 = tk.Button(fr1, text='haha')
btn1.pack()
lf = tk.LabelFrame(root, text=' super ')
lf.pack()
fr2 = tk.Frame(lf)
#fr2 = tk.Frame(root)
fr2.pack()
btn2 = tk.Button(fr2, text='hihi')
btn2.grid(row=0, column=0)
btn2a = tk.Button(fr2, text='hoho')
btn2a.grid(row=1, column=1)
root.mainloop()
