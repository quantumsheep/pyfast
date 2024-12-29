from dataclasses import dataclass
from parser.ast.base import SourceFile
from parser.ast.statements import StatementAST


@dataclass(kw_only=True)
class ProgramAST:
    file: SourceFile
    statements: list[StatementAST]
