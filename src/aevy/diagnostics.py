"""Human-friendly formatting for errors raised by the Aevy frontend/runtime."""


def format_error(error):
    """Return a concise error message without Python traceback noise."""
    name = type(error).__name__
    message = str(error).strip() or "An unexpected error occurred."
    if isinstance(error, SyntaxError):
        return f"Syntax error: {message}"
    if isinstance(error, NameError):
        return f"Name error: {message}"
    if isinstance(error, TypeError):
        return f"Type error: {message}"
    if isinstance(error, PermissionError):
        return f"Access error: {message}"
    if isinstance(error, ZeroDivisionError):
        return f"Arithmetic error: division by zero."
    if isinstance(error, (RuntimeError, ValueError, IndexError)):
        return f"Runtime error: {message}"
    return f"{name}: {message}"
