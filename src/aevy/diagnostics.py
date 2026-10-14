"""Human-friendly formatting for errors raised by the Aevy frontend/runtime."""


def format_error(error, source=None):
    """Format an error, including its Aevy source location when available."""
    name = type(error).__name__
    message = str(error).strip() or "An unexpected error occurred."

    if isinstance(error, SyntaxError):
        label = "Syntax error"
    elif isinstance(error, NameError):
        label = "Name error"
    elif isinstance(error, TypeError):
        label = "Type error"
    elif isinstance(error, PermissionError):
        label = "Access error"
    elif isinstance(error, ZeroDivisionError):
        label = "Arithmetic error"
        message = "Division by zero"
    elif isinstance(error, (RuntimeError, ValueError, IndexError)):
        label = "Runtime error"
    else:
        label = name

    result = f"{label}: {message}"
    line = getattr(error, "aevy_line", None)
    column = getattr(error, "aevy_column", None)
    if line is not None and column is not None:
        result += f"\n  at line {line}, column {column}"
        if source is not None:
            lines = source.splitlines()
            if 1 <= line <= len(lines):
                source_line = lines[line - 1]
                result += f"\n  {source_line}\n  {' ' * max(column - 1, 0)}^"
    return result
