import contextlib
import io
import unittest

from src.aevy.interpreter import Interpreter
from src.aevy.lexer import Lexer
from src.aevy.parser import Parser


def run_aevy(source, input_func=None):
    program = Parser(Lexer(source).scan_tokens()).parse()
    output = io.StringIO()
    interpreter = Interpreter(input_func=input_func or input)
    with contextlib.redirect_stdout(output):
        interpreter.interpret(program)
    return output.getvalue().strip().splitlines()


class AevyInputConversionTests(unittest.TestCase):
    def test_input_with_prompt_and_text_conversion(self):
        prompts = []
        def fake_input(prompt):
            prompts.append(prompt)
            return "Ada"
        result = run_aevy('name = give.input("Name? ")\nshow(text(name))\n', fake_input)
        self.assertEqual(result, ["Ada"])
        self.assertEqual(prompts, ["Name? "])

    def test_input_without_prompt(self):
        prompts = []
        def fake_input(prompt):
            prompts.append(prompt)
            return "hello"
        self.assertEqual(run_aevy('show(give.input())\n', fake_input), ["hello"])
        self.assertEqual(prompts, [""])

    def test_number_converts_integer_string(self):
        self.assertEqual(run_aevy('age = number("21")\nshow(age + 1)\n'), ["22"])

    def test_number_converts_decimal_string(self):
        self.assertEqual(run_aevy('show(number("2.5") + 1)\n'), ["3.5"])

    def test_integer_conversion(self):
        self.assertEqual(run_aevy('show(integer("12"))\n'), ["12"])

    def test_decimal_conversion(self):
        self.assertEqual(run_aevy('show(decimal("2.25"))\n'), ["2.25"])

    def test_boolean_conversion(self):
        self.assertEqual(run_aevy('show(boolean("TrUe"))\nshow(boolean("false"))\n'), ["True", "False"])

    def test_invalid_boolean_conversion(self):
        with self.assertRaisesRegex(ValueError, "expected True or False"):
            run_aevy('show(boolean("yes"))\n')

    def test_invalid_number_conversion(self):
        with self.assertRaises(ValueError):
            run_aevy('show(number("hello"))\n')

    def test_conversion_requires_one_argument(self):
        with self.assertRaisesRegex(TypeError, "expects exactly 1 argument"):
            run_aevy('show(number())\n')

    def test_input_rejects_multiple_arguments(self):
        with self.assertRaisesRegex(TypeError, "expects 0 or 1 argument"):
            run_aevy('show(give.input("a", "b"))\n')

    def test_text_conversion_of_boolean(self):
        self.assertEqual(run_aevy('show(text(True))\nshow(text(False))\n'), ["True", "False"])


if __name__ == "__main__":
    unittest.main()
