from dataclasses import dataclass
from parser.ast.base import SourceFile
from parser.ast.statements import MultipleStatementAST, StatementAST


@dataclass(kw_only=True)
class ProgramAST:
    file: SourceFile
    statements: MultipleStatementAST[StatementAST]

    def __str__(self) -> str:
        return str(self.statements)
