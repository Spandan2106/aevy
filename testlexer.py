from src.aevy.lexer import Lexer

source = '''name = "Aevy"
age = 20
price = 99.5
active = True
'''

for token in Lexer(source).scan_tokens():
    print(token)