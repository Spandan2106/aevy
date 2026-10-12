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


class AevyEdgeCaseTests(unittest.TestCase):
    def test_break_exits_loop(self):
        source = "for i in 1..6:\n    if i == 4:\n        break\n    show(i)\n"
        self.assertEqual(run_aevy(source), ["1", "2", "3"])

    def test_continue_skips_iteration(self):
        source = "for i in 1..5:\n    if i == 2:\n        continue\n    show(i)\n"
        self.assertEqual(run_aevy(source), ["1", "3", "4"])

    def test_nested_loops_keep_break_local(self):
        source = "for i in 1..4:\n    for j in 1..4:\n        if j == 2:\n            break\n        show(i * 10 + j)\n"
        self.assertEqual(run_aevy(source), ["11", "21", "31"])

    def test_inherited_constructor(self):
        source = '''class Parent {
    func init(value) {
        self.value = value
    }
    func get_value() {
        return self.value
    }
}
class Child extends Parent {
    func extra() {
        show("child")
    }
}
child = Child(27)
show(child.get_value())
child.extra()
'''
        self.assertEqual(run_aevy(source), ["27", "child"])

    def test_multilevel_super_chain(self):
        source = '''class A {
    func speak() {
        show("A")
    }
}
class B extends A {
    func speak() {
        super.speak()
        show("B")
    }
}
class C extends B {
    func speak() {
        super.speak()
        show("C")
    }
}
C().speak()
'''
        self.assertEqual(run_aevy(source), ["A", "B", "C"])

    def test_wrong_function_argument_count(self):
        source = '''func add(a, b) {
    return a + b
}
show(add(1))
'''
        with self.assertRaises(TypeError):
            run_aevy(source)

    def test_undefined_method(self):
        source = '''class Box {
    func init() {
        self.value = 1
    }
}
Box().missing()
'''
        with self.assertRaises(NameError):
            run_aevy(source)

    def test_non_boolean_if_condition(self):
        with self.assertRaises(TypeError):
            run_aevy("if 123:\n    show(1)\n")

    def test_mixed_indentation_is_rejected(self):
        source = "if True:\n    show(1)\n\tshow(2)\n"
        with self.assertRaises(SyntaxError):
            Lexer(source).scan_tokens()

    def test_subclass_cannot_access_parent_private_attribute(self):
        source = '''class Parent {
    func init() {
        self._secret = 7
    }
}
class Child extends Parent {
    func reveal() {
        return self._secret
    }
}
child = Child()
show(child.reveal())
'''
        with self.assertRaises(PermissionError):
            run_aevy(source)

    def test_private_attribute_owner_can_access_it(self):
        source = '''class Parent {
    func init() {
        self._secret = 7
    }
    func reveal() {
        return self._secret
    }
}
class Child extends Parent {
}
child = Child()
show(child.reveal())
'''
        self.assertEqual(run_aevy(source), ["7"])


if __name__ == "__main__":
    unittest.main()
