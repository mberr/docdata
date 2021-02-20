# -*- coding: utf-8 -*-

"""Test the docdata parser."""

import unittest

from docdata import docdata, parse_docdata


class TestParse(unittest.TestCase):
    """Test parsing docdata."""

    def _help(self, a, b):
        self.assertEqual(a.__doc__, b.__doc__)
        self.assertIsNone(docdata(b))
        self.assertEqual({'name': 'A'}, docdata(a))

    def test_parse_no_params(self):
        """Test parsing docdata."""

        @parse_docdata
        class A:
            """This class has a docdata.

            ---
            name: A
            """

        class B:
            """This class has a docdata."""

        self._help(A, B)

    def test_parse_with_params(self):
        """Test parsing docdata."""

        @parse_docdata
        class A:
            """This class has a docdata.

            :param args: Nope.
            ---
            name: A
            """

            def __init__(self, *args):
                self.args = args

        class B:
            """This class has a docdata.

            :param args: Nope.
            """

            def __init__(self, *args):
                self.args = args

        self._help(A, B)
