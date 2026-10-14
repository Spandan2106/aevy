import contextlib
import io
import unittest

from src.aevy.interpreter import Interpreter
from src.aevy.lexer import Lexer
from src.aevy.parser import Parser


def run_aevy(source):
    program = Parser(Lexer(source).scan_tokens()).parse()
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        Interpreter(source=source).interpret(program)
    return output.getvalue().strip().splitlines()


class AevyStandardLibraryTests(unittest.TestCase):
    def test_length(self):
        self.assertEqual(run_aevy('show(length("Aevy"))\n'), ["4"])

    def test_upper_and_lower(self):
        self.assertEqual(run_aevy('show(upper("Aevy"))\nshow(lower("HeLLo"))\n'), ["AEVY", "hello"])

    def test_trim(self):
        self.assertEqual(run_aevy('show(trim("  hello  "))\n'), ["hello"])

    def test_contains_true_and_false(self):
        self.assertEqual(run_aevy('show(contains("programming", "gram"))\nshow(contains("Aevy", "xyz"))\n'), ["True", "False"])

    def test_abs(self):
        self.assertEqual(run_aevy('show(abs(-12))\nshow(abs(-2.5))\n'), ["12", "2.5"])

    def test_min_and_max(self):
        self.assertEqual(run_aevy('show(min(7, 2, 9, -1))\nshow(max(7, 2, 9, -1))\n'), ["-1", "9"])

    def test_round_default_and_digits(self):
        self.assertEqual(run_aevy('show(round(3.6))\nshow(round(3.14159, 2))\n'), ["4.0", "3.14"])

    def test_string_builtins_reject_non_text(self):
        with self.assertRaisesRegex(TypeError, "must be text"):
            run_aevy('show(upper(12))\n')

    def test_numeric_builtins_reject_booleans(self):
        with self.assertRaisesRegex(TypeError, "must be a number"):
            run_aevy('show(abs(True))\n')

    def test_min_requires_two_arguments(self):
        with self.assertRaisesRegex(TypeError, "expects at least 2 argument"):
            run_aevy('show(min(5))\n')

    def test_round_digits_must_be_integer(self):
        with self.assertRaisesRegex(TypeError, "argument 2 must be an integer"):
            run_aevy('show(round(3.14, 1.5))\n')


if __name__ == "__main__":
    unittest.main()
