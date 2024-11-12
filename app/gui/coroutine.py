import random
import string

class Couroutine():
    instance = None

    def __init__(self, __after_func):
        self.__after = __after_func
        self.__couroutines = {}
    
    def start(self, func, timeout = 1, name = None, args=tuple()):
        name = self.__register__(func, timeout, name, args)
        self.__run__(name)
        return name
    
    def timeout(self, func, timeout = 1, name = None, args=tuple()):
        name = self.__register__(func, timeout, name, args)
        self.__after(timeout, lambda: self.__run_timeout__(name))
        return name
    
    def stop(self, name):
        if name in self.__couroutines:
            self.__couroutines[name]["stop"] = True
    
    def __run__(self, name):
        co = self.__couroutines[name]

        if co["stop"]:
            del co
            return

        co["func"](*co["args"])
        self.__after(co["timeout"], lambda: self.__run__(name))
    
    def __run_timeout__(self, name):
        co = self.__couroutines[name]

        if not co["stop"]:
            co["func"](*co["args"])

        del co
    
    def __register__(self, func, timeout, name, args):
        if name is None:
            name = self.__generate_id__(10)
        elif name in self.__couroutines and not self.__couroutines[name]["stop"]:
            raise Exception(f"An instance of {name} is already running")

        self.__couroutines[name] = {
            "func": func,
            "timeout": timeout,
            "args": args,
            "stop": False
        }

        return name
    
    def __generate_id__(self, n):
        id_ = None

        while(id_ is None or id_ in self.__couroutines):
            id_ = ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
        
        return id_

    @staticmethod
    def init(after_func):
        if Couroutine.instance is not None:
            raise Exception("Already initiated")

        Couroutine.instance = Couroutine(after_func)