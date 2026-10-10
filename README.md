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
- [ ] Classes and objects
- [ ] Constructors, attributes, and instance methods
- [ ] Inheritance
- [ ] Input handling and expanded built-in functions
- [ ] Better syntax and runtime error diagnostics
- [ ] Automated regression and edge-case tests
- [ ] Packaging and a more convenient command-line interface
- [ ] First stable prototype release

## Development Progress

**Estimated progress: approximately 35% toward a more complete, usable first version.**

This is a subjective development estimate, not a measured completion percentage. Core language execution and recursive functions work, while object-oriented features, comprehensive testing, diagnostics, and developer tooling remain unfinished.

## Language Specification

See [`SPEC.md`](SPEC.md) for the current syntax, supported constructs, examples, and known limitations.

## Contributing

Aevy is currently under active personal development. Bug reports, suggestions, and constructive feedback are welcome. As the language evolves, the specification and implementation may change.

## License

Aevy is licensed under the **MIT License**. See the [`LICENSE`](LICENSE) file for the complete license text.