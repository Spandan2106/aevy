
# Contributing to Aevy

Thank you for your interest in contributing to **Aevy**! Whether you are fixing a bug, proposing new syntax, improving test coverage, or optimizing internal mechanics, your help makes this project better.

Aevy is an experimental programming language designed from scratch in Python to explore how source code becomes executable behavior. We welcome constructive contributions from language enthusiasts, students, and engineers alike.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Reporting Bugs & Suggesting Features](#reporting-bugs--suggesting-features)
- [Development Setup](#development-setup)
  - [Prerequisites](#prerequisites)
  - [Windows (PowerShell)](#windows-powershell)
  - [macOS & Linux (Bash / Zsh)](#macos--linux-bash--zsh)
- [Running Tests](#running-tests)
- [Coding & Testing Standards](#coding--testing-standards)
- [Language Conventions & Syntax Rules](#language-conventions--syntax-rules)
- [Pull Request Workflow](#pull-request-workflow)
- [Security Disclosures](#security-disclosures)

---

## Code of Conduct

We are committed to providing a friendly, respectful, and welcoming environment for everyone. Please be considerate, communicate with empathy, and provide constructive technical feedback.

---

## Reporting Bugs & Suggesting Features

### Reporting Bugs

Before creating a bug report, check the open [Issues](https://github.com/Spandan2106/aevy/issues) to ensure it hasn't already been reported.

When filing an issue, include:

1. **A minimal reproducible example:** The shortest possible `.aevy` snippet demonstrating the problem.
2. **Execution details:** The exact command run (e.g., `aevy bug.aevy` or `python -m aevy bug.aevy`).
3. **Observed vs. Expected behavior:** Output logs, tracebacks, or diagnostic errors compared to what you expected.
4. **Environment:** Python version (`python --version`) and operating system.

### Suggesting Features or Syntax Changes

Because Aevy is an experimental language with a deliberate hybrid grammar, language changes require discussion before implementation:

- Open a feature proposal under [Issues](https://github.com/Spandan2106/aevy/issues).
- Outline the proposed syntax with clear examples.
- Explain the motivation: How does this improve the language without complicating the lexer/parser pipeline?
- Note any changes required in `SPEC.md`.

---

## Development Setup

### Prerequisites

- **Python 3.10+**
- **Git**

### Windows (PowerShell)

```powershell
# 1. Clone your fork
git clone https://github.com/<your-username>/aevy.git
cd aevy

# 2. Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install in editable mode with development dependencies
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### macOS & Linux (Bash / Zsh)

```bash
# 1. Clone your fork
git clone https://github.com/<your-username>/aevy.git
cd aevy

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install in editable mode with development dependencies
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

---

## Running Tests

Aevy uses `pytest` for unit and regression testing. All changes must pass the test suite before being reviewed.

```bash
# Run tests quietly
pytest -q

# Run tests with detailed output
pytest -v

# Run Python's built-in unittest runner (alternative)
python -m unittest discover -s tests -v
```

Always add new regression tests in the `tests/` directory for bug fixes or new grammar features.

---

## Coding & Testing Standards

To keep the language runtime clean, maintainable, and educational:

- **Zero Runtime Dependencies:** The core language engine (`src/aevy/`) must rely only on the Python standard library. Do not introduce third-party libraries for tokenizing, parsing, or interpreting.
- **Explicit Architecture:** Keep the separation of concerns distinct:
  - `token.py`: Token types and lexical representations.
  - `lexer.py`: Character scanning, string escapes, and line/column tracking.
  - `ast_nodes.py`: AST definitions and node representations.
  - `parser.py`: Grammar enforcement and tree assembly.
  - `interpreter.py`: Tree-walking runtime, environment scopes, and built-ins.
- **Accurate Diagnostics:** When raising runtime or syntax errors, attach line and column numbers using the token's coordinate data whenever possible.
- **Clean Python Code:** Follow PEP 8 guidelines and use descriptive variable and method names.

---

## Language Conventions & Syntax Rules

When implementing or modifying syntax, adhere to Aevy's established grammar principles:

1. **Hybrid Scoping**
   - **Braces `{}`** are used for declarations such as `func` and `class`.
   - **Colons and indentation** are used for control-flow blocks such as `if`, `elif`, `else`, `for`, and `while`.

2. **Dynamic Typing**
   - Variables are dynamically typed and inferred at assignment. Avoid introducing mandatory static type keywords into the core syntax without prior discussion.

3. **Explicit I/O and Built-ins**
   - Display output: `show(...)`
   - User console input: `give.input(...)`
   - Explicit conversions: `number()`, `integer()`, `decimal()`, `text()`, and `boolean()`

4. **File Isolation**
   - Built-in file I/O operations (`read_text`, `write_text`, and `append_text`) and relative `import` statements must remain sandboxed to the active workspace to prevent path-traversal vulnerabilities.

---

## Pull Request Workflow

1. **Fork and Branch:** Fork the repository and create a dedicated branch for your work.

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Implement:** Make your changes, keeping commits clear and focused.

3. **Test:** Verify that all existing tests pass, along with your new test cases.

   ```bash
   pytest -q
   ```

4. **Documentation:** Update `README.md` or `SPEC.md` if your changes alter language behavior or command-line flags.

5. **Submit:** Open a pull request targeting the `main` branch. Provide a clear summary of:
   - What the PR changes.
   - Why the change is necessary.
   - How you tested it.

---

## Security Disclosures

If you discover a security vulnerability or directory traversal flaw in Aevy, especially in file I/O or module loading:

- **Please do not open a public issue.**
- Report the vulnerability privately using GitHub's private vulnerability reporting feature, if enabled for the repository. Otherwise, contact the repository owner privately.
- Include reproduction steps and potential impact so a patch can be prepared before public disclosure.
