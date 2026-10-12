import unittest

from src.aevy.diagnostics import format_error
from src.aevy.lexer import Lexer
from src.aevy.parser import Parser


class AevyDiagnosticTests(unittest.TestCase):
    def test_unexpected_character_has_location(self):
        with self.assertRaisesRegex(SyntaxError, r"line 1, column 9"):
            Lexer("show(1) @").scan_tokens()

    def test_unterminated_string_has_line_and_column(self):
        with self.assertRaisesRegex(SyntaxError, r"line 2, column 6"):
            Lexer('show(1)' + chr(10) + 'show("oops)').scan_tokens()

    def test_parser_error_has_location(self):
        tokens = Lexer("show(1 2)\n").scan_tokens()
        with self.assertRaisesRegex(SyntaxError, r"line 1, column 8"):
            Parser(tokens).parse()

    def test_error_formatter_labels_common_errors(self):
        self.assertEqual(
            format_error(NameError("Undefined variable 'x'")),
            "Name error: Undefined variable 'x'",
        )
        self.assertEqual(
            format_error(PermissionError("Private attribute")),
            "Access error: Private attribute",
        )


if __name__ == "__main__":
    unittest.main()
