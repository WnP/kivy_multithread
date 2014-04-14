from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from threading import Thread
from time import sleep


class MyThread(Thread):

    def __init__(
            self,
            group=None, target=None, name=None, verbose=None,  # args required by threading.Thread
            *args, **kwargs):

        super(MyThread, self).__init__(
            group=group, target=target, name=name, verbose=verbose)

        # do whatever you want with args list and kwargs dict
        self.args = args
        self.kwargs = kwargs

        # handle the thread process result
        self._result = None
        self._is_finished = False

        # I prefer start threads directly, but that's my choice ;-)
        self.start()

    def run(self):
        print 'long blocking process -lbp- started!'
        sleep(4)
        print 'lbp continue'
        sleep(2)
        self._result = 'a very interresting result'
        self._is_finished = True
        print 'lbp finish'

    @property
    def is_finished(self):
        return self._is_finished

    @property
    def result(self):
        return self._result


class MyWidget(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(MyWidget, self).__init__(*args, **kwargs)
        # threads callbacks instance
        self.curent_threads_cbs = {}

    def start_blocking(self, *args, **kwargs):
        t = MyThread()
        cb = lambda dt: self.thread_callback(t)

        # thread id as dict key
        self.curent_threads_cbs[id(t)] = cb

        Clock.schedule_interval(cb, 0.5)

    def thread_callback(self, thread):
        if thread.is_finished:
            print thread.result
            Clock.unschedule(self.curent_threads_cbs[id(thread)])
        else:
            print 'waiting for result'


class MyApp(App):
    pass

if __name__ == '__main__':
    MyApp().run()
