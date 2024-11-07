class ProgressManager():
    def __init__(self, limit = 1):
        self.__current = 0
        self.__limit = limit
        self.__label = ""
    
    def reset(self, start = 0, limit = 1):
        self.__current = start
        self.__limit = limit
        self.__label = ""

    def set_label(self, label):
        self.__label = label
    
    def get_label(self):
        return self.__label
    
    def step(self, step = 1, label = None):
        self.__current += step
        self.__label = label if label is not None else self.__label
    
    def get(self):
        return int(self.__current / self.__limit * 100)