import io
import unittest
from contextlib import redirect_stdout

from aevy.interpreter import Interpreter
from aevy.lexer import Lexer
from aevy.parser import Parser


def execute(source):
    output = io.StringIO()
    with redirect_stdout(output):
        program = Parser(Lexer(source).scan_tokens()).parse()
        Interpreter(source=source).interpret(program)
    return output.getvalue().splitlines()


class AevyDictionaryTests(unittest.TestCase):
    def test_literal_and_key_access(self):
        self.assertEqual(execute('person = {"name": "Alex", "age": 20}\nshow(person["name"])'), ["Alex"])

    def test_empty_dictionary(self):
        self.assertEqual(execute('data = {}\nshow(length(data))'), ["0"])

    def test_assignment_adds_or_updates_key(self):
        self.assertEqual(execute('d = {"x": 1}\nd["x"] = 2\nd["y"] = 3\nshow(d["x"])\nshow(d["y"])'), ["2", "3"])

    def test_nested_dictionary(self):
        self.assertEqual(execute('d = {"user": {"name": "Sam"}}\nshow(d["user"]["name"])'), ["Sam"])

    def test_iteration_yields_keys(self):
        self.assertEqual(execute('d = {"a": 1, "b": 2}\nfor key in d:\n    show(key)'), ["a", "b"])

    def test_keys_and_values(self):
        self.assertEqual(execute('d = {"a": 1, "b": 2}\nshow(keys(d))\nshow(values(d))'), ["['a', 'b']", "[1, 2]"])

    def test_has_key(self):
        self.assertEqual(execute('d = {"a": 1}\nshow(has_key(d, "a"))\nshow(has_key(d, "b"))'), ["True", "False"])

    def test_remove_key(self):
        self.assertEqual(execute('d = {"a": 1, "b": 2}\nremove_key(d, "a")\nshow(length(d))'), ["1"])

    def test_membership_operator_checks_keys(self):
        self.assertEqual(execute('d = {"a": 1}\nshow("a" in d)\nshow("b" in d)'), ["True", "False"])

    def test_missing_key_raises_clear_error(self):
        with self.assertRaisesRegex(KeyError, "Dictionary key 'missing' was not found"):
            execute('d = {}\nshow(d["missing"])')

    def test_non_dictionary_indexing_is_rejected(self):
        with self.assertRaisesRegex(TypeError, "Indexing requires a list or dictionary"):
            execute('x = 4\nshow(x[0])')

    def test_unhashable_key_is_rejected(self):
        with self.assertRaisesRegex(TypeError, "Dictionary keys must be hashable"):
            execute('d = {[1, 2]: "value"}')

    def test_duplicate_key_uses_last_value(self):
        self.assertEqual(execute('d = {"x": 1, "x": 9}\nshow(d["x"])'), ["9"])


if __name__ == "__main__":
    unittest.main()
