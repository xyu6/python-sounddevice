#!/usr/bin/env python3
"""Simple GUI for recording into a WAV file.

There are 3 concurrent activities: GUI, audio callback, file-writing thread

Neither the GUI nor the audio callback is supposed to block.
Blocking in any of the GUI functions could make the GUI "freeze", blocking in
the audio callback could lead to drop-outs in the recording.
Blocking the file-writing thread for some time is no problem, as long as the
recording can be stopped successfully when it is supposed to.

"""
import queue
import sys
import tempfile
import threading
import tkinter as tk
from tkinter import ttk

import numpy as np
import sounddevice as sd
import soundfile as sf


def file_writing_thread(*, q, **soundfile_args):
    """Write data from queue to file until *None* is recieved."""
    # NB: If you want fine-grained control about the buffering of the file, you
    #     can use Python's open() function (with the "buffering" argument) and
    #     pass the resulting file object to sf.SoundFile().
    with sf.SoundFile(**soundfile_args) as f:
        while True:
            data = q.get()
            if data is None:
                break
            f.write(data)


class RecGui(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.title('Recording GUI')

        # We try to open a stream with default settings first, if that doesn't
        # work, the user can manually change the device(s)

        self.rec_button = ttk.Button()
        self.rec_button.pack()

        self.settings_button = ttk.Button(
            text='device settings', command=self.on_settings)
        # TODO: both buttons in a row, some margin
        self.settings_button.pack()

        self.file_label = ttk.Label(text='<file name>')
        self.file_label.pack()

        # TODO: meters?

        self.status_label = ttk.Label(text='input overflows: 0')
        # TODO: left-align?
        self.status_label.pack()

        self.meter = ttk.Progressbar()
        self.meter['orient'] = 'horizontal'
        self.meter['mode'] = 'determinate'
        self.meter['maximum'] = 100
        self.meter['value'] = 25
        self.meter.pack(fill='x')

        self.stream = sd.InputStream(channels=1, callback=self.callback)
        # TODO: try/catch around stream creation
        self.samplerate = int(self.stream.samplerate)
        self.channels = 1
        self.stream.start()
        # TODO: re-usable method for stream creation?

        self.recording = self._previously_recording = False
        self.audio_q = queue.Queue()
        self.status_q = queue.Queue(maxsize=1)

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
        self.thread = threading.Thread(
            target=file_writing_thread,
            kwargs=dict(
                file=filename,
                mode='x',
                samplerate=self.samplerate,
                channels=self.channels,
                q=self.audio_q,
            ),
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
