class Enstaller4rcError(Exception):
    pass


class InvalidSyntax(Enstaller4rcError):
    def __init__(self, message, lineno=None, col_offset=None):
        self.message = message
        self.lineno = lineno
        self.col_offset = col_offset

    def __str__(self):
        return self.message
