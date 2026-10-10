
from src.aevy.lexer import Lexer

source = '''if age >= 18:
    show("First")
  show("Second")
'''

try:
    tokens = Lexer(source).scan_tokens()
    print("ERROR: Invalid indentation was accepted.")
    for token in tokens:
        print(token)
except SyntaxError as error:
    print("Invalid indentation correctly rejected!")
    print(error)
