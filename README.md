
# Aevy

```{=html}
<p align="center">
```
`<strong>`{=html}A programming language built from scratch in
Python.`</strong>`{=html}`<br>`{=html} An experimental
language-engineering project exploring how source code becomes
executable behavior.
```{=html}
</p>
```
```{=html}
<p align="center">
```
`<a href="https://github.com/Spandan2106/aevy/releases">`{=html}Latest
release: v0.1.0`</a>`{=html} · `<a href="SPEC.md">`{=html}Language
specification`</a>`{=html} ·
`<a href="RELEASE_CHECKLIST.md">`{=html}Release checklist`</a>`{=html}
```{=html}
</p>
```

------------------------------------------------------------------------

Aevy is an experimental programming language with its own **lexer,
parser, abstract syntax tree (AST), and interpreter**. Its hybrid syntax
combines brace-delimited function and class definitions with
indentation-based control-flow blocks. It supports functions, recursion,
object-oriented programming, collections, module imports, and UTF-8
text-file operations.

**Current version:** `0.1.0` · **Status:** Experimental alpha

> \[!WARNING\] Aevy is under active development. Syntax and behavior may
> change between releases. It is a learning and experimentation project,
> not a production-ready language. Review the [language
> specification](SPEC.md) and [release checklist](RELEASE_CHECKLIST.md)
> before relying on it.

## Contents

-   [Highlights](#highlights)
-   [Your first Aevy program](#your-first-aevy-program)
-   [Language examples](#language-examples)
-   [Features](#features)
-   [How Aevy works](#how-aevy-works)
-   [Install and run](#install-and-run)
-   [Run the tests](#run-the-tests)
-   [Project structure](#project-structure)
-   [Roadmap](#roadmap)
-   [Contributing](#contributing)
-   [License](#license)

## Highlights

-   **Built from scratch:** a custom lexer, parser, AST, and
    interpreter.
-   **Readable syntax:** inferred variables, `func` declarations, and
    `show()` output.
-   **Core programming constructs:** conditions, loops, functions,
    return values, and recursion.
-   **Object-oriented programming:** classes, inheritance, and
    polymorphism.
-   **Useful data structures:** mutable lists and insertion-ordered
    dictionaries.
-   **Modules and files:** relative `.aevy` imports and UTF-8 text-file
    helpers.
-   **Developer tooling:** command-line runner, source-aware
    diagnostics, package metadata, and automated tests.

## Your first Aevy program

Save this as `hello.aevy`:

``` aevy
name = "Aevy"
show("Hello, " + name)
```

Output:

``` text
Hello, Aevy
```

Run it from the project root:

``` powershell
$env:PYTHONPATH = "src"
python -m aevy examples/hello.aevy
```

Or, after installing Aevy, use the command-line tool:

``` powershell
aevy examples/hello.aevy
```

## Language examples

### Functions and return values

``` aevy
func add(a, b) {
    return a + b
}

result = add(10, 20)
show(result)
```

Output: `30`

### Recursion

``` aevy
func factorial(n) {
    if n <= 1:
        return 1
    return n * factorial(n - 1)
}

show(factorial(5))
```

Output: `120`

### Lists

``` aevy
numbers = [5, 2, 8, 1]
append(numbers, 10)

for item in numbers:
    show(item)

show(sum(numbers))
show(sort(numbers))
```

Lists support indexing, indexed assignment, nesting, iteration,
mutation, concatenation, and repetition. Helpers include `append`,
`pop`, `insert`, `remove`, `index_of`, `reverse`, `sum`, and `sort`.

### Dictionaries

``` aevy
person = {"name": "Alex", "age": 20}
person["age"] = 21
person["city"] = "Kolkata"

show(person["name"])
show(keys(person))
show(values(person))
show(has_key(person, "city"))
remove_key(person, "city")
```

Dictionaries support key access and assignment, nested dictionaries,
membership checks, and insertion-ordered key iteration. String, number,
and boolean keys are supported when hashable.

### Modules

Create `helpers.aevy`:

``` aevy
func double(n) {
    return n * 2
}
```

Then create `main.aevy`:

``` aevy
import "helpers.aevy"
show(double(21))
```

Run the main file:

``` powershell
aevy main.aevy
```

Imports use quoted relative paths, are cached after execution, and
reject circular imports. Import paths are restricted to the directory
containing the main program.

### Text-file I/O

``` aevy
write_text("notes.txt", "Hello")
append_text("notes.txt", " Aevy")

show(read_text("notes.txt"))
show(file_exists("notes.txt"))
```

Text is read and written as UTF-8. `write_text()` replaces existing
content; `append_text()` adds content to the end. Paths must stay within
the directory containing the main `.aevy` file. File operations can
still fail because of permissions or other I/O errors.

### User input and conversion

``` aevy
name = give.input("What is your name? ")
age_text = give.input("How old are you? ")
age = number(age_text)

show("Hello, " + name)
show(age + 1)
```

`give.input()` returns text. Conversion helpers include `number()`,
`integer()`, `decimal()`, `text()`, and `boolean()`. Invalid conversions
raise errors rather than silently choosing a value.

## Features

  -----------------------------------------------------------------------
  Area                                Current support
  ----------------------------------- -----------------------------------
  Types and variables                 Integers, decimals, strings,
                                      booleans, inferred variables

  Expressions                         Arithmetic, comparison, equality,
                                      logical operators

  Control flow                        `if`, `elif`, `else`, `for`,
                                      `while`, `break`, `continue`

  Functions                           Parameters, calls, return values,
                                      recursion

  Object-oriented programming         Classes, constructors, inheritance,
                                      polymorphism

  Lists                               Indexing, mutation, nested lists,
                                      iteration, helper functions

  Dictionaries                        Key access, mutation, nested
                                      dictionaries, helper functions

  Built-ins                           `show()`, `give.input()`,
                                      conversions, string and numeric
                                      utilities

  Modules                             Relative `.aevy` imports, import
                                      caching, circular-import detection

  Text files                          UTF-8 read, write, append, and
                                      existence checks

  Diagnostics                         Lexer/parser locations and
                                      source-aware runtime errors

  CLI                                 `python -m aevy` and the installed
                                      `aevy` command
  -----------------------------------------------------------------------

For exact syntax, semantics, and known limitations, see
[`SPEC.md`](SPEC.md).

## Language design

Aevy uses a deliberate hybrid syntax:

-   `func` declares functions.
-   Function and class bodies use braces: `{}`.
-   Conditional and loop blocks use a colon followed by indentation.
-   Assignment creates variables; explicit type declarations are not
    required.
-   `show()` displays a value.
-   `return` sends a value back from a function.
-   `start..end` represents an end-exclusive integer range in a `for`
    loop.
-   Use `//` for comments.

Example:

``` aevy
func describe_age(age) {
    if age >= 18:
        show("Adult")
    else:
        show("Minor")
}

describe_age(20)
```

## How Aevy works

Aevy follows a conventional interpreter pipeline:

``` text
Aevy source file
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
 Program output
```

**Implementation:** Python · **Architecture:** Lexer, parser, AST,
interpreter · **Runtime dependencies:** None required

## Install and run

### Requirements

-   Python 3.10 or later
-   Git, if cloning the repository

### Option 1: Install the published release

Download `aevy_language-0.1.0-py3-none-any.whl` from the [GitHub
Releases page](https://github.com/Spandan2106/aevy/releases).

In Windows PowerShell, from the folder containing the downloaded wheel:

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install .\aevy_language-0.1.0-py3-none-any.whl
aevy --help
```

Then run an Aevy source file:

``` powershell
aevy path\to\your_program.aevy
```

On macOS/Linux, activate the environment with
`source .venv/bin/activate`, then install the downloaded wheel using
`python -m pip install ./aevy_language-0.1.0-py3-none-any.whl`.

### Option 2: Install from source

Clone the repository:

``` bash
git clone https://github.com/Spandan2106/aevy.git
cd aevy
```

Create and activate a virtual environment in PowerShell:

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the package in editable mode:

``` powershell
python -m pip install -e .
```

Run the CLI and an example:

``` powershell
aevy --help
aevy
aevy examples/hello.aevy
```

You can also run directly from source without installing the package:

``` powershell
$env:PYTHONPATH = "src"
python -m aevy examples/hello.aevy
```

On macOS/Linux, use:

``` bash
PYTHONPATH=src python -m aevy examples/hello.aevy
```

## Run the tests

From the repository root, with the development environment activated:

``` powershell
python -m pytest -q
```

The project also supports Python's built-in `unittest` runner:

``` powershell
$env:PYTHONPATH = "src"
python -m unittest discover -s tests -v
```

The current development test suite has **115 passing tests**. Tests
cover implemented behavior; they do not prove complete language
correctness or production security.

## Project structure

``` text
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
├── RELEASE_CHECKLIST.md
├── LICENSE
└── pyproject.toml
```

## Roadmap

-   [x] Lexer, parser, AST, and interpreter
-   [x] Variables, expressions, conditions, and loops
-   [x] Functions, return values, and recursion
-   [x] Classes, inheritance, and polymorphism
-   [x] Lists, dictionaries, and standard-library helpers
-   [x] Source-aware diagnostics and CLI file execution
-   [x] Relative imports and text-file I/O
-   [x] Automated regression tests and CI workflow
-   [x] Python package metadata and v0.1.0 distribution builds
-   [ ] Expand compatibility and edge-case coverage
-   [ ] Continue improving diagnostics and documentation
-   [ ] Review security boundaries and language semantics before a
    stable `1.0` release

## Contributing

Aevy is an active personal language-engineering project. Bug reports,
reproducible examples, feature ideas, and constructive feedback are
welcome through [GitHub
Issues](https://github.com/Spandan2106/aevy/issues).

When reporting a bug, include: - The smallest `.aevy` program that
reproduces it - The command you ran - The actual output and expected
output - Your Python version and operating system

Because Aevy is experimental, check the language specification before
assuming a feature is supported.

## License

Aevy is released under the [MIT License](LICENSE).

------------------------------------------------------------------------

**Curious about how programming languages work?** Explore the source,
run the examples, and follow Aevy's development through the [Aevy
repository](https://github.com/Spandan2106/aevy).
