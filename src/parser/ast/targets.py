from dataclasses import dataclass

from parser.ast.base import AST


@dataclass(kw_only=True)
class TargetAST(AST):
    pass


@dataclass(kw_only=True)
class UnpackTargetAST(TargetAST):
    target: TargetAST

    def __str__(self) -> str:
        return f"*{self.target}"
