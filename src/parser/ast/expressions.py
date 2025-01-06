from __future__ import annotations
from dataclasses import dataclass, field

from parser.ast.base import AST
from parser.ast.targets import TargetAST


@dataclass(kw_only=True)
class ExpressionAST(AST):
    pass


@dataclass(kw_only=True)
class ConditionalExpressionAST(ExpressionAST):
    condition: ExpressionAST
    then_expression: ExpressionAST
    else_expression: ExpressionAST

    def __str__(self) -> str:
        return f"{self.then_expression} if {self.condition} else {self.else_expression}"


@dataclass(kw_only=True)
class BinaryExpressionAST(ExpressionAST):
    left: ExpressionAST
    operator: str
    right: ExpressionAST

    def __str__(self) -> str:
        return f"{self.left} {self.operator} {self.right}"


@dataclass(kw_only=True)
class UnaryExpressionAST(ExpressionAST):
    expression: ExpressionAST
    operator: str

    def __str__(self) -> str:
        return f"{self.operator}{self.expression}"


@dataclass(kw_only=True)
class AwaitExpressionAST(ExpressionAST):
    expression: ExpressionAST

    def __str__(self) -> str:
        return f"await {self.expression}"


@dataclass(kw_only=True)
class NameExpressionAST(ExpressionAST, TargetAST):
    expression: ExpressionAST
    name: str

    def __str__(self) -> str:
        return f"{self.expression}.{self.name}"


@dataclass(kw_only=True)
class CallExpressionAST(ExpressionAST):
    expression: ExpressionAST
    arguments: list[CallExpressionArgumentAST] = field(default_factory=list)

    def __str__(self) -> str:
        arguments = ", ".join(str(argument) for argument in self.arguments)
        return f"{self.expression}({arguments})"


@dataclass(kw_only=True)
class CallExpressionArgumentAST(AST):
    name: str | None = None
    expression: ExpressionAST

    def __str__(self) -> str:
        return f"{self.name}={self.expression}" if self.name else str(self.expression)


@dataclass(kw_only=True)
class SubscriptExpressionAST(ExpressionAST):
    expression: ExpressionAST
    slices: list[SliceAST]

    def __str__(self) -> str:
        slices = "".join(f"[{slice}]" for slice in self.slices)
        return f"{self.expression}{slices}"


@dataclass(kw_only=True)
class LiteralExpressionAST(ExpressionAST):
    pass


@dataclass(kw_only=True)
class NameLiteralExpressionAST(LiteralExpressionAST, TargetAST):
    value: str

    def __str__(self) -> str:
        return self.value


@dataclass(kw_only=True)
class BooleanLiteralExpressionAST(LiteralExpressionAST):
    value: bool

    def __str__(self) -> str:
        return "True" if self.value else "False"


@dataclass(kw_only=True)
class NoneLiteralExpressionAST(LiteralExpressionAST):
    def __str__(self) -> str:
        return "None"


@dataclass(kw_only=True)
class StringLiteralExpressionAST(LiteralExpressionAST):
    value: str

    def __str__(self) -> str:
        return f'"{self.value}"'


@dataclass(kw_only=True)
class FStringLiteralExpressionAST(LiteralExpressionAST):
    def __str__(self) -> str:
        return f'f""'


@dataclass(kw_only=True)
class ListExpressionAST(ExpressionAST):
    elements: list[ExpressionAST]

    def __str__(self) -> str:
        elements = ", ".join(str(element) for element in self.elements)
        return f"[{elements}]"


@dataclass(kw_only=True)
class SliceAST(AST):
    start: ExpressionAST | None = None
    stop: ExpressionAST | None = None
    step: ExpressionAST | None = None

    def __str__(self) -> str:
        values = ":".join(
            str(value) for value in [self.start, self.stop, self.step] if value
        )
        return values


@dataclass(kw_only=True)
class CombinatoryStringLiteralExpressionAST(LiteralExpressionAST):
    values: list[StringLiteralExpressionAST | FStringLiteralExpressionAST]

    def __str__(self) -> str:
        values = " ".join(str(value) for value in self.values)
        return values


@dataclass(kw_only=True)
class NumberLiteralExpressionAST(LiteralExpressionAST):
    value: int | float

    def __str__(self) -> str:
        return str(self.value)


@dataclass(kw_only=True)
class ListComprehensionExpressionAST(ExpressionAST):
    expression: ExpressionAST
    clauses: list[ListComprehensionForIfClauseAST]

    def __str__(self) -> str:
        clauses = "".join(str(clause) for clause in self.clauses)
        return f"[{self.expression}{clauses}]"


@dataclass(kw_only=True)
class ListComprehensionForIfClauseAST(AST):
    is_async: bool
    targets: list[TargetAST]
    iterator: ExpressionAST
    condition: ExpressionAST | None = None

    def __str__(self) -> str:
        targets = ", ".join(str(target) for target in self.targets)
        condition = f" if {self.condition}" if self.condition else ""
        return f" for {targets} in {self.iterator}{condition}"
