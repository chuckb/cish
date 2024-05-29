from lexer import Lexer
from parser_ import Parser
from interpreter import Interpreter

# Example usage:
if __name__ == '__main__':
  text = '''
  s = "Hello World!";
  print(s);
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
  parser = Parser(lexer)
  program = parser.parse()
  interpreter = Interpreter()
  program.accept(interpreter)