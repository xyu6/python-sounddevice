class TkFrame(object):
    def __init__(self):
        print('I am TkFrame')

#class TkLabelFrame(TkFrame):
class TkLabelFrame(object):
    def __init__(self, text='nothing'):
        print('I am TkLabelFrame:', text)
        super().__init__()

class TkLabelFrameAdapter(TkLabelFrame, TkFrame):
    pass

class MyFrame(TkFrame):
    def __init__(self, *args, **kwargs):
        super(MyFrame, self).__init__(*args, **kwargs)

#class MyBetterFrame(MyFrame, TkLabelFrameAdapter):
class MyBetterFrame(TkLabelFrame, MyFrame):
    pass

MyFrame()
MyBetterFrame()
MyBetterFrame(text='haha')

import collections

class MyFrame2(TkFrame):
    pass

class MyBetterFrame2(MyFrame2, collections.OrderedDict):
    pass
