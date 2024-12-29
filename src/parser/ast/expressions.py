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


@dataclass(kw_only=True)
class BinaryExpressionAST(ExpressionAST):
    left: ExpressionAST
    operator: str
    right: ExpressionAST


@dataclass(kw_only=True)
class UnaryExpressionAST(ExpressionAST):
    expression: ExpressionAST
    operator: str


@dataclass(kw_only=True)
class AwaitExpressionAST(ExpressionAST):
    expression: ExpressionAST


@dataclass(kw_only=True)
class NameExpressionAST(ExpressionAST, TargetAST):
    expression: ExpressionAST
    name: str


@dataclass(kw_only=True)
class CallExpressionAST(ExpressionAST):
    expression: ExpressionAST
    arguments: list[CallExpressionArgumentAST] = field(default_factory=list)


@dataclass(kw_only=True)
class CallExpressionArgumentAST(AST):
    name: str | None = None
    expression: ExpressionAST


@dataclass(kw_only=True)
class SubscriptExpressionAST(ExpressionAST):
    expression: ExpressionAST
    slices: list[SliceAST]


@dataclass(kw_only=True)
class LiteralExpressionAST(ExpressionAST):
    pass


@dataclass(kw_only=True)
class NameLiteralExpressionAST(LiteralExpressionAST, TargetAST):
    value: str


@dataclass(kw_only=True)
class BooleanLiteralExpressionAST(LiteralExpressionAST):
    value: bool


@dataclass(kw_only=True)
class NoneLiteralExpressionAST(LiteralExpressionAST):
    pass


@dataclass(kw_only=True)
class StringLiteralExpressionAST(LiteralExpressionAST):
    value: str


@dataclass(kw_only=True)
class FStringLiteralExpressionAST(LiteralExpressionAST):
    pass


@dataclass(kw_only=True)
class ListExpressionAST(ExpressionAST):
    elements: list[ExpressionAST]


@dataclass(kw_only=True)
class SliceExpressionAST(ExpressionAST):
    expression: ExpressionAST
    slices: list[SliceAST]


@dataclass(kw_only=True)
class SliceAST(AST):
    start: ExpressionAST | None = None
    stop: ExpressionAST | None = None
    step: ExpressionAST | None = None


@dataclass(kw_only=True)
class CombinatoryStringLiteralExpressionAST(LiteralExpressionAST):
    values: list[StringLiteralExpressionAST | FStringLiteralExpressionAST]


@dataclass(kw_only=True)
class NumberLiteralExpressionAST(LiteralExpressionAST):
    value: int | float


@dataclass(kw_only=True)
class ListComprehensionExpressionAST(ExpressionAST):
    expression: ExpressionAST
    clauses: list[ListComprehensionForIfClauseAST]


@dataclass(kw_only=True)
class ListComprehensionForIfClauseAST(AST):
    is_async: bool
    targets: list[TargetAST]
    iterator: ExpressionAST
    condition: ExpressionAST | None = None
