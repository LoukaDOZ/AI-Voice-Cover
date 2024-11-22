class Result():
    def __init__(self, default = None):
        self.result = default
    
    def set(self, value):
        self.result = value
    
    def get(self):
        return self.result