from __future__ import annotations
from dataclasses import dataclass, field

from parser.ast.base import AST
from parser.ast.expressions import ExpressionAST
from parser.ast.targets import TargetAST


@dataclass(kw_only=True)
class StatementAST(AST):
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
class FunctionDefinitionParameterAST(AST):
    variadic: bool = False
    keywords: bool = False
    name: str
    annotation: ExpressionAST | None = None
    default_value: ExpressionAST | None = None


@dataclass(kw_only=True)
class TypeParameterAST(AST):
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
class IfStatementAST(StatementAST):
    condition: ExpressionAST
    body: list[StatementAST]
    else_body: list[StatementAST] = field(default_factory=list)


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
class ReturnStatementAST(StatementAST):
    expressions: list[ExpressionAST] = field(default_factory=list)


@dataclass(kw_only=True)
class ImportStatementAST(StatementAST):
    path: list[str]
    alias: str | None = None


@dataclass(kw_only=True)
class ExpressionsStatementAST(StatementAST):
    expressions: list[ExpressionAST]


@dataclass(kw_only=True)
class ClassDefinitionStatementAST(StatementAST):
    name: str
    body: list[StatementAST]


@dataclass(kw_only=True)
class AssignmentStatementAST(StatementAST):
    targets: list[TargetAST]
    type: ExpressionAST | None = None
    operator: str | None = None
    values: list[ExpressionAST]


@dataclass(kw_only=True)
class RaiseStatementAST(StatementAST):
    expression: ExpressionAST | None = None
    from_expression: ExpressionAST | None = None
