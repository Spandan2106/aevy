# Aevy Language Specification

**Version:** 0.1.0 — Working Draft  
**Status:** Experimental prototype  
**Implementation:** Python

## 1. Introduction

Aevy is an experimental programming language implemented in Python. Its purpose is to explore language design and interpreter construction through a custom lexer, parser, Abstract Syntax Tree (AST), and interpreter.

This document describes the language features currently implemented in the prototype. It is a working specification: behavior and syntax may change as development continues.

### 1.1 Design Goals

- Keep the syntax readable and approachable.
- Build the interpreter from fundamental components.
- Support expressions, variables, control flow, and functions.
- Make function calls and recursive execution possible.
- Extend the language incrementally with testing and documentation.

## 2. Source Code and Syntax

### 2.1 Statements and Line Structure

Aevy programs consist of statements separated by newlines. Semicolons are not required.

```text
x = 10
y = 20
show(x + y)
```

### 2.2 Comments

Single-line comments begin with `//`.

```text
// This is a comment
score = 100
show(score)
```

Comments and blank lines are ignored by the lexer.

### 2.3 Identifiers

Identifiers represent variable names, function names, and parameters.

- An identifier starts with a letter or underscore.
- Subsequent characters may include letters, digits, and underscores.
- Identifier names are case-sensitive.

Examples:

```text
count = 10
user_name = "Aevy"
_total = 50
```

### 2.4 Indentation and Braces

Aevy currently uses a hybrid block syntax:

- Braces delimit function bodies.
- Indentation delimits conditional and loop bodies.
- Tabs and spaces may be supported by the lexer, but they must not be mixed within the same indentation structure.

Function example:

```text
func multiply(a, b) {
    return a * b
}
```

Conditional example:

```text
if score >= 50:
    show("Pass")
else:
    show("Fail")
```

## 3. Values and Variables

### 3.1 Variable Assignment

Variables are created through assignment. Explicit variable declarations and type annotations are not currently required.

```text
age = 20
name = "Aevy"
active = True
```

The interpreter stores assigned values in its execution environment.

### 3.2 Supported Data Types

| Type | Example |
|---|---|
| Integer | `42` |
| Floating-point number | `3.14` |
| String | `"Hello"` |
| Boolean | `True`, `False` |

Type inference occurs from the assigned value. The exact rules for reassignment and implicit type conversion remain subject to implementation details.

### 3.3 Built-in Conversions

Aevy provides these built-in conversion functions:

| Function | Behavior |
|---|---|
| `number(value)` | Keeps a number unchanged or parses a string as an integer when possible, otherwise as a decimal number. |
| `integer(value)` | Converts an integer, decimal number, or numeric string to an integer. |
| `decimal(value)` | Converts a number or numeric string to a floating-point number. |
| `text(value)` | Converts a value to its textual representation. |
| `boolean(value)` | Accepts a boolean or the strings `True` and `False` (case-insensitive). |

Each conversion function accepts exactly one argument. Invalid values raise a `ValueError`; incorrect argument counts raise a `TypeError`.

### 3.4 User Input

`give.input()` reads a line of text from standard input and returns it as a string. An optional string argument is displayed as a prompt:

```text
name = give.input("What is your name? ")
age = number(give.input("How old are you? "))
show("Hello, " + name)
show(age + 1)
```

`give.input()` accepts zero or one argument. If an argument is supplied, it must be a string. Input is always returned as text; convert it explicitly before numeric calculations. When standard input reaches end-of-file, the interpreter reports a runtime error.

### 3.5 Standard Library Utilities

Aevy reserves the following built-in names:

| Function | Behavior | Arguments |
|---|---|---|
| `length(text)` | Returns the number of characters in a string. | Exactly 1 string |
| `upper(text)` | Returns the string in uppercase. | Exactly 1 string |
| `lower(text)` | Returns the string in lowercase. | Exactly 1 string |
| `trim(text)` | Removes whitespace from both ends of a string. | Exactly 1 string |
| `contains(text, part)` | Checks whether `part` occurs in `text`. | Exactly 2 strings |
| `abs(number)` | Returns the absolute value. | Exactly 1 number |
| `min(a, b, ...)` | Returns the smallest argument. | At least 2 numbers |
| `max(a, b, ...)` | Returns the largest argument. | At least 2 numbers |
| `round(number[, digits])` | Rounds a number, optionally to a specified number of decimal places. | 1 number and optional integer |

These helpers validate argument types. Booleans are not accepted as numeric arguments. Invalid argument types or counts raise a `TypeError`. `length()` currently accepts strings only; list and collection support is not part of this version.

## 4. Operators and Expressions

### 4.1 Arithmetic Operators

| Operator | Purpose |
|---|---|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |

### 4.2 Comparison Operators

The language supports comparison and equality expressions, including:

```text
a < b
a <= b
a > b
a >= b
a == b
a != b
```

These expressions are commonly used in conditions and loops.

### 4.3 Logical Operators

```text
a and b
a or b
not a
```

The exact evaluation rules, including short-circuit behavior, should be documented after they are verified against the interpreter.

### 4.4 Grouping Expressions

Parentheses can be used to group expressions and to pass arguments to function calls.

```text
result = (2 + 3) * 4
show(result)
```

### 4.5 Operator Precedence

The parser implements expression precedence so that expressions are not evaluated solely from left to right. The complete precedence table and associativity rules remain to be formally documented and tested.

## 5. Output

The `show()` construct displays the result of an expression.

```text
show(10)
show("Hello, Aevy")
show(5 + 7)
```

The current parser expects an expression inside `show()`. Empty calls such as `show()` are not part of the documented syntax.

## 6. Conditional Statements

### 6.1 `if`

```text
if age >= 18:
    show("Adult")
```

### 6.2 `if` and `else`

```text
if score >= 50:
    show("Pass")
else:
    show("Fail")
```

### 6.3 `elif`

```text
if score >= 90:
    show("Excellent")
elif score >= 50:
    show("Pass")
else:
    show("Try again")
```

Conditions are evaluated by the interpreter to select the branch to execute.

## 7. Loops

### 7.1 `while`

A `while` loop repeats while its condition remains true.

```text
count = 1

while count <= 3:
    show(count)
    count = count + 1
```

### 7.2 `for` and Ranges

Aevy supports range-based iteration using `..`.

```text
for i in 1..5:
    show(i)
```

The end value is exclusive. The intended sequence is `1`, `2`, `3`, and `4`.

### 7.3 `break`

`break` exits the current loop.

```text
for i in 1..10:
    if i == 4:
        break
    show(i)
```

### 7.4 `continue`

`continue` skips the remaining statements in the current iteration and proceeds to the next iteration.

```text
for i in 1..5:
    if i == 3:
        continue
    show(i)
```

The precise behavior of nested loop-control statements should be covered by regression tests.

## 8. Functions

### 8.1 Function Declaration

Functions are declared using `func`, followed by a name, a parameter list, and a brace-delimited body.

```text
func greet(name) {
    show(name)
}
```

### 8.2 Parameters and Function Calls

```text
func add(a, b) {
    return a + b
}

result = add(10, 20)
show(result)
```

Arguments are evaluated when the function is called and associated with the corresponding parameters. The current interpreter checks that the number of arguments matches the number of parameters.

### 8.3 Return Values

`return` exits the current function and optionally supplies a result.

```text
func square(n) {
    return n * n
}

show(square(5))
```

A function that reaches the end of its body without returning a value produces the interpreter's default `None` result.

A `return` statement is intended to be used inside a function. Error handling for invalid uses remains an area for improvement.

### 8.4 Nested Function Calls

Function calls can be composed:

```text
func add(a, b) {
    return a + b
}

func double(n) {
    return n * 2
}

func calculate(x) {
    temp = add(x, 5)
    return double(temp)
}

show(calculate(10))
```

Expected output:

```text
30
```

### 8.5 Recursion

A function may call itself recursively.

```text
func factorial(n) {
    if n <= 1:
        return 1
    return n * factorial(n - 1)
}

show(factorial(5))
```

Expected output:

```text
120
```

The current prototype supports recursive function execution. A configurable recursion limit and dedicated recursion diagnostics are not yet specified.

### 8.6 Function Scope

The interpreter creates a local environment for each function call and restores the previous environment after the call finishes. Variable lookup can fall back to the global environment.

Detailed rules for variable shadowing, global assignment, closures, and nested function declarations are not yet part of the formal specification.

## 9. Execution Model

Aevy follows a multi-stage interpretation pipeline.

1. **Lexing:** Source text is converted into tokens.
2. **Parsing:** Tokens are converted into an AST.
3. **AST construction:** The AST represents expressions and statements as structured nodes.
4. **Interpretation:** The interpreter evaluates expressions and executes statements.
5. **Output:** Operations such as `show()` display values.

The implementation is organized into separate modules:

- `token.py` — token definitions
- `lexer.py` — lexical analysis
- `ast_nodes.py` — AST node definitions
- `parser.py` — syntax analysis
- `interpreter.py` — execution and evaluation
- `__main__.py` — current program entry point

## 10. Known Limitations

The current prototype does not yet define or fully implement the following language features:

- Classes and objects
- Constructors and instance methods
- Object attributes and inheritance
- [x] User input as a standard language feature
- Modules and imports
- Exception handling
- A formal standard library
- Complete static or runtime type rules
- A stable, comprehensive error-reporting system
- A complete operator precedence and associativity reference
- A comprehensive automated conformance test suite
- A packaged executable or stable command-line interface

These are potential development areas, not promises that every feature will necessarily be implemented.

## 11. Development Roadmap

- [x] Lexer and token definitions
- [x] AST representation and parser
- [x] Variables and expressions
- [x] Conditional statements
- [x] Loops and loop control
- [x] Functions and parameters
- [x] Return values
- [x] Nested function calls and recursion
- [ ] Formalize operator precedence and evaluation rules
- [ ] Add automated tests for language behavior
- [ ] Improve syntax and runtime diagnostics
- [ ] Add classes, objects, and constructors
- [ ] Add instance methods and inheritance
- [x] Add input handling and built-in conversion functions
- [ ] Define a stable execution and packaging workflow

## 12. Specification Status

This document describes an early prototype and is not a finalized language standard. Where behavior has not been tested or explicitly specified, implementation behavior may change.

Future releases should update this specification alongside changes to the lexer, parser, AST, interpreter, and test suite.

## 13. License

Aevy is distributed under the MIT License. See the repository's `LICENSE` file for the complete terms.