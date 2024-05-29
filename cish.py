import re

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)})'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token('NUMBER', int(result))

    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return Token('IDENTIFIER', result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return self.number()
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()
            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token('EQ', '==')
            if self.current_char == '=':
                self.advance()
                return Token('ASSIGN', '=')
            if self.current_char == '+':
                self.advance()
                return Token('PLUS', '+')
            if self.current_char == '-':
                self.advance()
                return Token('MINUS', '-')
            if self.current_char == '*':
                self.advance()
                return Token('MUL', '*')
            if self.current_char == '/':
                self.advance()
                return Token('DIV', '/')
            if self.current_char == '>':
                self.advance()
                return Token('GT', '>')
            if self.current_char == '<':
                self.advance()
                return Token('LT', '<')
            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')
            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')
            if self.current_char == '{':
                self.advance()
                return Token('LBRACE', '{')
            if self.current_char == '}':
                self.advance()
                return Token('RBRACE', '}')
            if self.current_char == ';':
                self.advance()
                return Token('SEMI', ';')
            if self.current_char == '"':
                self.advance()
                return Token('QUOTE', '"')
            if self.current_char == 'i' and self.peek() == 'f':
                self.advance()
                self.advance()
                return Token('IF', 'if')
            if self.current_char == 'w' and self.peek() == 'hile':
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token('WHILE', 'while')
            if self.current_char == 'p' and self.peek() == 'rint':
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                return Token('PRINT', 'print')
            raise Exception(f'Unexpected character {self.current_char}')

        return Token('EOF', None)

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]

class Interpreter:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.variables = {}

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return token.value
        elif token.type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            if token.value in self.variables:
                return self.variables[token.value]
            else:
                raise Exception(f'Undefined variable {token.value}')
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            result = self.expr()
            self.eat('RPAREN')
            return result

    def term(self):
        result = self.factor()
        while self.current_token.type in ('MUL', 'DIV'):
            token = self.current_token
            if token.type == 'MUL':
                self.eat('MUL')
                result *= self.factor()
            elif token.type == 'DIV':
                self.eat('DIV')
                result /= self.factor()
        return result

    def expr(self):
        result = self.term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            token = self.current_token
            if token.type == 'PLUS':
                self.eat('PLUS')
                result += self.term()
            elif token.type == 'MINUS':
                self.eat('MINUS')
                result -= self.term()
        return result

    def condition(self):
        left = self.expr()
        token = self.current_token
        if token.type == 'EQ':
            self.eat('EQ')
        elif token.type == 'LT':
            self.eat('LT')
        elif token.type == 'GT':
            self.eat('GT')
        else:
            self.error()
        right = self.expr()
        if token.type == 'EQ':
            return left == right
        elif token.type == 'LT':
            return left < right
        elif token.type == 'GT':
            return left > right

    def assignment(self):
        var_name = self.current_token.value
        self.eat('IDENTIFIER')
        self.eat('ASSIGN')
        var_value = self.expr()
        self.eat('SEMI')
        self.variables[var_name] = var_value

    def if_statement(self):
        self.eat('IF')
        self.eat('LPAREN')
        condition = self.condition()
        self.eat('RPAREN')
        self.eat('LBRACE')
        if condition:
            self.statement_list()
        self.eat('RBRACE')

    def while_statement(self):
        self.eat('WHILE')
        self.eat('LPAREN')
        condition_expr = self.condition
        self.eat('RPAREN')
        self.eat('LBRACE')
        while condition_expr():
            self.statement_list()
        self.eat('RBRACE')

    def print_statement(self):
        self.eat('PRINT')
        self.eat('LPAREN')
        value = self.expr()
        self.eat('RPAREN')
        self.eat('SEMI')
        print(value)

    def statement(self):
        if self.current_token.type == 'IDENTIFIER':
            self.assignment()
        elif self.current_token.type == 'IF':
            self.if_statement()
        elif self.current_token.type == 'WHILE':
            self.while_statement()
        elif self.current_token.type == 'PRINT':
            self.print_statement()
        else:
            self.error()

    def statement_list(self):
        while self.current_token.type not in ('RBRACE', 'EOF'):
            self.statement()

    def interpret(self):
        self.statement_list()

# Example usage:
if __name__ == '__main__':
    text = '''
    x = 10;
    y = 20;
    print(x + y);
    if (x < y) {
        print("x is less than y");
    }
    while (x < y) {
        x = x + 1;
        print(x);
    }
    '''
    lexer = Lexer(text)
    interpreter = Interpreter(lexer)
    interpreter.interpret()
