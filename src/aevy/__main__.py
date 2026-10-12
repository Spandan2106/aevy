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
class Animal {
    func init(name) {
        self.name = name
    }

    func speak() {
        show("Animal sound")
    }
}

class Dog extends Animal {
    func init(name, breed) {
        super.init(name)
        self.breed = breed
    }

    func speak() {
        super.speak()
        show(self.breed)
    }
}

pet = Dog("Rex", "Labrador")
pet.speak()
"""

    run(source)


if __name__ == "__main__":
    main()
