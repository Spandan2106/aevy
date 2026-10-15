"""Aevy command-line runner.

Usage:
    python -m aevy                 Run the built-in demonstration.
    python -m aevy path/to/file.aevy  Execute an Aevy source file.
"""

import argparse
import sys
from pathlib import Path

from .diagnostics import format_error
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter


def run(source, input_func=input, base_dir=None):
    """Parse and execute Aevy source text."""
    tokens = Lexer(source).scan_tokens()
    program = Parser(tokens).parse()
    interpreter = Interpreter(source=source, input_func=input_func, base_dir=base_dir)
    interpreter.interpret(program)


def run_file(filename):
    """Read and execute one UTF-8 encoded Aevy source file."""
    path = Path(filename)
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Aevy: cannot read '{path}': {error.strerror or error}", file=sys.stderr)
        return 2

    try:
        run(source, base_dir=path.resolve().parent)
    except Exception as error:
        print(format_error(error, source), file=sys.stderr)
        return 1
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="aevy",
        description="Run an Aevy source file, or the built-in demo if no file is supplied.",
    )
    parser.add_argument("file", nargs="?", help="path to an .aevy source file")
    args = parser.parse_args(argv)

    if args.file:
        return run_file(args.file)

    demo = '''\
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
'''
    try:
        run(demo)
    except Exception as error:
        print(format_error(error, demo), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
