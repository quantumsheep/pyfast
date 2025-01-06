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

    def __str__(self) -> str:
        return "\n".join(map(str, self.statements))


@dataclass(kw_only=True)
class FunctionDefinitionStatementAST(StatementAST):
    is_async: bool
    name: str
    type_parameters: list[TypeParameterAST] = field(default_factory=list)
    parameters: list[FunctionDefinitionParameterAST] = field(default_factory=list)
    return_type: ExpressionAST | None = None
    body: MultipleStatementAST

    def __str__(self) -> str:
        parameters = ", ".join(map(str, self.parameters))

        lines = str(self.body).split("\n")
        body = "\n".join(map(lambda line: f"    {line}", lines))

        return f"def {self.name}({parameters}) -> {self.return_type}:\n{body}"


@dataclass(kw_only=True)
class FunctionDefinitionParameterAST(AST):
    variadic: bool = False
    keywords: bool = False
    name: str
    annotation: ExpressionAST | None = None
    default_value: ExpressionAST | None = None

    def __str__(self) -> str:
        if self.default_value:
            return f"{self.name}: {self.annotation} = {self.default_value}"
        if self.annotation:
            return f"{self.name}: {self.annotation}"
        return self.name


@dataclass(kw_only=True)
class TypeParameterAST(AST):
    name: str
    bound: ExpressionAST | None = None

    def __str__(self) -> str:
        return f"{self.name}: {self.bound}" if self.bound else self.name


@dataclass(kw_only=True)
class WhileStatementAST(StatementAST):
    condition: ExpressionAST
    body: MultipleStatementAST
    else_body: MultipleStatementAST | None = None

    def __str__(self) -> str:
        lines = str(self.body).split("\n")
        body = "\n".join(map(lambda line: f"    {line}", lines))

        if self.else_body:
            lines = str(self.else_body).split("\n")
            else_body = "\n".join(map(lambda line: f"    {line}", lines))
            return f"while {self.condition}:\n{body}\nelse:\n{else_body}"

        return f"while {self.condition}:\n{body}"


@dataclass(kw_only=True)
class ForStatementAST(StatementAST):
    is_async: bool
    targets: list[TargetAST]
    iterators: list[ExpressionAST]
    body: MultipleStatementAST
    else_body: MultipleStatementAST | None = None

    def __str__(self) -> str:
        targets = ", ".join(map(str, self.targets))
        iterators = ", ".join(map(str, self.iterators))

        lines = str(self.body).split("\n")
        body = "\n".join(map(lambda line: f"    {line}", lines))

        if self.else_body:
            lines = str(self.else_body).split("\n")
            else_body = "\n".join(map(lambda line: f"    {line}", lines))
            return f"for {targets} in {iterators}:\n{body}\nelse:\n{else_body}"

        return f"for {targets} in {iterators}:\n{body}"


@dataclass(kw_only=True)
class IfStatementAST(StatementAST):
    condition: ExpressionAST
    body: MultipleStatementAST
    else_body: MultipleStatementAST | None = None

    def __str__(self) -> str:
        lines = str(self.body).split("\n")
        body = "\n".join(map(lambda line: f"    {line}", lines))

        if self.else_body:
            lines = str(self.else_body).split("\n")
            else_body = "\n".join(map(lambda line: f"    {line}", lines))
            return f"if {self.condition}:\n{body}\nelse:\n{else_body}"

        return f"if {self.condition}:\n{body}"


@dataclass(kw_only=True)
class PassStatementAST(StatementAST):
    def __str__(self) -> str:
        return "pass"


@dataclass(kw_only=True)
class BreakStatementAST(StatementAST):
    def __str__(self) -> str:
        return "break"


@dataclass(kw_only=True)
class ContinueStatementAST(StatementAST):
    def __str__(self) -> str:
        return "continue"


@dataclass(kw_only=True)
class ReturnStatementAST(StatementAST):
    expressions: list[ExpressionAST] = field(default_factory=list)

    def __str__(self) -> str:
        expressions = ", ".join(map(str, self.expressions))
        return f"return {expressions}"


@dataclass(kw_only=True)
class ImportStatementAST(StatementAST):
    path: list[str]
    alias: str | None = None

    def __str__(self) -> str:
        path = ".".join(self.path)
        return f"import {path} as {self.alias}" if self.alias else f"import {path}"


@dataclass(kw_only=True)
class ExpressionsStatementAST(StatementAST):
    expressions: list[ExpressionAST]

    def __str__(self) -> str:
        return ", ".join(map(str, self.expressions))


@dataclass(kw_only=True)
class ClassDefinitionStatementAST(StatementAST):
    name: str
    body: MultipleStatementAST

    def __str__(self) -> str:
        lines = str(self.body).split("\n")
        body = "\n".join(map(lambda line: f"    {line}", lines))
        return f"class {self.name}\n{body}"


@dataclass(kw_only=True)
class AssignmentStatementAST(StatementAST):
    targets: list[TargetAST]
    type: ExpressionAST | None = None
    operator: str | None = None
    values: list[ExpressionAST]

    def __str__(self) -> str:
        targets = ", ".join(map(str, self.targets))
        values = ", ".join(map(str, self.values))

        if self.type:
            targets += ": " + str(self.type)

        if self.operator:
            return f"{targets} {self.operator} {values}"

        return targets


@dataclass(kw_only=True)
class RaiseStatementAST(StatementAST):
    expression: ExpressionAST | None = None
    from_expression: ExpressionAST | None = None

    def __str__(self) -> str:
        if self.expression:
            return f"raise {self.expression}"
        return f"raise from {self.from_expression}"
