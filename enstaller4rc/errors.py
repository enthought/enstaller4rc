class Enstaller4rcException(Exception):
    pass


class InvalidSyntax(Enstaller4rcException):
    def __init__(self, message, lineno=None, col_offset=None):
        self.message = message
        self.lineno = lineno
        self.col_offset = col_offset

    def __str__(self):
        return self.message
