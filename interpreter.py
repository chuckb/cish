from parser_ import *

class Interpreter(ASTVisitor):
  def __init__(self, context = {"strings":{}, "ints":{}}):
    self.variables = context

  def error(self):
    #TODO: Add location information
    raise Exception('Invalid syntax')

  def visit_number(self, number:NumberNode) -> int:
    return number.value

  def visit_string_identifier(self, identifier:StringIdentifierNode) -> str:
    return self.variables["strings"][identifier.name]

  def visit_int_identifier(self, identifier:IntIdentifierNode) -> int:
    return self.variables["ints"][identifier.name]

  def visit_unary_condition(self, unary_condition:UnaryConditionNode) -> bool:
    return unary_condition.expression.accept(self)

  def visit_binary_condition(self, binary_condition:BinaryConditionNode) -> bool:
    #TODO: Number vs. string comparison type checking?
    assert len(RelOpType) == 3, "Non-exhaustive token handling in visit_binary_condition."
    if binary_condition.relop == RelOpType.EQ:
      return binary_condition.first_expression.accept(self) == binary_condition.second_expression.accept(self)
    elif binary_condition.relop == RelOpType.GT:
      return binary_condition.first_expression.accept(self) > binary_condition.second_expression.accept(self)
    elif binary_condition.relop == RelOpType.LT:
      return binary_condition.first_expression.accept(self) < binary_condition.second_expression.accept(self)

  def visit_term_expression(self, term_expression:TermExpressionNode) -> int:
    return term_expression.term.accept(self)

  def visit_binary_expression(self, binary_expression:BinaryExpressionNode) -> int:
    #TODO: Number vs. string type checking?
    assert len(ExpOpType) == 2, "Non-exhaustive token handling in visit_binary_expression."
    if binary_expression.exp_op == ExpOpType.PLUS:
      return binary_expression.term.accept(self) + binary_expression.expression.accept(self)
    else:
      return binary_expression.term.accept(self) - binary_expression.expression.accept(self)

  def visit_string(self, string:StringNode) -> str:
    return string.value

  def visit_string_expression(self, string_expression:StringExpressionNode) -> str:
    return string_expression.string.accept(self)

  def visit_unary_term(self, unary_term:UnaryTermNode) -> int:
    return unary_term.factor.accept(self)

  def visit_binary_term(self, binary_term:BinaryTermNode) -> int:
    assert len(TermOpType) == 2, "Non-exhaustive token handling in visit_binary_term."
    if binary_term.term_op == TermOpType.MUL:
      return binary_term.factor.accept(self) * binary_term.term.accept(self)
    else:
      return binary_term.factor.accept(self) / binary_term.term.accept(self)

  def visit_assignment(self, assignment:AssignmentNode):
    identifier = assignment.identifier.name
    value = assignment.value.accept(self)
    if type(assignment.identifier) is StringIdentifierNode:
      if type(value) is str:
        self.variables["strings"][identifier] = value
      else:
         #TODO: Add location to message
         raise Exception("Type exception")
    elif type(assignment.identifier) is IntIdentifierNode:
      if type(value) is int:
        self.variables["ints"][identifier] = value
      else:
        #TODO: Add location to message
        raise Exception("Type exception")
    else:
      assert False, "Non-exhaustive type handling in visit_assignment"

  def visit_if_statement(self, if_statement:IfStatementNode):
    if if_statement.condition.accept(self):
      for statement in if_statement.statement_list.statements:
        statement.accept(self)

  def visit_while_statement(self, while_statement:WhileStatementNode):
    while(while_statement.condition.accept(self)):
      for statement in while_statement.statement_list.statements:
        statement.accept(self)

  def visit_print_statement(self, print_statement:PrintStatementNode):
    expression = print_statement.expression.accept(self)
    print(expression)

  def visit_statement_list(self, statement_list:StatementListNode):
    for statement in statement_list.statements:
      statement.accept(self)

  def visit_program(self, program:ProgramNode):
    program.statement_list.accept(self)
