import sys
from tkinter import *
from tkinter.ttk import *
import tkinter as tk

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
                button = tk.Button(text=label, width=1, relief=relief)
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
def main():
    app = Tk()
    pw = PanedWindow(app, orient='vertical')
    paneA = LabelFrame(pw, text="Pane A", height=240, width=320)
    paneB = LabelFrame(pw, text="Pane B", height=240, width=320)
    #KeyPad(paneB)
    #paneB = KeyPad(pw)
    pw.add(paneA, weight=50)
    pw.add(paneB, weight=50)
    pw.pack(fill='both', expand=True)
    app.mainloop()

if __name__=='__main__':
    sys.exit(main())
