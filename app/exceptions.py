
class ValidError(Exception):
    def __init__(self,  Errors):
        Exception.__init__(self)
        self.Errors = Errors

