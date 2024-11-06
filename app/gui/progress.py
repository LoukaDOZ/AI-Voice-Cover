class ProgressManager():
    def __init__(self, limit = 1):
        self.__current = 0
        self.__limit = limit
    
    def reset(self, start = 0, limit = 1):
        self.__current = start
        self.__limit = limit
    
    def step(self, step = 1):
        self.__current += step
    
    def get(self):
        return int(self.__current / self.__limit * 100)
    
    def info(self):
        return str(self.__current) + " / " + str(self.__limit) + " = " + str(self.get())