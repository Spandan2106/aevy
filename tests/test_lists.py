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


class AevyListTests(unittest.TestCase):
    def test_list_literal_and_indexing(self):
        self.assertEqual(run_aevy('numbers = [10, 20, 30]\nshow(numbers[0])\nshow(numbers[2])\n'), ['10', '30'])

    def test_empty_list(self):
        self.assertEqual(run_aevy('items = []\nshow(length(items))\n'), ['0'])

    def test_nested_lists(self):
        self.assertEqual(run_aevy('grid = [[1, 2], [3, 4]]\nshow(grid[1][0])\n'), ['3'])

    def test_index_assignment(self):
        self.assertEqual(run_aevy('numbers = [1, 2, 3]\nnumbers[1] = 9\nshow(numbers[1])\n'), ['9'])

    def test_list_is_mutable_through_alias(self):
        self.assertEqual(run_aevy('a = [1, 2]\nb = a\nb[0] = 7\nshow(a[0])\n'), ['7'])

    def test_append_mutates_list(self):
        self.assertEqual(run_aevy('items = [1]\nappend(items, 2)\nshow(length(items))\nshow(items[1])\n'), ['2', '2'])

    def test_pop_returns_last_item(self):
        self.assertEqual(run_aevy('items = [4, 8]\nshow(pop(items))\nshow(length(items))\n'), ['8', '1'])

    def test_contains_supports_lists(self):
        self.assertEqual(run_aevy('items = [2, 4, 6]\nshow(contains(items, 4))\nshow(contains(items, 5))\n'), ['True', 'False'])

    def test_index_must_be_integer(self):
        with self.assertRaisesRegex(TypeError, 'index must be an integer'):
            run_aevy('items = [1, 2]\nshow(items[1.5])\n')

    def test_out_of_range_index(self):
        with self.assertRaisesRegex(IndexError, 'out of range'):
            run_aevy('items = [1]\nshow(items[3])\n')

    def test_index_assignment_requires_list(self):
        with self.assertRaisesRegex(TypeError, 'requires a list'):
            run_aevy('value = 3\nvalue[0] = 4\n')

    def test_pop_empty_list_raises_clear_error(self):
        with self.assertRaisesRegex(IndexError, 'empty list'):
            run_aevy('items = []\npop(items)\n')

    def test_length_rejects_unsupported_types(self):
        with self.assertRaisesRegex(TypeError, 'text or a list'):
            run_aevy('show(length(123))\n')


if __name__ == '__main__':
    unittest.main()
