# -*- coding: utf-8 -*-

"""Test the docdata parser."""

import unittest

from docdata import docdata, parse_docdata
from docdata.api import _strip_trailing_lines


class TestUtils(unittest.TestCase):
    """Test utilities."""

    def test_strip_trailing_lines(self):
        """Test stripping trailing lines."""
        for expected, actual in [
            ([], []),
            (['hello'], ['hello']),
            (['hello'], ['hello', '']),
            (['hello'], ['hello', '', '']),
            (['hello', '', 'goodbye'], ['hello', '', 'goodbye']),
            (['hello', '', 'goodbye'], ['hello', '', 'goodbye', '']),
            (['hello', '', 'goodbye'], ['hello', '', 'goodbye', '', '']),
        ]:
            with self.subTest(value=actual):
                self.assertEqual(expected, _strip_trailing_lines(actual))


class B:
    """This class has a docdata."""


class D:
    """This class has a docdata.

    :param args: Nope.
    """

    def __init__(self, *args):
        """Initialize the class with dummy args."""
        self.args = args


class TestParse(unittest.TestCase):
    """Test parsing docdata."""

    def _help(self, a, b):
        self.assertEqual(a.__doc__, b.__doc__)
        self.assertIsNone(docdata(b))
        self.assertEqual({'name': 'A'}, docdata(a))

    def test_parse_no_params_no_newline(self):
        """Test parsing docdata with no params, and no trailing space.."""

        @parse_docdata
        class A:
            """This class has a docdata.
            ---
            name: A
            """  # noqa: D205

        self._help(A, B)

    def test_parse_no_params_one_newline(self):
        """Test parsing docdata with no params, and a newline before the delimiter."""

        @parse_docdata
        class A:
            """This class has a docdata.

            ---
            name: A
            """

        self._help(A, B)

    def test_parse_no_params_many_newline(self):
        """Test parsing docdata with no params, and a newline before the delimiter."""

        @parse_docdata
        class A:
            """This class has a docdata.



            ---
            name: A
            """  # noqa: D205

        self._help(A, B)

    def test_parse_with_params_no_newline(self):
        """Test parsing docdata."""

        @parse_docdata
        class C:
            """This class has a docdata.

            :param args: Nope.
            ---
            name: A
            """

            def __init__(self, *args):
                """Initialize the class with dummy args."""
                self.args = args

        self._help(C, D)

    def test_parse_with_params_one_newline(self):
        """Test parsing docdata."""

        @parse_docdata
        class C:
            """This class has a docdata.

            :param args: Nope.

            ---
            name: A
            """

            def __init__(self, *args):
                """Initialize the class with dummy args."""
                self.args = args

        self._help(C, D)

    def test_parse_with_params_many_newline(self):
        """Test parsing docdata."""

        @parse_docdata
        class C:
            """This class has a docdata.

            :param args: Nope.



            ---
            name: A
            """

            def __init__(self, *args):
                """Initialize the class with dummy args."""
                self.args = args

        self._help(C, D)
