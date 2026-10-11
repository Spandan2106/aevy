from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter


def run(source):
    tokens = Lexer(source).scan_tokens()
    program = Parser(tokens).parse()
    interpreter = Interpreter()
    interpreter.interpret(program)


def main():
    source = """
class Counter {
    func init(value) {
        self.value = value
    }

    func display() {
        show(self.value)
    }
}

a = Counter(10)
b = Counter(50)

a.display()
b.display()
"""

    run(source)


if __name__ == "__main__":
    main()
