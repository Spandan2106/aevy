
from src.aevy.lexer import Lexer
from src.aevy.token import TokenType

source = '''func greet() {
    show("Hello")
}

if True:
    show("Inside if")

show("Done")
'''

tokens = Lexer(source).scan_tokens()

for token in tokens:
    print(token)

indent_count = sum(
    1 for token in tokens if token.type == TokenType.INDENT
)
dedent_count = sum(
    1 for token in tokens if token.type == TokenType.DEDENT
)

assert indent_count == 2, (
    f"Expected 2 INDENT tokens, got {indent_count}"
)
assert dedent_count == 2, (
    f"Expected 2 DEDENT tokens, got {dedent_count}"
)

print("\nBraces and indentation test passed!")
