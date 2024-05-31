from enum import Enum, auto
from typing import Union

class Location:
  def __init__(self, path:str, line:int, col:int):
    self.path = path
    self.line = line
    self.col = col

  def __repr__(self):
    return f'{self.path}:{self.line}:{self.col}'

class TokenType(Enum):
  EQ=auto()
  ASSIGN=auto()
  GT=auto()
  LT=auto()
  PLUS=auto()
  MINUS=auto()
  MUL=auto()
  DIV=auto()
  LPAREN=auto()
  RPAREN=auto()
  LBRACE=auto()
  RBRACE=auto()
  SEMI=auto()
  IF=auto()
  WHILE=auto()
  PRINT=auto()
  EOF=auto()
  NUMBER=auto()
  IDENTIFIER=auto()
  STRING=auto()

class Token:
  def __init__(self, type_:TokenType, value:Union[str, int], location:Location):
    self.type = type_
    self.value = value
    self.location = location

  def __repr__(self):
    return f'Token({repr(self.location)}, {self.type}, {repr(self.value)})'

class Lexer:
  def __init__(self, text):
    self.text = text
    self.pos = 0
    self.line = 1
    self.col = 1
    self.current_char = self.text[self.pos] if self.text else None

  def advance(self, count=1):
    self.pos += count
    self.col += count
    self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

  def skip_whitespace(self):
    while self.current_char is not None and self.current_char.isspace():
      if self.current_char == "\n":
        self.line += 1
        self.col = 0
      self.advance()

  def number(self) -> Token:
    result = ''
    while self.current_char is not None and self.current_char.isdigit():
      result += self.current_char
      self.advance()
    return Token(TokenType.NUMBER, int(result), Location("", self.line, self.col))

  def identifier(self) -> Token:
    result = ''
    while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_' or self.current_char == '$'):
      result += self.current_char
      self.advance()
    return Token(TokenType.IDENTIFIER, result, Location("", self.line, self.col))

  def string(self) -> Token:
    result = ''
    while self.current_char is not None and self.current_char != "\"":
      if self.current_char == "\\" and self.peek(1) == "\"":
        result += "\""
        self.advance(2)
      else:
        result += self.current_char
        self.advance()
    self.advance()
    return Token(TokenType.STRING, result, Location("", self.line, self.col))

  def get_next_token(self) -> Token:
    assert len(TokenType) == 20, "Exhaustive token handling in get_next_token."
    while self.current_char is not None:
      if self.current_char.isspace():
        self.skip_whitespace()
        continue
      if self.current_char == '=' and self.peek(1) == '=':
        self.advance(2)
        return Token(TokenType.EQ, '==', Location("", self.line, self.col))
      if self.current_char == '=':
        self.advance()
        return Token(TokenType.ASSIGN, '=', Location("", self.line, self.col))
      if self.current_char == '>':
        self.advance()
        return Token(TokenType.GT, '>', Location("", self.line, self.col))
      if self.current_char == '<':
        self.advance()
        return Token(TokenType.LT, '<', Location("", self.line, self.col))
      if self.current_char == '+':
        self.advance()
        return Token(TokenType.PLUS, '+', Location("", self.line, self.col))
      if self.current_char == '-':
        self.advance()
        return Token(TokenType.MINUS, '-', Location("", self.line, self.col))
      if self.current_char == '*':
        self.advance()
        return Token(TokenType.MUL, '*', Location("", self.line, self.col))
      if self.current_char == '/':
        self.advance()
        return Token(TokenType.DIV, '/', Location("", self.line, self.col))
      if self.current_char == '(':
        self.advance()
        return Token(TokenType.LPAREN, '(', Location("", self.line, self.col))
      if self.current_char == ')':
        self.advance()
        return Token(TokenType.RPAREN, ')', Location("", self.line, self.col))
      if self.current_char == '{':
        self.advance()
        return Token(TokenType.LBRACE, '{', Location("", self.line, self.col))
      if self.current_char == '}':
        self.advance()
        return Token(TokenType.RBRACE, '}', Location("", self.line, self.col))
      if self.current_char == ';':
        self.advance()
        return Token(TokenType.SEMI, ';', Location("", self.line, self.col))
      if self.current_char == '"':
        self.advance()
        return self.string()
      if self.current_char == 'i' and self.peek(1) == 'f':
        self.advance(2)
        return Token(TokenType.IF, 'if', Location("", self.line, self.col))
      if self.current_char == 'w' and self.peek(4) == 'hile':
        self.advance(5)
        return Token(TokenType.WHILE, 'while', Location("", self.line, self.col))
      if self.current_char == 'p' and self.peek(4) == 'rint':
        self.advance(5)
        return Token(TokenType.PRINT, 'print', Location("", self.line, self.col))
      if self.current_char.isdigit():
        return self.number()
      if self.current_char.isalpha() or self.current_char == '_':
        return self.identifier()
      raise Exception(f':{self.line}:{self.col} LEXER_ERROR: Unexpected character {self.current_char}')

    return Token(TokenType.EOF, None, Location("", self.line, self.col))

  def peek(self, count) -> str:
    peek_str = ''
    peek_pos = self.pos + 1
    left = count
    while peek_pos < len(self.text) and not left == 0:
      peek_str = peek_str + self.text[peek_pos]
      peek_pos = peek_pos + 1
      left = left - 1
    return peek_str
