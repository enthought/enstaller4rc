import ast
import os.path

import six

from six.moves import urllib

from .errors import InvalidSyntax
from ._platform import ARCH, CUSTOM_PLAT, SUBDIR


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
    if isinstance(file_or_filename, six.string_types):
        with open(file_or_filename) as fp:
            return _AssignmentParser().parse(fp.read())
    else:
        return _AssignmentParser().parse(file_or_filename.read())


def cleanup_url(url):
    """
    Ensure a given repo string, i.e. a string specifying a repository,
    is valid and return a cleaned up version of the string.
    """
    p = urllib.parse.urlparse(url)
    scheme, netloc, path, params, query, fragment = p[:6]

    if scheme == "":
        scheme = "file"

    if scheme == "file":
        netloc = os.path.expanduser(netloc)
        path = os.path.expanduser(path)

    if scheme in ('http', 'https', 'file'):
        if not path.endswith('/'):
            path += '/'
    else:
        raise ValueError("Unsupported scheme: {0!r}".format(url))

    return urllib.parse.urlunparse((scheme, netloc, path, params, query, fragment))


def fill_template_path(path):
    path = path.replace('{ARCH}', ARCH)
    path = path.replace('{SUBDIR}', SUBDIR)
    path = path.replace('{PLATFORM}', CUSTOM_PLAT)
    return path


def fill_url(url):
    url = fill_template_path(url)
    return cleanup_url(url)
