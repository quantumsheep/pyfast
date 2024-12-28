from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class ProgramAST:
    filename: str = ""
    statements: list[StatementAST]


@dataclass(kw_only=True)
class StatementAST:
    pass


@dataclass(kw_only=True)
class MultipleStatementAST[T: StatementAST](StatementAST):
    statements: list[T]


@dataclass(kw_only=True)
class FunctionDefinitionStatementAST(StatementAST):
    is_async: bool
    name: str
    type_parameters: list[TypeParameterAST] = field(default_factory=list)
    parameters: list[FunctionDefinitionParameterAST] = field(default_factory=list)
    return_type: ExpressionAST | None = None
    body: list[StatementAST]


@dataclass(kw_only=True)
class FunctionDefinitionParameterAST:
    keyword_only: bool = False
    unpacked: bool = False
    name: str
    default_value: ExpressionAST | None = None


@dataclass(kw_only=True)
class TypeParameterAST:
    name: str
    bound: ExpressionAST | None = None


@dataclass(kw_only=True)
class WhileStatementAST(StatementAST):
    condition: ExpressionAST
    body: list[StatementAST]
    else_body: list[StatementAST] = field(default_factory=list)


@dataclass(kw_only=True)
class ForStatementAST(StatementAST):
    is_async: bool
    targets: list[TargetAST]
    iterators: list[ExpressionAST]
    body: list[StatementAST]
    else_body: list[StatementAST] = field(default_factory=list)


@dataclass(kw_only=True)
class TargetAST:
    pass


@dataclass(kw_only=True)
class UnpackTargetAST(TargetAST):
    target: TargetAST


@dataclass(kw_only=True)
class IfStatementAST(StatementAST):
    condition: ExpressionAST
    body: list[StatementAST]
    else_body: list[StatementAST] = field(default_factory=list)


@dataclass(kw_only=True)
class NameTargetAST(TargetAST):
    name: str


@dataclass(kw_only=True)
class PassStatementAST(StatementAST):
    pass


@dataclass(kw_only=True)
class BreakStatementAST(StatementAST):
    pass


@dataclass(kw_only=True)
class ContinueStatementAST(StatementAST):
    pass


@dataclass(kw_only=True)
class ImportStatementAST(StatementAST):
    path: list[str]
    alias: str | None = None


@dataclass(kw_only=True)
class ExpressionsStatementAST(StatementAST):
    expressions: list[ExpressionAST]


@dataclass(kw_only=True)
class ExpressionAST:
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
class NameExpressionAST(ExpressionAST):
    expression: ExpressionAST
    name: str


@dataclass(kw_only=True)
class CallExpressionAST(ExpressionAST):
    expression: ExpressionAST
    arguments: list[CallExpressionArgumentAST] = field(default_factory=list)


@dataclass(kw_only=True)
class CallExpressionArgumentAST:
    name: str | None = None
    expression: ExpressionAST


@dataclass(kw_only=True)
class SubscriptExpressionAST(ExpressionAST):
    expression: ExpressionAST
    slices: list[ExpressionAST]


@dataclass(kw_only=True)
class LiteralExpressionAST(ExpressionAST):
    pass


@dataclass(kw_only=True)
class NameLiteralExpressionAST(LiteralExpressionAST):
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
class CombinatoryStringLiteralExpressionAST(LiteralExpressionAST):
    values: list[StringLiteralExpressionAST | FStringLiteralExpressionAST]


@dataclass(kw_only=True)
class NumberLiteralExpressionAST(LiteralExpressionAST):
    value: int | float
