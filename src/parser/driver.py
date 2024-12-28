from parser.ast.ast import ProgramAST

from antlr4 import CommonTokenStream, FileStream

from .grammar.PythonLexer import PythonLexer
from .grammar.PythonParser import PythonParser
from .visitor import Visitor


class SyntaxError(Exception):
    def __init__(self, message: str):
        self.message = message


def parse_one(filepath: str) -> ProgramAST:
    input_stream = FileStream(filepath)
    lexer = PythonLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = PythonParser(stream)
    tree = parser.file_input()

    if parser.getNumberOfSyntaxErrors() > 0:
        raise SyntaxError("Syntax error")

    v = Visitor()
    program_ast = v.visitFile_input(tree)
    program_ast.filepath = filepath

    return program_ast


def parse(files: list[str]) -> list[ProgramAST]:
    asts = list[ProgramAST]()

    for file in files:
        ast = parse_one(file)
        asts.append(ast)

    return asts
