#!/usr/bin/env python3

import sys
import tkinter as tk
from tkinter import ttk

# TODO: import numpy?
import sounddevice as sd


class RecGui(tk.Tk):
    """
    """

    def __init__(self):
        tk.Tk.__init__(self)

        self.title('Recording GUI')
        # We try to open a stream with default settings first, if that doesn't
        # work, the user can manually change the device(s)

        # TODO: raw stream?
        self.stream = sd.InputStream(callback=self.callback)
        # TODO: try/catch around stream creation
        # TODO: if Stream doesn't work try InputStream?
        # TODO: re-usable method for stream creation?

        self.rec_button = ttk.Button(text='rec', command=self.on_rec_button)
        self.rec_button.pack()

        # TODO: change button to "stop" when pressed

        # TODO: red button, blinking?

        # TODO: open file already?

        self.file_label = ttk.Label(text='<file name>')
        self.file_label.pack()

        # TODO: meters?

        # TODO: show xruns?

        # TODO: start stream 
        # TODO: activate rec button if stream is available


    # TODO: GUI for selecting device and WAV subtype
    # TODO: button for device settings (channels=1? channel selection?)
    #       List with radio buttons (or drop-down?) for device selection
    #       List with checkboxes for channel selection (+ (un)select all)
    #       scrollable!
    #       available sample rates?

    def callback(self, indata, outdata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        # TODO: thread-safe check for button states!
        # TODO: check if recording, if yes put data into queue
        #q.put(indata.copy())
        # TODO: check if playing back, if yes read from buffer (or queue?)

    # TODO: def start_recording(self):
    # TODO: is file already open?

    # TODO: def stop_recording(self):
    # TODO: close file

    def on_rec_button(self, *args):
        print('rec button:', args)
        # TODO: open/close file?
        # TODO: set recording state
        if recording:
            # TODO: stop recording
            # TODO: change button text (and style?)
        else:
            # TODO: start recording
            # TODO: change button text (and style?)
            # TODO: create file writing thread
            # NB: file creation might fail
            #filename = tempfile.mktemp(prefix='rec_gui_',
            #                            suffix='.wav', dir='')




def main():
    app = RecGui()
    app.mainloop()


if __name__ == '__main__':
    main()
