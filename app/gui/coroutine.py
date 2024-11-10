class Couroutine():
    instance = None

    def __init__(self, __after_func):
        self.__after = __after_func
        self.__couroutines = {}
    
    def start(self, name, func, timeout = 1, *args):
        if name in self.__couroutines and not self.__couroutines[name]["stop"]:
            raise Exception(f"An instance of {name} is already running")

        self.__couroutines[name] = {
            "func": func,
            "timeout": timeout,
            "args": args,
            "stop": False
        }
        self.__run__(name)
    
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

    @staticmethod
    def init(after_func):
        if Couroutine.instance is not None:
            raise Exception("Already initiated")

        Couroutine.instance = Couroutine(after_func)