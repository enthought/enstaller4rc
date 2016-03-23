import ast
import sys

from .errors import InvalidSyntax


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


if PY2:
    string_types = (basestring,)
    import StringIO
    StringIO = StringIO.StringIO
else:
    string_types = (str,)
    StringIO = io.StringIO


class _AssignmentParser(ast.NodeVisitor):
    def __init__(self):
        self._data = {}

    def parse(self, s):
        self._data.clear()

        root = ast.parse(s)
        self.visit(root)
        return self._data

    def generic_visit(self, node):
        if type(node) != ast.Module:
            raise InvalidSyntax(
                "Unexpected expression @ line {0}".format(node.lineno), node.lineno
            )
        super(_AssignmentParser, self).generic_visit(node)

    def visit_Assign(self, node):
        try:
            value = ast.literal_eval(node.value)
        except ValueError:
            msg = "Invalid configuration syntax at line {0}".format(node.lineno)
            raise InvalidSyntax(msg, node.lineno)
        else:
            for target in node.targets:
                self._data[target.id] = value


def parse_assignments(file_or_filename):
    """
    Parse files which contain only python assignements, and returns the
    corresponding dictionary name: value

    Parameters
    ----------
    file_or_filename: str, file object
        If a string, interpreted as a filename. File object otherwise.
    """
    if isinstance(file_or_filename, string_types):
        with open(file_or_filename) as fp:
            return _AssignmentParser().parse(fp.read())
    else:
        return _AssignmentParser().parse(file_or_filename.read())
