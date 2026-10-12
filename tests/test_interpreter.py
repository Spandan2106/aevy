import contextlib
import io
import unittest
from src.aevy.lexer import Lexer
from src.aevy.parser import Parser
from src.aevy.interpreter import Interpreter

def run_aevy(source):
    program = Parser(Lexer(source).scan_tokens()).parse()
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        Interpreter().interpret(program)
    return output.getvalue().strip().splitlines()

class AevyInterpreterTests(unittest.TestCase):
    def test_arithmetic(self):
        self.assertEqual(run_aevy("x = 10 + 5 * 2\nshow(x)\n"), ["20"])

    def test_function_return(self):
        self.assertEqual(run_aevy("func add(a, b) {\n    return a + b\n}\nshow(add(7, 8))\n"), ["15"])

    def test_recursion(self):
        self.assertEqual(run_aevy("func factorial(n) {\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n}\nshow(factorial(5))\n"), ["120"])

    def test_for_range_end_exclusive(self):
        self.assertEqual(run_aevy("for i in 1..4:\n    show(i)\n"), ["1", "2", "3"])

    def test_polymorphism(self):
        source = '''class Animal {
    func speak() {
        show("Animal")
    }
}
class Dog extends Animal {
    func speak() {
        show("Woof")
    }
}
func make_sound(animal) {
    animal.speak()
}
make_sound(Dog())
make_sound(Animal())
'''
        self.assertEqual(run_aevy(source), ["Woof", "Animal"])

    def test_super_method(self):
        source = '''class Animal {
    func speak() {
        show("Animal")
    }
}
class Dog extends Animal {
    func speak() {
        super.speak()
        show("Dog")
    }
}
Dog().speak()
'''
        self.assertEqual(run_aevy(source), ["Animal", "Dog"])

    def test_private_attribute_allowed_inside_class(self):
        source = '''class Account {
    func init(balance) {
        self._balance = balance
    }
    func get_balance() {
        return self._balance
    }
}
account = Account(125)
show(account.get_balance())
'''
        self.assertEqual(run_aevy(source), ["125"])

    def test_private_attribute_read_denied_outside(self):
        source = '''class Account {
    func init(balance) {
        self._balance = balance
    }
}
account = Account(125)
show(account._balance)
'''
        with self.assertRaises(PermissionError):
            run_aevy(source)

    def test_private_attribute_assignment_denied_outside(self):
        source = '''class Account {
    func init(balance) {
        self._balance = balance
    }
}
account = Account(125)
account._balance = 0
'''
        with self.assertRaises(PermissionError):
            run_aevy(source)

    def test_public_attribute(self):
        source = '''class Box {
    func init(value) {
        self.value = value
    }
}
box = Box(42)
show(box.value)
box.value = 9
show(box.value)
'''
        self.assertEqual(run_aevy(source), ["42", "9"])

    def test_undefined_variable_error(self):
        with self.assertRaises(NameError):
            run_aevy("show(missing)\n")

if __name__ == "__main__":
    unittest.main()
