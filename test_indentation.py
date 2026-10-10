
from src.aevy.lexer import Lexer
from src.aevy.token import TokenType

source = '''age = 20
score = 75

if age >= 18:
    if score >= 50:
        show("Pass")
    show("Checked")
show("Done")
'''

tokens = Lexer(source).scan_tokens()

for token in tokens:
    print(token)

# Check that indentation levels open and close correctly.
indent_tokens = [
    token.type
    for token in tokens
    if token.type in (TokenType.INDENT, TokenType.DEDENT)
]

expected = [
    TokenType.INDENT,
    TokenType.INDENT,
    TokenType.DEDENT,
    TokenType.DEDENT,
]

assert indent_tokens == expected, (
    f"Unexpected indentation tokens: {indent_tokens}"
)

print("\nNested indentation test passed!")
