from threading import Thread, Event

class JoinNonBlockingThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stop_event = Event()
    
    def start(self):
        super().start()
    
    def run(self):
        self._target(*self._args, *self._kwargs)
        self._stop_event.set()
    
    def join(self):
        if self._stop_event.is_set():
            super().join()
            return True
        
        return False