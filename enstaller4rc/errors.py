#------------------------------------------------------------------------------
#
#  Copyright (c) 2016, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#------------------------------------------------------------------------------
class Enstaller4rcError(Exception):
    pass


class InvalidSyntax(Enstaller4rcError):
    def __init__(self, message, lineno=None, col_offset=None):
        self.message = message
        self.lineno = lineno
        self.col_offset = col_offset

    def __str__(self):
        return self.message
