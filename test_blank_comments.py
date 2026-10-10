
from src.aevy.lexer import Lexer
from src.aevy.token import TokenType

source = '''if age >= 18:

    // This is a comment

    show("Adult")

show("Done")
'''

tokens = Lexer(source).scan_tokens()

for token in tokens:
    print(token)

indent_tokens = [
    token.type
    for token in tokens
    if token.type in (TokenType.INDENT, TokenType.DEDENT)
]

assert indent_tokens == [
    TokenType.INDENT,
    TokenType.DEDENT,
], f"Unexpected indentation tokens: {indent_tokens}"

print("\nBlank lines and comments test passed!")
