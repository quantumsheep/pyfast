from parser.ast import ProgramAST

from antlr4 import CommonTokenStream, FileStream

from .grammar.PythonLexer import PythonLexer
from .grammar.PythonParser import PythonParser
from .visitor import Visitor


class SyntaxError(Exception):
    def __init__(self, message: str):
        self.message = message


def parse(filename: str) -> ProgramAST:
    input_stream = FileStream(filename)
    lexer = PythonLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = PythonParser(stream)
    tree = parser.file_input()

    if parser.getNumberOfSyntaxErrors() > 0:
        raise SyntaxError("Syntax error")

    v = Visitor()
    program_ast = v.visitFile_input(tree)

    return program_ast
