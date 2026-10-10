
# Aevy Language Specification

**Version:** 0.1  
**Status:** Initial design — implementation not started

## 1. Overview

Aevy is a general-purpose programming language designed to be
readable, beginner-friendly, and practical.

Its syntax combines explicit braces for declarations with
colon-and-indentation blocks for control flow.

The initial implementation will be an interpreter written in Python.

## 2. Design Principles

- Readable, minimal syntax
- No semicolons required
- Automatic type inference on assignment
- Explicit type conversion when needed
- Braces for functions, classes, and methods
- Colons and indentation for conditions and loops
- Clear error messages
- Interpreter first; native compilation later

## 3. Statements and Variables

Each statement normally occupies its own line.
Semicolons are not required.

Variables do not need explicit type declarations.

```aevy
name = "Spandan"
age = 20
price = 99.5
active = True
```

The interpreter infers the type from the assigned value.
Variables can be reassigned.

```aevy
age = 21
```

The exact rules for reassignment and type changes will be
defined during implementation.

## 4. Initial Data Types

The first version will support:

- Integer
- Floating-point number
- String
- Boolean

Additional types, including character and specialized numeric
types, may be introduced in later versions.

## 5. Output

`show()` displays a value.

```aevy
show("Hello, Aevy!")
show(10)
show(10 + 20)
```

## 6. Input and Type Conversion

Input is planned for a later implementation milestone.

Proposed syntax:

```aevy
name = give.input()
age = int(give.input())
price = float("99.5")
message = str(100)
```

Supported conversion functions will initially include
`int()`, `float()`, and `str()`.

Conversion behavior and invalid-input errors must be specified
before these features are implemented.

## 7. Operators

Initial arithmetic operators:

- `+` addition
- `-` subtraction
- `*` multiplication
- `/` division

Parentheses control evaluation order.

```aevy
show(10 + 20 * 2)
show((10 + 20) * 2)
```

Expected output:

```text
50
60
```

Operator precedence and division behavior will be defined
and tested during expression-parser implementation.

## 8. Comments

Single-line comments begin with `//`.

```aevy
// This is a comment
show("Hello")
```

## 9. Functions

Functions use the `func` keyword and braces.

```aevy
func greet(name) {
    show("Hello, " + name)
}
```

Rules:
- Function declarations begin with `func`.
- Parameters appear inside parentheses.
- The function body is enclosed in `{}`.
- Semicolons are not required inside the body.
- Function calls use parentheses.

Return values and return statements will be defined later.

## 10. Classes and Methods

Classes and their methods use braces.

```aevy
class Student {
    func introduce() {
        show("I am a student")
    }
}
```

Object creation, fields, constructors, inheritance, and
method-call syntax remain future design decisions.

## 11. Conditions

Conditions use a colon followed by an indented body.

```aevy
if age >= 18:
    show("Adult")
else:
    show("Minor")
```

Indentation defines the body of each condition.
`else if` or an equivalent syntax will be finalized later.

## 12. Loops

Loops use a colon followed by an indented body.

Proposed iteration syntax:

```aevy
for i in range(5):
    show(i)
```

The `range()` function, iteration rules, and other loop forms
will be defined before loop implementation.

## 13. Program Entry Point

A `main()` function is optional.

A simple program may execute top-level statements directly.

```aevy
show("Hello from Aevy")
```

A program may also declare:

```aevy
func main() {
    show("Program started")
}
```

The execution rules for `main()` will be finalized before
function execution is implemented. Its presence must not
silently change program behavior.

## 14. Block Syntax Rules

- Function declarations use braces.
- Class declarations use braces.
- Method declarations use braces.
- Conditions use colons and indentation.
- Loops use colons and indentation.
- Newlines separate statements.
- Indentation is significant inside colon-based blocks.
- Nested blocks must be supported.
- Invalid or mismatched blocks must produce clear errors.

## 15. Implementation Roadmap

1. Finalize syntax and document examples.
2. Build the lexer to produce tokens.
3. Build the parser and abstract syntax tree.
4. Evaluate literals, arithmetic, and variables.
5. Implement `show()` and error handling.
6. Add conditions and loops.
7. Add functions and optional `main()`.
8. Add classes and methods.
9. Add input and type conversion.
10. Test the language and document usage.
11. Explore intermediate representations and native compilation.
