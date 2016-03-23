import textwrap
import unittest

from ..errors import InvalidSyntax
from ..utils import StringIO, parse_assignments


class TestParseAssignments(unittest.TestCase):
    def test_parse_simple(self):
        # Given
        r_data = {
            "IndexedRepos": ["http://acme.com/{SUBDIR}"],
            "webservice_entry_point": "http://acme.com/eggs/{PLATFORM}/"
        }

        s = textwrap.dedent("""\
        IndexedRepos = [
            "http://acme.com/{SUBDIR}",
        ]
        webservice_entry_point = "http://acme.com/eggs/{PLATFORM}/"
        """)

        # When
        data = parse_assignments(StringIO(s))

        # Then
        self.assertEqual(data, r_data)

    def test_parse_simple_invalid_file(self):
        with self.assertRaises(InvalidSyntax):
            parse_assignments(StringIO("EPD_auth += 2"))

        with self.assertRaises(InvalidSyntax):
            parse_assignments(StringIO("1 + 2"))
