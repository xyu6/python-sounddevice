#!/usr/bin/env python3

import queue
import sys
import tempfile
import threading
import tkinter as tk
from tkinter import ttk

import numpy as np
import sounddevice as sd
import soundfile as sf


class FileWritingThread(threading.Thread):

    def __init__(self, *, q, **soundfile_args):
        super().__init__()
        self.soundfile_args = soundfile_args
        self.q = q

    def run(self):
        with sf.SoundFile(**self.soundfile_args) as f:
            while True:
                data = self.q.get()
                if data is None:
                    break
                f.write(data)


class RecGui(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.title('Recording GUI')

        self.recording = self._previously_recording = False

        # We try to open a stream with default settings first, if that doesn't
        # work, the user can manually change the device(s)

        self.rec_button = ttk.Button()
        self.rec_button.pack()

        # TODO: bright red button, blinking?

        self.settings_button = ttk.Button(
            text='device settings', command=self.on_settings)
        # TODO: both buttons in a row
        self.settings_button.pack()

        self.file_label = ttk.Label(text='<file name>')
        self.file_label.pack()

        # TODO: meters?

        # TODO: show xruns?

        self.stream = sd.InputStream(channels=1, callback=self.callback)
        # TODO: try/catch around stream creation
        self.samplerate = int(self.stream.samplerate)
        self.channels = 1
        self.stream.start()
        # TODO: re-usable method for stream creation?

        self.thread = None
        self.audio_q = queue.Queue()

        self.init_buttons()
        self.protocol('WM_DELETE_WINDOW', self.close_window)

    # TODO: GUI for selecting device and WAV subtype
    # TODO: channels=1? channel selection?
    #       List with radio buttons (or drop-down?) for device selection
    #       List with checkboxes for channel selection (+ (un)select all)
    #       scrollable!
    #       available sample rates?

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            # TODO: accumulate numbers and show in GUI?
            print(status, file=sys.stderr)
        # NB: self.recording is accessed from different threads.
        #     This is safe because here we are only accessing it once (with a
        #     single bytecode instruction).
        if self.recording:
            self.audio_q.put(indata.copy())
            self._previously_recording = True
        else:
            if self._previously_recording:
                self.audio_q.put(None)
                self._previously_recording = False

        # TODO: get RMS (or peak?) value, put it in 1-element queue

    def on_rec(self):
        self.settings_button['state'] = 'disabled'
        self.recording = True

        filename = tempfile.mktemp(
            prefix='delme_rec_gui_', suffix='.wav', dir='')

        if self.audio_q.qsize() != 0:
            print('WARNING: Queue not empty!')
        self.thread = FileWritingThread(
            file=filename,
            mode='x',
            samplerate=self.samplerate,
            channels=self.channels,
            q=self.audio_q,
        )
        self.thread.start()

        # NB: File creation might fail!  For brevity, we don't check for this.

        self.rec_button['text'] = 'stop'
        self.rec_button['command'] = self.on_stop
        self.rec_button['state'] = 'normal'
        # TODO: change button style?
        self.file_label['text'] = filename

    def on_stop(self, *args):
        self.rec_button['state'] = 'disabled'
        self.recording = False
        self.wait_for_thread()

    def wait_for_thread(self):
        # NB: Waiting time could be calculated based on stream.latency
        self.after(10, self._wait_for_thread)

    def _wait_for_thread(self):
        if self.thread.is_alive():
            self.wait_for_thread()
            return
        self.thread.join()
        self.init_buttons()

    def on_settings(self, *args):
        print('settings not yet implemented')

    def init_buttons(self):
        self.rec_button['text'] = 'rec'
        self.rec_button['command'] = self.on_rec
        # TODO: set button style?
        if self.stream:
            self.rec_button['state'] = 'normal'
        self.settings_button['state'] = 'normal'

    def close_window(self):
        if self.recording:
            self.on_stop()
        self.destroy()


def main():
    app = RecGui()
    app.mainloop()


if __name__ == '__main__':
    main()
