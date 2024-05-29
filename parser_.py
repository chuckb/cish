from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Union
from lexer import TokenType, Location

class ASTVisitor(ABC):
  @abstractmethod
  def visit_number(self, number):
    pass

  @abstractmethod
  def visit_identifier(self, identifier):
    pass

  @abstractmethod
  def visit_statement_list(self, statement_list):
    pass

  @abstractmethod
  def visit_unary_condition(self, unary_condition):
    pass

  @abstractmethod
  def visit_binary_condition(self, binary_condition):
    pass

  @abstractmethod
  def visit_term_expression(self, term_expression):
    pass

  @abstractmethod
  def visit_binary_expression(self, binary_expression):
    pass

  @abstractmethod
  def visit_string(self, string):
    pass

  @abstractmethod
  def visit_string_expression(self, string_expression):
    pass

  @abstractmethod
  def visit_unary_term(self, unary_term):
    pass

  @abstractmethod
  def visit_binary_term(self, binary_term):
    pass

  @abstractmethod
  def visit_assignment(self, assignment):
    pass

  @abstractmethod
  def visit_if_statement(self, if_statement):
    pass

  @abstractmethod
  def visit_while_statement(self, while_statement):
    pass

  @abstractmethod
  def visit_print_statement(self, print_statement):
    pass

  @abstractmethod
  def visit_program(self, program):
    pass

class ASTNode(ABC):
  @abstractmethod
  def accept(self, visitor:ASTVisitor):
    pass

class NumberNode(ASTNode):
  def __init__(self, value:int):
    self.value = value

  def accept(self, visitor:ASTVisitor):
    return visitor.visit_number(self)

class IdentifierNode(ASTNode):
  def __init__(self, name:str):
    self.name = name  # Variable name

  def accept(self, visitor):
    return visitor.visit_identifier(self)

class StatementNode(ASTNode):
  pass

class StatementListNode(ASTNode):
  def __init__(self, statement:StatementNode):
    self.statements = []
    self.statements.append(statement)

  def accept(self, visitor:ASTVisitor):
    return visitor.visit_statement_list(self)
  
  def append(self, statement: StatementNode):
    self.statements.append(statement)

class ConditionNode(ASTNode):
   pass

class ExpressionNode(ASTNode):
   pass

class RelOpType(Enum):
   EQ=auto()
   GT=auto()
   LT=auto()

class UnaryConditionNode(ConditionNode):
  def __init__(self, expression:ExpressionNode):
    self.expression = expression

  def accept(self, visitor:ASTVisitor):
    return visitor.visit_unary_condition(self)

class BinaryConditionNode(ConditionNode):
  def __init__(self, first_expression:ExpressionNode, relop:RelOpType, second_expression:ExpressionNode):
    self.first_expression = first_expression
    self.relop = relop
    self.second_expression = second_expression

  def accept(self, visitor:ASTVisitor):
    return visitor.visit_binary_condition(self)

class TermNode(ASTNode):
   pass

class TermExpressionNode(ExpressionNode):
  def __init__(self, term:TermNode):
    self.term = term

  def accept(self, visitor:ASTVisitor):
    return visitor.visit_term_expression(self)

class ExpOpType(Enum):
   PLUS=auto()
   MINUS=auto()

class BinaryExpressionNode(ExpressionNode):
  def __init__(self, term:TermNode, exp_op:ExpOpType, expression:ExpressionNode):
    self.term = term
    self.exp_op = exp_op
    self.expression = expression

  def accept(self, visitor:ASTVisitor):
    return visitor.visit_binary_expression(self)

class StringNode(ASTNode):
  def __init__(self, value:str):
    self.value = value

  def accept(self, visitor:ASTVisitor):
    return visitor.visit_string(self)

class StringExpressionNode(ExpressionNode):
  def __init__(self, string:StringNode):
    self.string = string

  def accept(self, visitor:ASTVisitor):
    return visitor.visit_string_expression(self)

class FactorNode(ASTNode):
  def __init__(self, node:Union[NumberNode, IdentifierNode, StringNode, ExpressionNode]):
    self.node = node

  def accept(self, visitor:ASTVisitor):
    return visitor.visit_factor(self)

class UnaryTermNode(TermNode):
  def __init__(self, factor:FactorNode):
    self.factor = factor

  def accept(self, visitor:ASTVisitor):
    return visitor.visit_unary_term(self)

class TermOpType(Enum):
   MUL=auto()
   DIV=auto()

class BinaryTermNode(TermNode):
  def __init__(self, factor:FactorNode, term_op:TermOpType, term:TermNode):
    self.factor = factor
    self.term_op = term_op
    self.term = term

  def accept(self, visitor:ASTVisitor):
    return visitor.visit_binary_term(self)

class IfStatementNode(StatementNode):
  def __init__(self, condition:ConditionNode, statement_list:StatementListNode):
    self.condition = condition
    self.statement_list = statement_list

  def accept(self, visitor:ASTVisitor):
    return visitor.visit_if_statement(self)

class WhileStatementNode(StatementNode):
  def __init__(self, condition:ConditionNode, statement_list:StatementListNode):
    self.condition = condition
    self.statement_list = statement_list
    
  def accept(self, visitor:ASTVisitor):
    return visitor.visit_while_statement(self)

class PrintStatementNode(StatementNode):
  def __init__(self, expression:ExpressionNode):
    self.expression = expression
    
  def accept(self, visitor:ASTVisitor):
    return visitor.visit_print_statement(self)

class ProgramNode(ASTNode):
  def __init__(self, statement_list:StatementListNode):
    self.statement_list = statement_list

  def accept(self, visitor:ASTVisitor):
    return visitor.visit_program(self)
        
class AssignmentNode(StatementNode):
  def __init__(self, identifier:IdentifierNode, value:ExpressionNode):
    self.identifier = identifier
    self.value = value  # Expression node

  def accept(self, visitor):
    return visitor.visit_assignment(self)
            
class Parser:
  def __init__(self, lexer):
    self.lexer = lexer
    self.current_token = self.lexer.get_next_token()

  def error(self, location:Location):
    raise Exception(f'{location.path}:{location.line}:{location.col} PARSER_ERROR: Invalid syntax')

  def eat(self, token_type):
    if self.current_token.type == token_type:
      self.current_token = self.lexer.get_next_token()
    else:
      self.error(self.current_token.location)

  def factor(self) -> Union[NumberNode, IdentifierNode, StringNode, ExpressionNode]:
    token = self.current_token
    node = Union[NumberNode, IdentifierNode, StringNode, ExpressionNode]
    if token.type == TokenType.NUMBER:
      self.eat(TokenType.NUMBER)
      node = NumberNode(token.value)
    elif token.type == TokenType.STRING:
      self.eat(TokenType.STRING)
      node = StringNode(token.value)
    elif token.type == TokenType.IDENTIFIER:
      self.eat(TokenType.IDENTIFIER)
      node = IdentifierNode(token.value)
    elif token.type == TokenType.LPAREN:
      self.eat(TokenType.LPAREN)
      node = self.expression()
      self.eat(TokenType.RPAREN)
    else:
      self.error(self.current_token.location)
    return node

  def term(self) -> Union[BinaryTermNode, UnaryTermNode]:
    factor = self.factor()
    if self.current_token.type in (TokenType.MUL, TokenType.DIV):
      assert len(TermOpType) == 2, "Non-exhaustive token handling in term."
      token = self.current_token
      self.eat(TokenType.MUL) if token.type == TokenType.MUL else self.eat(TokenType.DIV)
      return BinaryTermNode(factor, TermOpType.MUL if token.type == TokenType.MUL else TermOpType.DIV, self.term())
    else:
      return UnaryTermNode(factor)

  def expression(self) -> Union[StringExpressionNode, TermExpressionNode, BinaryExpressionNode]:
    if self.current_token.type == TokenType.STRING:
      token = self.current_token
      self.eat(TokenType.STRING)
      return StringExpressionNode(StringNode(token.value))
    else:
      term = self.term()
      assert len(ExpOpType) == 2, "Non-exhaustive token handling in expression."
      if self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
        token = self.current_token
        self.eat(TokenType.PLUS) if token.type == TokenType.PLUS else self.eat(TokenType.MINUS)
        return BinaryExpressionNode(term, ExpOpType.PLUS if token.type == TokenType.PLUS else ExpOpType.MINUS, self.expression())
      else:
        return TermExpressionNode(term)
      
  def assignment(self) -> AssignmentNode:
    identifier = IdentifierNode(self.current_token.value)
    self.eat(TokenType.IDENTIFIER)
    self.eat(TokenType.ASSIGN)
    expression = self.expression()
    self.eat(TokenType.SEMI)
    return AssignmentNode(identifier, expression)

  def condition(self) -> Union[BinaryConditionNode, UnaryConditionNode]:
    expression = self.expression()
    token = self.current_token
    assert len(RelOpType) == 3, "Non-exhaustive token handling in condition."
    if token.type == TokenType.EQ:
        self.eat(TokenType.EQ)
        return BinaryConditionNode(expression, RelOpType.EQ, self.expression())
    elif token.type == TokenType.LT:
        self.eat(TokenType.LT)
        return BinaryConditionNode(expression, RelOpType.LT, self.expression())
    elif token.type == TokenType.GT:
        self.eat(TokenType.GT)
        return BinaryConditionNode(expression, RelOpType.GT, self.expression())
    else:
        UnaryConditionNode(expression)
        
  def if_statement(self) -> IfStatementNode:
    self.eat(TokenType.IF)
    self.eat(TokenType.LPAREN)
    condition = self.condition()
    self.eat(TokenType.RPAREN)
    self.eat(TokenType.LBRACE)
    statement_list = self.statement_list()
    self.eat(TokenType.RBRACE)
    return IfStatementNode(condition, statement_list)

  def while_statement(self) -> WhileStatementNode:
    self.eat(TokenType.WHILE)
    self.eat(TokenType.LPAREN)
    condition = self.condition()
    self.eat(TokenType.RPAREN)
    self.eat(TokenType.LBRACE)
    statement_list = self.statement_list()
    self.eat(TokenType.RBRACE)
    return WhileStatementNode(condition, statement_list)

  def print_statement(self) -> PrintStatementNode:
    self.eat(TokenType.PRINT)
    self.eat(TokenType.LPAREN)
    expression = self.expression()
    self.eat(TokenType.RPAREN)
    self.eat(TokenType.SEMI)
    return PrintStatementNode(expression)

  def statement(self) -> Union[AssignmentNode, PrintStatementNode, IfStatementNode, WhileStatementNode]:
    if self.current_token.type == TokenType.IDENTIFIER:
      return self.assignment()
    elif self.current_token.type == TokenType.IF:
      return self.if_statement()
    elif self.current_token.type == TokenType.WHILE:
      return self.while_statement()
    elif self.current_token.type == TokenType.PRINT:
      return self.print_statement()
    else:
      self.error()

  def statement_list(self) -> StatementListNode:
    statement = self.statement()
    statement_list = StatementListNode(statement)
    while self.current_token.type != TokenType.RBRACE and self.current_token.type != TokenType.EOF:
      statement = self.statement()
      statement_list.append(statement)
    return statement_list

  def parse(self) -> ProgramNode:
    statement_list = self.statement_list()
    return ProgramNode(statement_list)
