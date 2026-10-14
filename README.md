# Aevy

**An experimental programming language implemented from scratch in Python.**

Aevy is a personal language-engineering project exploring how programming languages work internally. It includes a custom lexer, parser, Abstract Syntax Tree (AST), and interpreter, with a focus on readable syntax and incremental development.

> **Project status:** Early-stage prototype — actively under development.

## Current Features

- **Lexical Analysis:** Converts source code into tokens using a custom lexer.
- **Parsing:** Parses tokens into a structured AST.
- **Interpreter:** Executes programs by evaluating expressions and statements.
- **Variables:** Assignment-based variable creation without explicit type declarations.
- **Basic Data Types:** Integers, floating-point numbers, strings, and booleans.
- **Expressions:** Arithmetic, comparison, equality, and logical operators.
- **Conditional Logic:** `if`, `elif`, and `else`.
- **Loops:** `for` loops with range syntax and `while` loops.
- **Loop Control:** `break` and `continue`.
- **Functions:** Function declarations, parameters, and function calls.
- **Return Values:** Functions can return computed values.
- **Recursion:** Functions can call themselves, including recursive computations.
- **Output:** Displays evaluated values using `show()`.
- **User Input:** Reads a line of text with `give.input()` or `give.input("Prompt: ")`.
- **Type Conversions:** Provides `number()`, `integer()`, `decimal()`, `text()`, and `boolean()` with validation.
- **String Utilities:** `length()`, `upper()`, `lower()`, `trim()`, and `contains()`.
- **Lists:** list literals, indexing, indexed assignment, nested lists, and list mutation.
- **Numeric Utilities:** `abs()`, `min()`, `max()`, and `round()` with argument validation.

## Example Programs

### Functions and Return Values

```text
func add(a, b) {
    return a + b
}

result = add(10, 20)
show(result)
```

Output:

```text
30
```

### Recursion

```text
func factorial(n) {
    if n <= 1:
        return 1
    return n * factorial(n - 1)
}

show(factorial(5))
```

Output:

```text
120
```

## User Input and Type Conversion

```text
name = give.input("What is your name? ")
age_text = give.input("How old are you? ")
age = number(age_text)
show("Hello, " + name)
show(age + 1)
```

`give.input()` returns text. Use `number(value)` to convert a numeric string to an integer or decimal, `integer(value)` for an integer, `decimal(value)` for a floating-point number, `text(value)` for text, and `boolean(value)` for `True` or `False`. Invalid conversions raise a readable `ValueError` rather than silently choosing a value.

For deterministic automated tests, the Python `Interpreter` accepts an optional `input_func` callable; ordinary Aevy programs do not need to know about this testing hook.

## Lists

Aevy supports list literals with square brackets, including empty and nested lists. List indexes are zero-based.

```aevy
numbers = [10, 20, 30]
show(numbers[0])
numbers[1] = 99
append(numbers, 40)
show(length(numbers))
show(pop(numbers))
```

`append(list, value)` adds a value to the end and returns no value. `pop(list)` removes and returns the last value; calling it on an empty list raises an error. Indexes must be integers and must be in range. Lists are mutable, so assigning a list to another variable shares the same list object.

## Standard Library

Aevy includes a small set of built-in string and numeric helpers:

```text
show(length("Aevy"))
show(upper("hello"))
show(lower("WORLD"))
show(trim("  spaced text  "))
show(contains("programming", "gram"))
show(abs(-12))
show(min(7, 2, 9))
show(max(7, 2, 9))
show(round(3.14159, 2))
```

The string functions require text arguments. `contains(text, part)` returns `True` when `part` occurs inside `text`. Numeric helpers reject booleans rather than treating them as numbers. `min()` and `max()` accept two or more numeric arguments; `round()` accepts a number and an optional integer number of decimal places. Invalid argument types or counts raise clear errors.

## Language Design

Aevy currently uses a hybrid syntax:

- Function bodies use braces: `{}`.
- Conditional and loop blocks use indentation.
- `func` declares a function.
- `return` returns a value from a function.
- `show()` displays an expression's result.
- Assignment creates variables without explicit type declarations.
- The `..` operator represents a range in `for` loops; the ending value is exclusive.

The syntax and semantics may change as the language evolves.

## Architecture

Aevy follows a traditional interpreter pipeline:

```text
Source Code
    |
    v
   Lexer
    |
    v
  Tokens
    |
    v
   Parser
    |
    v
   AST
    |
    v
 Interpreter
    |
    v
 Program Output
```

### Technology Stack

- **Implementation language:** Python
- **Architecture:** Lexer, parser, AST, and interpreter
- **Version control:** Git and GitHub

## Project Structure

```text
aevy/
├── src/
│   └── aevy/
│       ├── __init__.py
│       ├── __main__.py
│       ├── token.py
│       ├── lexer.py
│       ├── ast_nodes.py
│       ├── parser.py
│       └── interpreter.py
├── README.md
├── SPEC.md
├── LICENSE
└── ...
```

## Getting Started

### Requirements

- Python 3.10 or later
- Git, if cloning the repository

### Run Aevy

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd aevy
```

Run the current entry point in Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m aevy
```

The current entry point executes the source program configured in `src/aevy/__main__.py`.

## Roadmap

- [x] Lexer and token definitions
- [x] Parser and AST representation
- [x] Variables and assignment
- [x] Arithmetic, comparison, and logical expressions
- [x] Conditional statements
- [x] Loops and loop-control statements
- [x] Function declarations and calls
- [x] Return values
- [x] Recursive function execution
- [x] Classes and objects
- [x] Constructors, attributes, and instance methods
- [x] Single inheritance, method overriding, polymorphism, and `super` calls
- [ ] Input handling and expanded built-in functions
- [x] Lexer/parser diagnostics and source-aware runtime error locations
- [x] Automated regression and edge-case tests
- [ ] Packaging and a more convenient command-line interface
- [ ] First stable prototype release

## Automated Tests

Run the interpreter regression tests from the project root:

```powershell
python -m unittest discover -s tests -v
```

The suite contains 29 tests covering arithmetic, functions and return values, recursion,
range loops, inheritance, `super` calls, private and public attributes, loop edge cases,
syntax diagnostics, and source-aware runtime errors. Add a regression test whenever a
language feature or bug fix is introduced.

## Development Progress

**Estimated progress: approximately 35% toward a more complete, usable first version.**

This is a subjective development estimate, not a measured completion percentage. Core language execution and recursive functions work, while object-oriented features, comprehensive testing, diagnostics, and developer tooling remain unfinished.

## Language Specification

See [`SPEC.md`](SPEC.md) for the current syntax, supported constructs, examples, and known limitations.

## Contributing

Aevy is currently under active personal development. Bug reports, suggestions, and constructive feedback are welcome. As the language evolves, the specification and implementation may change.

## License

Aevy is licensed under the **MIT License**. See the [`LICENSE`](LICENSE) file for the complete license text.

## Error messages

Aevy reports lexer and parser errors with line and column locations where available.
Runtime errors now retain the most specific available AST source location. The formatter
can display the line, column, source line, and a caret pointing to the error. For example,
`show(x / y)` reports division-by-zero at the `/` operator. The command-line demo prints
concise, categorized errors instead of a Python traceback for common language errors.

Run the regression tests from the project root:

```bash
python -m unittest discover -s tests -v
```
