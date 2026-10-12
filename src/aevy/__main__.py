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
    func speak() {
        show("Animal sound")
    }
}

class Dog extends Animal {
    func speak() {
        show("Woof!")
    }
}

class Cat extends Animal {
    func speak() {
        show("Meow!")
    }
}

func make_sound(animal) {
    animal.speak()
}

dog = Dog()
cat = Cat()
animal = Animal()

make_sound(dog)
make_sound(cat)
make_sound(animal)
"""

    run(source)


if __name__ == "__main__":
    main()
