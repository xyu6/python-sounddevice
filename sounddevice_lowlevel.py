# Copyright (c) 2015-2018 Matthias Geier
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from ctypes.util import find_library as _find_library
import os as _os
import platform as _platform

from _sounddevice import ffi as _ffi

try:
    _basestring = basestring
except NameError:
    _basestring = str, bytes


class PortAudio(object):

    initialized = 0

    def __init__(self, libname=None):
        #if libname:
        #    self.libname = libname
        #    # TODO: implement this
        try:
            for self.libname in (
                    'portaudio',  # Default name on POSIX systems
                    'bin\\libportaudio-2.dll',  # DLL from conda-forge
                    'lib/libportaudio.dylib',  # dylib from anaconda
                    ):
                self.libname = _find_library(self.libname)
                if self.libname is not None:
                    break
            else:
                raise OSError('PortAudio library not found')
            self._lib = _ffi.dlopen(self.libname)
        except OSError:
            if _platform.system() == 'Darwin':
                self.libname = 'libportaudio.dylib'
            elif _platform.system() == 'Windows':
                self.libname = 'libportaudio{0}.dll'.format(
                    _platform.architecture()[0])
            else:
                raise
            import _sounddevice_data
            self.libname = _os.path.join(
                next(iter(_sounddevice_data.__path__)), 'portaudio-binaries',
                self.libname)
            self._lib = _ffi.dlopen(self.libname)

        self.sampleformats = {
            'float32': self._lib.paFloat32,
            'int32': self._lib.paInt32,
            'int24': self._lib.paInt24,
            'int16': self._lib.paInt16,
            'int8': self._lib.paInt8,
            'uint8': self._lib.paUInt8,
        }
        self.initialize()

        pa = self

        class MyOtherStream(_MyStream):

            def __init__(self):
                _MyStream.__init__(self, lib=pa._lib)

        self.MyOtherStream = MyOtherStream

    def initialize(self):
        self.check(self._lib.Pa_Initialize(), 'Error initializing PortAudio')
        self.initialized += 1

    def terminate(self):
        self.check(self._lib.Pa_Terminate(), 'Error terminating PortAudio')
        self.initialized -= 1

    def check(self, err, msg=''):
        """Raise PortAudioError for below-zero error codes."""
        if err >= 0:
            return err

        errormsg = _ffi.string(self._lib.Pa_GetErrorText(err)).decode()
        if msg:
            errormsg = "{0}: {1}".format(msg, errormsg)

        if err == self._lib.paUnanticipatedHostError:
            # (gh82) We grab the host error info here rather than inside
            # PortAudioError since check() should only ever be called after a
            # failing API function call. This way we can avoid any potential issues
            # in scenarios where multiple APIs are being used simultaneously.
            info = self._lib.Pa_GetLastHostErrorInfo()
            host_api = self._lib.Pa_HostApiTypeIdToHostApiIndex(info.hostApiType)
            hosterror_text = _ffi.string(info.errorText).decode()
            hosterror_info = host_api, info.errorCode, hosterror_text
            raise PortAudioError(errormsg, err, hosterror_info)

        raise PortAudioError(errormsg, err)

    def MyStream(self, *args, **kwargs):
        return _MyStream(*args, lib=self._lib, **kwargs)


class _MyStream(object):

    def __init__(self, lib):
        self._lib = lib

    def device_count(self):
        return self._lib.Pa_GetDeviceCount()


class PortAudioError(Exception):
    """This exception will be raised on PortAudio errors.

    Attributes
    ----------
    args
        A variable length tuple containing the following elements when
        available:

        1) A string describing the error
        2) The PortAudio ``PaErrorCode`` value
        3) A 3-tuple containing the host API index, host error code, and the
           host error message (which may be an empty string)

    """

    def __str__(self):
        errormsg = self.args[0] if self.args else ''
        if len(self.args) > 1:
            errormsg = "{0} [PaErrorCode {1}]".format(errormsg, self.args[1])
        if len(self.args) > 2:
            host_api, hosterror_code, hosterror_text = self.args[2]
            hostname = query_hostapis(host_api)['name']
            errormsg = "{0}: '{1}' [{2} error {3}]".format(
                errormsg, hosterror_text, hostname, hosterror_code)

        return errormsg




def ignore_stderr():
    """Try to forward PortAudio messages from stderr to /dev/null."""
    try:
        stdio = _ffi.dlopen(None)
        devnull = stdio.fopen(_os.devnull.encode(), b'w')
    except (OSError, AttributeError):
        return
    try:
        stdio.stderr = devnull
    except _ffi.error:
        try:
            stdio.__stderrp = devnull
        except _ffi.error:
            stdio.fclose(devnull)
