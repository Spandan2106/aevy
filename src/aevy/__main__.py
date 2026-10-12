import sys

from .diagnostics import format_error
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

class BankAccount {
    func init(balance) {
        self._balance = balance
    }

    func deposit(amount) {
        if amount > 0:
            self._balance = self._balance + amount
    }

    func get_balance() {
        return self._balance
    }
}

account = BankAccount(1000)
account.deposit(500)
show(account.get_balance())

"""
    try:
        run(source)
    except (SyntaxError, NameError, TypeError, PermissionError,
            RuntimeError, ValueError, ZeroDivisionError, IndexError) as error:
        print(format_error(error), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
