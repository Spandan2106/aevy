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


class AevyCollectionV2Tests(unittest.TestCase):
    def test_iterate_list(self):
        self.assertEqual(run_aevy('numbers = [10, 20, 30]\nfor item in numbers:\n    show(item)\n'), ['10', '20', '30'])

    def test_iterate_empty_list(self):
        self.assertEqual(run_aevy('items = []\nfor item in items:\n    show(item)\nshow("done")\n'), ['done'])

    def test_list_iteration_continue_and_break(self):
        source = 'numbers = [1, 2, 3, 4]\nfor item in numbers:\n    if item == 2:\n        continue\n    if item == 4:\n        break\n    show(item)\n'
        self.assertEqual(run_aevy(source), ['1', '3'])

    def test_range_loop_still_works(self):
        self.assertEqual(run_aevy('for i in 1..4:\n    show(i)\n'), ['1', '2', '3'])

    def test_insert_at_middle(self):
        self.assertEqual(run_aevy('items = [1, 3]\ninsert(items, 1, 2)\nshow(items[1])\nshow(length(items))\n'), ['2', '3'])

    def test_remove_value(self):
        self.assertEqual(run_aevy('items = [1, 2, 3]\nremove(items, 2)\nshow(length(items))\nshow(contains(items, 2))\n'), ['2', 'False'])

    def test_index_of_found_and_missing(self):
        self.assertEqual(run_aevy('items = [5, 8, 9]\nshow(index_of(items, 8))\nshow(index_of(items, 3))\n'), ['1', '-1'])

    def test_reverse_mutates_and_returns_list(self):
        self.assertEqual(run_aevy('items = [1, 2, 3]\nreverse(items)\nshow(items[0])\nshow(items[2])\n'), ['3', '1'])

    def test_sum_numbers(self):
        self.assertEqual(run_aevy('show(sum([1, 2, 3.5]))\n'), ['6.5'])

    def test_sort_returns_sorted_copy(self):
        self.assertEqual(run_aevy('items = [3, 1, 2]\nsorted_items = sort(items)\nshow(sorted_items[0])\nshow(items[0])\n'), ['1', '3'])

    def test_list_concatenation(self):
        self.assertEqual(run_aevy('items = [1, 2] + [3]\nshow(length(items))\nshow(items[2])\n'), ['3', '3'])

    def test_list_repetition(self):
        self.assertEqual(run_aevy('items = [7] * 3\nshow(length(items))\nshow(items[2])\n'), ['3', '7'])

    def test_list_equality_and_membership_operator(self):
        self.assertEqual(run_aevy('show([1, 2] == [1, 2])\nshow(2 in [1, 2, 3])\nshow(9 in [1, 2, 3])\n'), ['True', 'True', 'False'])

    def test_invalid_list_iteration(self):
        with self.assertRaisesRegex(TypeError, 'iteration requires a list'):
            run_aevy('for item in 123:\n    show(item)\n')

    def test_insert_invalid_index(self):
        with self.assertRaisesRegex(IndexError, 'Insert index'):
            run_aevy('items = [1]\ninsert(items, 3, 2)\n')

    def test_remove_missing_value(self):
        with self.assertRaisesRegex(ValueError, 'was not found'):
            run_aevy('items = [1, 2]\nremove(items, 3)\n')

    def test_sum_rejects_non_numeric_elements(self):
        with self.assertRaisesRegex(TypeError, 'must be a number'):
            run_aevy('show(sum([1, "x"]))\n')

    def test_list_concatenation_requires_two_lists(self):
        with self.assertRaisesRegex(TypeError, 'requires two lists'):
            run_aevy('items = [1] + 2\n')

    def test_list_repetition_requires_non_negative_integer(self):
        with self.assertRaisesRegex(TypeError, 'non-negative integer'):
            run_aevy('items = [1] * -2\n')


if __name__ == '__main__':
    unittest.main()
