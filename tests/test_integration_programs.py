import io
import unittest
from contextlib import redirect_stdout

from aevy.interpreter import Interpreter
from aevy.lexer import Lexer
from aevy.parser import Parser


class AevyIntegrationProgramTests(unittest.TestCase):
    def test_function_list_dictionary_and_loop_work_together(self):
        source = '''func total(values) {
    result = 0
    for value in values:
        result = result + value
    return result
}

scores = [10, 20, 30]
profile = {"name": "Alex", "scores": scores}
append(profile["scores"], 40)
show(profile["name"])
show(total(profile["scores"]))
show(has_key(profile, "scores"))
'''
        output = io.StringIO()
        with redirect_stdout(output):
            program = Parser(Lexer(source).scan_tokens()).parse()
            Interpreter(source=source).interpret(program)
        self.assertEqual(output.getvalue().splitlines(), ["Alex", "100", "True"])

    def test_input_conversion_and_dictionary_work_together(self):
        source = '''name = give.input("Name: ")
age = number(give.input("Age: "))
profile = {"name": name, "age": age}
show(profile["name"])
show(profile["age"] + 1)
'''
        inputs = iter(["Sam", "19"])
        output = io.StringIO()
        with redirect_stdout(output):
            program = Parser(Lexer(source).scan_tokens()).parse()
            Interpreter(source=source, input_func=lambda prompt="": next(inputs)).interpret(program)
        self.assertEqual(output.getvalue().splitlines(), ["Sam", "20"])


if __name__ == "__main__":
    unittest.main()
