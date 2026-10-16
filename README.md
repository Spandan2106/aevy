[![Architecture diagram](https://gitdiagram.com/diagram-badge.svg)](https://gitdiagram.com/spandan2106/aevy?utm_source=readme&utm_medium=badge)
[![Architecture diagram of spandan2106/aevy](https://gitdiagram.com/spandan2106/aevy/diagram.png)](https://gitdiagram.com/spandan2106/aevy?utm_source=readme&utm_medium=picture)
# Aevy

<p align="center">
  <strong>A programming language built from scratch in Python.</strong><br>
  Explore how lexical analysis, AST construction, and tree-walk interpretation bring code to life.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue.svg?style=flat-square" alt="Version 0.1.0">
  <img src="https://img.shields.io/badge/python-3.10%2B-3776AB.svg?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/tests-115%20passing-brightgreen.svg?style=flat-square" alt="115 passing tests">
  <img src="https://img.shields.io/badge/license-MIT-green.svg?style=flat-square" alt="MIT License">
</p>

<p align="center">
  <a href="https://github.com/Spandan2106/aevy/releases">Releases</a> ·
  <a href="SPEC.md">Language Specification</a> ·
  <a href="RELEASE_CHECKLIST.md">Release Checklist</a> ·
  <a href="CONTRIBUTING.md">Contributing</a> ·
  <a href="https://github.com/Spandan2106/aevy/issues">Report an Issue</a>
</p>

---

**Aevy** is an experimental interpreted programming language implemented in Python. It has its own **lexer, recursive-descent parser, abstract syntax tree (AST), and interpreter**, built using Python's standard library.

Aevy uses a deliberate hybrid syntax: **brace-delimited function and class definitions** combined with **indentation-based control flow**. The language explores core programming concepts through variables, expressions, functions, recursion, classes, collections, modules, and file operations.

> [!WARNING]
> **Experimental Alpha — v0.1.0**
>
> Aevy is actively evolving. Its syntax, built-in APIs, and behavior may change between releases. It is intended for learning and experimentation, not production-critical applications. See [SPEC.md](SPEC.md) for supported syntax and known limitations.

## Table of Contents

- [Key Highlights](#key-highlights)
- [Quick Start](#quick-start)
- [Language Overview](#language-overview)
  - [Functions and Recursion](#functions-and-recursion)
  - [Lists and Dictionaries](#lists-and-dictionaries)
  - [Object-Oriented Programming](#object-oriented-programming)
  - [Modules and File I/O](#modules-and-file-io)
  - [User Input](#user-input)
- [Language Design](#language-design)
- [Architecture](#architecture)
- [Installation](#installation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Key Highlights

- **Built from scratch:** A custom lexer, parser, AST, and tree-walk interpreter.
- **Hybrid syntax:** Brace-delimited declarations with indentation-based conditional and loop blocks.
- **Dynamic variables:** Create variables through assignment without explicit type declarations.
- **Core programming features:** Expressions, conditions, loops, functions, return values, and recursion.
- **Object-oriented programming:** Classes, constructors, inheritance, and polymorphism.
- **Collections:** Mutable lists and insertion-ordered dictionaries with built-in utilities.
- **Module system:** Relative `.aevy` imports, import caching, and circular-import detection.
- **Text-file operations:** UTF-8 reading, writing, appending, and file-existence checks.
- **Source-aware diagnostics:** Lexer, parser, and runtime errors with source-location information where available.
- **Python packaging:** Installable package with a command-line runner and distributable release artifacts.
- **Automated tests:** A regression test suite with 115 passing tests in the verified development run.

## Quick Start

### Your first Aevy program

Create a file named `hello.aevy`:

```aevy
// Welcome to Aevy
name = "World"
show("Hello, " + name + "!")
```

Expected output:

```text
Hello, World!
```

### Run Aevy

After installing the package, execute:

```powershell
aevy hello.aevy
```

You can also run a file directly from the source repository:

```powershell
$env:PYTHONPATH = "src"
python -m aevy examples/hello.aevy
```

To see the command-line options:

```powershell
aevy --help
```

## Language Overview

### Functions and Recursion

Functions are declared using `func`, with braces around the function body. Conditional blocks inside functions use a colon followed by indentation.

```aevy
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

Functions support parameters, function calls, return values, and recursion.

### Lists and Dictionaries

Aevy provides mutable lists and dictionaries for working with collections.

#### Lists

```aevy
numbers = [10, 5, 8, 2]

append(numbers, 20)
show(sort(numbers))
show(sum(numbers))
```

Available list helpers include:

- `append(list, value)`
- `pop(list)`
- `insert(list, index, value)`
- `remove(list, value)`
- `index_of(list, value)`
- `reverse(list)`
- `sum(list)`
- `sort(list)`

Lists support indexing, indexed assignment, nesting, iteration, concatenation, and repetition.

#### Dictionaries

```aevy
user = {
    "username": "spandan",
    "role": "engineer"
}

user["active"] = True

if has_key(user, "role"):
    show("User role: " + user["role"])
```

Available dictionary helpers include:

- `keys(dictionary)`
- `values(dictionary)`
- `has_key(dictionary, key)`
- `remove_key(dictionary, key)`

Dictionaries support key access, assignment, nested dictionaries, and insertion-ordered iteration. Supported keys must be hashable.

### Object-Oriented Programming

Aevy supports classes, constructors, instance methods, inheritance, and polymorphism.

```aevy
class Animal {
    func init(name) {
        this.name = name
    }

    func speak() {
        return "Generic sound"
    }
}

class Dog : Animal {
    func speak() {
        return "Woof!"
    }
}

dog = Dog("Buddy")
show(dog.name + " says: " + dog.speak())
```

Expected output:

```text
Buddy says: Woof!
```

For exact constructor, inheritance, and method-call semantics, consult [SPEC.md](SPEC.md).

### Modules and File I/O

Aevy programs can import other `.aevy` files using quoted relative paths.

For example, create `math_utils.aevy`:

```aevy
func double(n) {
    return n * 2
}
```

Then import and use it from `main.aevy`:

```aevy
import "math_utils.aevy"

show(double(21))
```

Run the main file:

```powershell
aevy main.aevy
```

Imports are cached after execution, and circular imports are reported as errors. Import paths are restricted to the directory containing the main program.

#### Text-file operations

```aevy
write_text("output.txt", "Building languages from scratch.\n")
append_text("output.txt", "Powered by Aevy.")

if file_exists("output.txt"):
    show(read_text("output.txt"))
```

The available file helpers are:

- `read_text(path)` — reads UTF-8 text.
- `write_text(path, content)` — writes text, replacing existing content.
- `append_text(path, content)` — appends text to a file.
- `file_exists(path)` — checks whether a file exists.

File paths must remain within the directory containing the main `.aevy` file. Normal operating-system permissions and I/O errors still apply.

### User Input

Aevy supports interactive line input through `give.input()`.

```aevy
name = give.input("What is your name? ")
age_text = give.input("How old are you? ")
age = number(age_text)

show("Hello, " + name)
show(age + 1)
```

`give.input()` returns text. Available conversion helpers include `number()`, `integer()`, `decimal()`, `text()`, and `boolean()`.

Invalid conversions raise errors rather than silently selecting a value.

## Language Design

Aevy uses a hybrid syntax designed to explore different approaches to readable code.

| Construct | Syntax |
|---|---|
| Function declaration | `func name(args) { ... }` |
| Class declaration | `class Name { ... }` |
| Conditional | `if condition:` followed by indentation |
| Alternative branch | `else:` followed by indentation |
| Loop | `for` or `while` with an indented body |
| Output | `show(value)` |
| Return value | `return expression` |
| Variable creation | Assignment without explicit type declarations |
| Range | `start..end`, with the ending value exclusive |
| Comment | `// comment` |

Example:

```aevy
func describe_age(age) {
    if age >= 18:
        show("Adult")
    else:
        show("Minor")
}

describe_age(20)
```

Aevy's syntax and semantics are experimental and may evolve. The language specification is the authoritative reference for supported behavior.

## Architecture

Aevy follows a conventional interpreter pipeline:

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
      Abstract Syntax Tree (AST)
                 |
                 v
            Interpreter
                 |
                 v
            Program Output
```

### Core Components

| Component | Responsibility |
|---|---|
| `lexer.py` | Converts source text into tokens. |
| `parser.py` | Parses tokens and constructs the AST. |
| `ast_nodes.py` | Defines the language's syntax-tree nodes. |
| `interpreter.py` | Evaluates statements and expressions and executes programs. |
| `__main__.py` | Provides the module command-line entry point. |

### Technology

- **Implementation language:** Python
- **Architecture:** Lexer, parser, AST, and interpreter
- **Runtime dependencies:** Python standard library
- **Package format:** Python wheel and source distribution
- **Testing:** `pytest` and `unittest`

## Installation

### Prerequisites

- Python 3.10 or later
- Git, if cloning the repository

### Method 1: Install the published wheel

1. Open the [Aevy Releases page](https://github.com/Spandan2106/aevy/releases).
2. Download `aevy_language-0.1.0-py3-none-any.whl`.
3. Open a terminal in the directory containing the downloaded file.

#### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install .\aevy_language-0.1.0-py3-none-any.whl
aevy --help
```

Then run an Aevy program:

```powershell
aevy path\to\your_program.aevy
```

#### macOS and Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install ./aevy_language-0.1.0-py3-none-any.whl
aevy --help
```

### Method 2: Install from source

Clone the repository:

```bash
git clone https://github.com/Spandan2106/aevy.git
cd aevy
```

Create and activate a virtual environment.

#### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### macOS and Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Aevy in editable mode:

```bash
python -m pip install -e .
```

Run the command-line tool:

```bash
aevy --help
aevy
aevy examples/hello.aevy
```

You can also run directly from the source tree without installing the package:

#### Windows PowerShell

```powershell
$env:PYTHONPATH = "src"
python -m aevy examples/hello.aevy
```

#### macOS and Linux

```bash
PYTHONPATH=src python -m aevy examples/hello.aevy
```

## Testing

Aevy has an automated regression test suite covering implemented language behavior, parsing, execution, and error handling.

Run the tests from the repository root:

```bash
python -m pytest -q
```

For verbose test output:

```bash
python -m pytest -v
```

The project also supports Python's built-in `unittest` runner.

#### Windows PowerShell

```powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

#### macOS and Linux

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

**Verified development result:** 115 tests passed in 1.27 seconds.

Test results reflect the covered cases; they do not establish complete language correctness or production-grade security.

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
├── examples/
├── tests/
├── README.md
├── SPEC.md
├── CONTRIBUTING.md
├── RELEASE_CHECKLIST.md
├── LICENSE
└── pyproject.toml
```

## Roadmap

### Completed

- [x] Lexer, parser, AST, and tree-walk interpreter
- [x] Variables, expressions, conditions, and loops
- [x] Functions, return values, and recursion
- [x] Classes, constructors, inheritance, and polymorphism
- [x] Lists, dictionaries, and built-in utilities
- [x] Source-aware diagnostics
- [x] Relative module imports and UTF-8 text-file operations
- [x] CLI runner and Python package metadata
- [x] Automated regression tests and CI workflow
- [x] v0.1.0 wheel and source distribution

### Planned

- [ ] Expand compatibility and edge-case coverage
- [ ] Improve diagnostics, documentation, and examples
- [ ] Explore an interactive REPL
- [ ] Evaluate additional standard-library functionality
- [ ] Investigate bytecode compilation and a virtual-machine runtime
- [ ] Continue language-semantics and security reviews before a stable 1.0 release

The roadmap is exploratory. Planned items are not implemented features and may change as the project develops.

## Contributing

Contributions, feedback, bug reports, documentation improvements, and feature suggestions are welcome.

1. Read [`CONTRIBUTING.md`](CONTRIBUTING.md).
2. Check the [existing issues](https://github.com/Spandan2106/aevy/issues).
3. For substantial changes, discuss the design in an issue first.
4. Add or update tests for behavioral changes.
5. Run the test suite before submitting a pull request.

When reporting a bug, include a minimal `.aevy` example, the command you ran, expected and actual behavior, and your Python version and operating system.

## Language Specification

See [`SPEC.md`](SPEC.md) for detailed syntax, supported constructs, semantics, examples, and known limitations.

## License

Aevy is released under the [MIT License](LICENSE).

---

**Curious about how programming languages work?** Explore the [Aevy repository](https://github.com/Spandan2106/aevy), run the examples, and follow the project's development.
