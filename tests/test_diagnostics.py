import unittest

from src.aevy.diagnostics import format_error
from src.aevy.lexer import Lexer
from src.aevy.parser import Parser
from src.aevy.interpreter import Interpreter


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

    def test_runtime_error_has_expression_location(self):
        source = "x = 10\ny = 0\nshow(x / y)\n"
        program = Parser(Lexer(source).scan_tokens()).parse()
        with self.assertRaises(ZeroDivisionError) as caught:
            Interpreter(source=source).interpret(program)
        self.assertEqual(caught.exception.aevy_line, 3)
        self.assertEqual(caught.exception.aevy_column, 8)

    def test_formatter_shows_source_line_and_caret(self):
        source = "x = 10\ny = 0\nshow(x / y)\n"
        program = Parser(Lexer(source).scan_tokens()).parse()
        with self.assertRaises(ZeroDivisionError) as caught:
            Interpreter(source=source).interpret(program)
        rendered = format_error(caught.exception, source)
        self.assertIn("Arithmetic error: Division by zero", rendered)
        self.assertIn("at line 3, column 8", rendered)
        self.assertIn("show(x / y)", rendered)
        self.assertIn("         ^", rendered)

    def test_undefined_variable_has_exact_location(self):
        source = "show(missing)\n"
        program = Parser(Lexer(source).scan_tokens()).parse()
        with self.assertRaises(NameError) as caught:
            Interpreter(source=source).interpret(program)
        self.assertEqual(caught.exception.aevy_line, 1)
        self.assertEqual(caught.exception.aevy_column, 6)


if __name__ == "__main__":
    unittest.main()
