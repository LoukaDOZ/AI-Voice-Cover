class Event():
    def __init__(self):
        self.__listeners = []
    
    def add_listener(self, listener):
        self.__listeners.append(listener)
    
    def remove_listener(self, listener):
        self.__listeners.remove(listener)
    
    def invoke(self, *args):
        for l in self.__listeners:
            l(args)