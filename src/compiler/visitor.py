from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
import os
from typing import cast
from parser import ast
from parser.driver import parse

from llvmlite import ir


class CompilerError(Exception):
    def __init__(self, tree: ast.AST, message: str):
        super().__init__(
            tree.source_position.error(
                f"{message}. This is not your fault, but a bug in the compiler.",
                title="Compiler Error",
            )
        )


class SourceError(Exception):
    def __init__(self, tree: ast.AST, message: str):
        super().__init__(tree.source_position.error(message))


class FeatureNotImplementedError(SourceError):
    def __init__(self, tree: ast.AST, feature: str | None = None):
        ast_type = type(tree).__name__

        message = f"{feature} " if feature is not None else ""
        message += f"feature not implemented in compiler ({ast_type})"

        super().__init__(tree, message)


class ModuleNotFoundError(SourceError):
    def __init__(self, tree: ast.AST, tried_paths: list[str]):
        super().__init__(tree, "module not found. Tried: " + ", ".join(tried_paths))


@dataclass(kw_only=True)
class PyTypeObject:
    id: int
    name: str
    generics: list[PyTypeObject]

    llvm_type: ir.Type


PyTypeNone = PyTypeObject(
    id=1,
    name="None",
    generics=[],
    llvm_type=ir.VoidType(),
)

PyTypeInt8 = PyTypeObject(
    id=1,
    name="int8",
    generics=[],
    llvm_type=ir.IntType(8),
)

PyTypeInt16 = PyTypeObject(
    id=2,
    name="int16",
    generics=[],
    llvm_type=ir.IntType(16),
)

PyTypeInt32 = PyTypeObject(
    id=3,
    name="int32",
    generics=[],
    llvm_type=ir.IntType(32),
)

PyTypeInt64 = PyTypeObject(
    id=4,
    name="int64",
    generics=[],
    llvm_type=ir.IntType(64),
)

PyTypeFloat32 = PyTypeObject(
    id=5,
    name="float32",
    generics=[],
    llvm_type=ir.FloatType(),
)

PyTypeFloat64 = PyTypeObject(
    id=6,
    name="float64",
    generics=[],
    llvm_type=ir.DoubleType(),
)


@dataclass(kw_only=True)
class PyClassProperty:
    name: str
    typ: PyTypeObject


@dataclass(kw_only=True)
class PyClass:
    name: str
    properties: dict[str, PyClassProperty]


IRValue = ir.Constant | ir.NamedValue


@dataclass(kw_only=True)
class Scope:
    parent: Scope | None = None

    is_function: bool = False
    is_loop: bool = False

    values: dict[str, IRValue | ir.Type] = field(default_factory=dict, init=False)

    loop_cond_block: ir.Block | None = None
    loop_end_block: ir.Block | None = None

    def __getitem__(self, name: str) -> IRValue | ir.Type | None:
        if name in self.values:
            return self.values[name]

        if self.parent is not None:
            return self.parent[name]

        return None

    def __setitem__(self, name: str, value: IRValue | ir.Type):
        self.values[name] = value

    def __contains__(self, name: str) -> bool:
        if name in self.values:
            return True

        if self.parent is not None:
            return name in self.parent

        return False

    def for_variables(self) -> Scope:
        if self.is_function:
            return self

        if self.parent is not None:
            return self.parent.for_variables()

        return self

    def current_loop(self) -> Scope | None:
        if self.is_loop:
            return self

        if self.parent is not None:
            return self.parent.current_loop()

        return None


class Visitor:
    def __init__(self):
        env_pyfast_module_paths = os.environ.get("PYFAST_MODULE_PATH", "").split(":")

        self.module_paths = set(env_pyfast_module_paths)
        self.imported_modules = set[str]()

        self.module = ir.Module(name="main.py")

        # Main function
        main_function_type = ir.FunctionType(PyTypeInt32.llvm_type, ())
        main_function = ir.Function(self.module, main_function_type, name="main")

        main_block = main_function.append_basic_block(name="entry")
        self.main_builder = ir.IRBuilder(main_block)

    def finish(self):
        self.main_builder.ret(PyTypeInt32.llvm_type(0))

    def walk_program(self, program_ast: ast.ProgramAST):
        scope = Scope()

        if program_ast.file.filename is not None:
            self.imported_modules.add(program_ast.file.filename)

        for statement in program_ast.statements.statements:
            self.walk_statement(scope, self.main_builder, statement)

    def walk_statement(
        self,
        scope: Scope,
        builder: ir.IRBuilder,
        statement: ast.StatementAST,
    ):
        if cast(ir.Block, builder.block).terminator is not None:
            return

        match statement:
            case ast.ImportStatementAST():
                self.walk_import_statement(builder, statement)
            case ast.PassStatementAST():
                pass
            case ast.ExpressionsStatementAST():
                for expression in statement.expressions:
                    self.walk_expression(scope, builder, expression)
            case ast.FunctionDefinitionStatementAST():
                raise FeatureNotImplementedError(statement)
            case ast.MultipleStatementAST():
                for sub_statement in statement.statements:
                    self.walk_statement(scope, builder, sub_statement)
            case ast.AssignmentStatementAST():
                self.walk_assignment_statement(scope, builder, statement)
            case ast.IfStatementAST():
                self.walk_if_statement(scope, builder, statement)
            case ast.WhileStatementAST():
                self.walk_while_statement(scope, builder, statement)
            case ast.ForStatementAST():
                self.walk_for_statement(scope, builder, statement)
            case ast.BreakStatementAST():
                self.walk_break_statement(scope, builder, statement)
            case ast.ContinueStatementAST():
                self.walk_continue_statement(scope, builder, statement)
            case _:
                raise FeatureNotImplementedError(statement)

    def walk_import_statement(
        self,
        builder: ir.IRBuilder,
        statement: ast.ImportStatementAST,
    ):
        tried_paths = list[str]()

        import_path = "/".join(statement.path)
        for module_path in self.module_paths:
            filepath = os.path.join(module_path, f"{import_path}.py")

            if os.path.exists(filepath):
                program_ast = parse(filepath)
                self.walk_program(program_ast)
                return

            tried_paths.append(filepath)

        raise ModuleNotFoundError(statement, tried_paths)

    def walk_assignment_statement(
        self,
        scope: Scope,
        builder: ir.IRBuilder,
        statement: ast.AssignmentStatementAST,
    ):
        if len(statement.targets) < len(statement.values):
            raise FeatureNotImplementedError(
                statement, "assignment to more values than targets"
            )

        if len(statement.targets) > len(statement.values):
            raise FeatureNotImplementedError(
                statement, "assignment to less values than targets"
            )

        for target, value in zip(statement.targets, statement.values):
            value_value = self.walk_expression(scope, builder, value)
            if isinstance(value_value, ir.Type):
                raise FeatureNotImplementedError(
                    value, "cannot assign type to variable"
                )

            target_value = self.walk_target(scope, builder, target, value_value)

            match statement.operator:
                case "=":
                    builder.store(value_value, target_value)
                case (
                    "+="
                    | "-="
                    | "*="
                    | "/="
                    | "%="
                    | "&="
                    | "|="
                    | "^="
                    | "<<="
                    | ">>="
                    | "**="
                    | "//="
                ):
                    left = builder.load(target_value)
                    right = value_value

                    if left.type != right.type:
                        raise SourceError(statement, "cannot add different types")

                    match statement.operator:
                        case "+=":
                            result = builder.add(left, right)
                        case "-=":
                            result = builder.sub(left, right)
                        case "*=":
                            result = builder.mul(left, right)
                        case "/=":
                            result = builder.udiv(left, right)
                        case "%=":
                            result = builder.urem(left, right)
                        case "&=":
                            result = builder.and_(left, right)
                        case "|=":
                            result = builder.or_(left, right)
                        case "^=":
                            result = builder.xor(left, right)
                        case "<<=":
                            result = builder.shl(left, right)
                        case ">>=":
                            result = builder.ashr(left, right)
                        case _:
                            raise FeatureNotImplementedError(
                                statement, f"operator {statement.operator}"
                            )

                    builder.store(result, target_value)
                case _:
                    raise FeatureNotImplementedError(
                        statement, f"operator {statement.operator}"
                    )

    def walk_target(
        self,
        scope: Scope,
        builder: ir.IRBuilder,
        target: ast.TargetAST,
        value: IRValue,
    ) -> IRValue:
        match target:
            case ast.NameLiteralExpressionAST():
                scope_item = scope[target.value]

                if scope_item is None or isinstance(scope_item, ir.Type):
                    alloca = builder.alloca(value.type, name=target.value)
                    scope.for_variables()[target.value] = alloca

                    return alloca

                return scope_item
            case _:
                raise FeatureNotImplementedError(target)

    def walk_if_statement(
        self,
        scope: Scope,
        builder: ir.IRBuilder,
        statement: ast.IfStatementAST,
    ):
        condition = self.walk_expression(scope, builder, statement.condition)
        if isinstance(condition, ir.Type):
            raise SourceError(statement, "cannot use type as condition")

        if statement.else_body:
            if_else_generator = if_else(builder, condition)

            # If block
            next(if_else_generator)
            for sub_statement in statement.body.statements:
                self.walk_statement(scope, builder, sub_statement)

            # Else block
            next(if_else_generator)
            for sub_statement in statement.else_body.statements:
                self.walk_statement(scope, builder, sub_statement)

            # End if block
            next(if_else_generator, None)
        else:
            with if_then(builder, condition):
                for sub_statement in statement.body.statements:
                    self.walk_statement(scope, builder, sub_statement)

    def walk_while_statement(
        self,
        scope: Scope,
        builder: ir.IRBuilder,
        statement: ast.WhileStatementAST,
    ):
        bb = cast(ir.Block, builder.block)

        bbcond = builder.append_basic_block(name=bb.name + ".while.cond")
        builder.branch(bbcond)

        builder.position_at_end(bbcond)

        condition = self.walk_expression(scope, builder, statement.condition)
        if isinstance(condition, ir.Type):
            raise SourceError(statement, "cannot use type as condition")

        if statement.else_body:
            while_else_generator = while_else(scope, builder, condition)

            # While block
            while_scope = next(while_else_generator)
            for sub_statement in statement.body.statements:
                self.walk_statement(while_scope, builder, sub_statement)

            # Else block
            else_scope = next(while_else_generator)
            for sub_statement in statement.else_body.statements:
                self.walk_statement(else_scope, builder, sub_statement)

            # End if block
            next(while_else_generator, None)
        else:
            with while_then(scope, builder, condition) as while_scope:
                for sub_statement in statement.body.statements:
                    self.walk_statement(while_scope, builder, sub_statement)

    def walk_for_statement(
        self,
        scope: Scope,
        builder: ir.IRBuilder,
        statement: ast.ForStatementAST,
    ):
        raise FeatureNotImplementedError(statement)

    def walk_break_statement(
        self,
        scope: Scope,
        builder: ir.IRBuilder,
        statement: ast.BreakStatementAST,
    ):
        loop = scope.current_loop()
        if loop is None:
            raise SourceError(statement, "break statement outside loop")

        builder.branch(loop.loop_end_block)

    def walk_continue_statement(
        self,
        scope: Scope,
        builder: ir.IRBuilder,
        statement: ast.ContinueStatementAST,
    ):
        loop = scope.current_loop()
        if loop is None:
            raise SourceError(statement, "continue statement outside loop")

        builder.branch(loop.loop_cond_block)

    def walk_expression(
        self,
        scope: Scope,
        builder: ir.IRBuilder,
        expression: ast.ExpressionAST,
    ) -> IRValue | ir.Type:
        match expression:
            case ast.NumberLiteralExpressionAST():
                return self.walk_number_literal_expression(scope, builder, expression)
            case ast.NameLiteralExpressionAST():
                return self.walk_name_literal_expression(scope, builder, expression)
            case ast.CallExpressionAST():
                return self.walk_call_expression(scope, builder, expression)
            case ast.UnaryExpressionAST():
                return self.walk_unary_expression(scope, builder, expression)
            case ast.BinaryExpressionAST():
                return self.walk_binary_expression(scope, builder, expression)
            case _:
                raise FeatureNotImplementedError(expression)

    def walk_number_literal_expression(
        self,
        scope: Scope,
        builder: ir.IRBuilder,
        expression: ast.NumberLiteralExpressionAST,
    ) -> IRValue:
        match expression.value:
            case int():
                return PyTypeInt32.llvm_type(expression.value)
            case float():
                return PyTypeFloat64.llvm_type(expression.value)
            case _:
                raise SourceError(expression, "undefined identifier")

    def walk_name_literal_expression(
        self,
        scope: Scope,
        builder: ir.IRBuilder,
        expression: ast.NameLiteralExpressionAST,
    ) -> IRValue | ir.Type:
        value = scope.for_variables()[expression.value]
        if value is None:
            raise SourceError(expression, f"undefined identifier {expression.value}")

        return value

    def walk_call_expression(
        self,
        scope: Scope,
        builder: ir.IRBuilder,
        expression: ast.CallExpressionAST,
    ) -> IRValue | ir.Type:
        left_expression = self.walk_expression(scope, builder, expression.expression)
        arguments = [
            self.walk_expression(scope, builder, argument.expression)
            for argument in expression.arguments
        ]

        return builder.call(left_expression, arguments)

    def walk_unary_expression(
        self,
        scope: Scope,
        builder: ir.IRBuilder,
        expression: ast.UnaryExpressionAST,
    ) -> IRValue | ir.Type:
        value = self.walk_expression(scope, builder, expression.expression)

        match expression.operator:
            case "+":
                return value
            case "-":
                return cast(ir.NamedValue, builder.sub(PyTypeInt32.llvm_type(0), value))
            case "~":
                return cast(ir.NamedValue, builder.not_(value))
            case _:
                raise FeatureNotImplementedError(
                    expression, f"operator {expression.operator}"
                )

    def walk_binary_expression(
        self,
        scope: Scope,
        builder: ir.IRBuilder,
        expression: ast.BinaryExpressionAST,
    ) -> IRValue | ir.Type:
        left = self.walk_expression(scope, builder, expression.left)
        if isinstance(left, ir.Type):
            raise SourceError(expression, "cannot use type as left operand")

        right = self.walk_expression(scope, builder, expression.right)
        if isinstance(right, ir.Type):
            raise SourceError(expression, "cannot use type as right operand")

        if isinstance(left, ir.AllocaInstr):
            left = builder.load(left)

        if isinstance(right, ir.AllocaInstr):
            right = builder.load(right)

        if left.type != right.type:
            raise SourceError(expression, "cannot add different types")

        match expression.operator:
            case "+":
                return cast(ir.NamedValue, builder.add(left, right))
            case "-":
                return cast(ir.NamedValue, builder.sub(left, right))
            case "*":
                return cast(ir.NamedValue, builder.mul(left, right))
            case "/":
                return cast(ir.NamedValue, builder.udiv(left, right))
            case "%":
                return cast(ir.NamedValue, builder.urem(left, right))
            case "&":
                return cast(ir.NamedValue, builder.and_(left, right))
            case "|":
                return cast(ir.NamedValue, builder.or_(left, right))
            case "^":
                return cast(ir.NamedValue, builder.xor(left, right))
            case "<<":
                return cast(ir.NamedValue, builder.shl(left, right))
            case ">>":
                return cast(ir.NamedValue, builder.ashr(left, right))
            case "==":
                return cast(ir.NamedValue, builder.icmp_signed("==", left, right))
            case "!=":
                return cast(ir.NamedValue, builder.icmp_signed("!=", left, right))
            case "<=":
                return cast(ir.NamedValue, builder.icmp_signed("<=", left, right))
            case "<":
                return cast(ir.NamedValue, builder.icmp_signed("<", left, right))
            case ">=":
                return cast(ir.NamedValue, builder.icmp_signed(">=", left, right))
            case ">":
                return cast(ir.NamedValue, builder.icmp_signed(">", left, right))
            case _:
                raise FeatureNotImplementedError(
                    expression, f"operator {expression.operator}"
                )

    # if isinstance(expression, ast.CombinatoryStringLiteralExpressionAST):
    #     for value in expression.values:
    #         if isinstance(value, ast.StringLiteralExpressionAST):
    #             global_raw_string_type = ir.ArrayType(
    #                 PyTypeInt8.llvm_type,
    #                 len(value.value) + 1,
    #             )
    #             global_raw_string = ir.GlobalVariable(
    #                 module=self.module,
    #                 typ=global_raw_string_type,
    #                 name="str",
    #             )
    #             global_raw_string.linkage = "private"
    #             global_raw_string.global_constant = True
    #             global_raw_string.unnamed_addr = True
    #             global_raw_string.align = 1  # type: ignore
    #             global_raw_string.initializer = ir.Constant(  # type: ignore
    #                 typ=global_raw_string_type,
    #                 constant=bytearray(value.value.encode("utf-8")),
    #             )

    #             global_string_type = self.scope["libpy.str"]
    #             global_string = ir.GlobalVariable(
    #                 module=self.module,
    #                 typ=global_string_type,
    #                 name="str.2",
    #             )
    #             global_string.linkage = "private"
    #             global_string.global_constant = True
    #             global_string.unnamed_addr = True
    #             global_string.initializer = ir.Constant(  # type: ignore
    #                 global_string_type,
    #                 [
    #                     PyTypeInt64.llvm_type(len(value.value)),
    #                     global_raw_string.gep(
    #                         [PyTypeInt32.llvm_type(0), PyTypeInt32.llvm_type(0)]
    #                     ),
    #                 ],
    #             )

    #             return global_string

    # raise FeatureNotImplementedError(expression)


@contextmanager
def if_then(builder: ir.IRBuilder, condition: ir.Value):
    bb = cast(ir.Block, builder.block)

    # If block
    bbif = cast(ir.Block, builder.append_basic_block(name=bb.name + ".if.true"))
    builder.position_at_end(bbif)

    yield

    bbif_end = cast(ir.Block, builder.block)

    # End if block
    bbendif = cast(ir.Block, builder.append_basic_block(name=bb.name + ".if.end"))

    # Add br if the block does not have a terminator
    builder.position_at_end(bbif_end)
    if cast(ir.Block, builder.block).terminator is None:
        builder.branch(bbendif)

    # Add cbranch to the end of the original block
    builder.position_at_end(bb)
    builder.cbranch(condition, bbif, bbendif)

    # Move to the end block
    builder.position_at_end(bbendif)


def if_else(builder: ir.IRBuilder, condition: ir.Value):
    bb = cast(ir.Block, builder.block)

    # If block
    bbif = cast(ir.Block, builder.append_basic_block(name=bb.name + ".if.true"))
    builder.position_at_end(bbif)

    yield

    bbif_end = cast(ir.Block, builder.block)

    # Else block
    bbelse = cast(ir.Block, builder.append_basic_block(name=bb.name + ".if.false"))
    builder.position_at_end(bbelse)

    yield

    bbelse_end = cast(ir.Block, builder.block)

    # End if block
    bbendif = cast(ir.Block, builder.append_basic_block(name=bb.name + ".if.end"))

    # Add br if the blocks does not have a terminator
    builder.position_at_end(bbif_end)
    if cast(ir.Block, builder.block).terminator is None:
        builder.branch(bbendif)

    builder.position_at_end(bbelse_end)
    if cast(ir.Block, builder.block).terminator is None:
        builder.branch(bbendif)

    # Add cbranch to the end of the original block
    builder.position_at_end(bb)
    builder.cbranch(condition, bbif, bbelse)

    # Move to the end block
    builder.position_at_end(bbendif)


@contextmanager
def while_then(
    scope: Scope,
    builder: ir.IRBuilder,
    condition: ir.Value,
):
    bbcond = cast(ir.Block, builder.block)
    name_without_cond = bbcond.name.rsplit(".", 1)[0]

    bbend = ir.Block(parent=bbcond.function, name=name_without_cond + ".end")

    scope = Scope(
        parent=scope,
        is_loop=True,
        loop_cond_block=bbcond,
        loop_end_block=bbend,
    )

    # Body block
    bbbody = cast(
        ir.Block, builder.append_basic_block(name=name_without_cond + ".body")
    )
    builder.position_at_end(bbbody)

    yield scope

    bbbody_end = cast(ir.Block, builder.block)

    # End block
    function = cast(ir.Function, builder.function)
    function.blocks.append(bbend)

    # Add br if the block does not have a terminator
    builder.position_at_end(bbbody_end)
    if cast(ir.Block, builder.block).terminator is None:
        builder.branch(bbcond)

    # Add cbranch to the end of the original block
    builder.position_at_end(bbcond)
    builder.cbranch(condition, bbbody, bbend)

    # Move to the end block
    builder.position_at_end(bbend)


def while_else(
    scope: Scope,
    builder: ir.IRBuilder,
    condition: ir.Value,
):
    bbcond = cast(ir.Block, builder.block)
    name_without_cond = bbcond.name.rsplit(".", 1)[0]

    bbend = ir.Block(parent=bbcond.function, name=name_without_cond + ".end")

    scope = Scope(
        parent=scope,
        is_loop=True,
        loop_cond_block=bbcond,
        loop_end_block=bbend,
    )

    # Body block
    bbbody = cast(
        ir.Block, builder.append_basic_block(name=name_without_cond + ".body")
    )
    builder.position_at_end(bbbody)

    yield scope

    bbbody_end = cast(ir.Block, builder.block)

    # Else block
    bbelse = cast(
        ir.Block, builder.append_basic_block(name=name_without_cond + ".else")
    )
    builder.position_at_end(bbelse)

    scope = cast(Scope, scope)
    yield scope

    bbelse_end = cast(ir.Block, builder.block)

    # End block
    function = cast(ir.Function, builder.function)
    function.blocks.append(bbend)

    # Add br if the block does not have a terminator
    builder.position_at_end(bbbody_end)
    if cast(ir.Block, builder.block).terminator is None:
        builder.branch(bbcond)

    builder.position_at_end(bbelse_end)
    if cast(ir.Block, builder.block).terminator is None:
        builder.branch(bbend)

    # Add cbranch to the end of the original block
    builder.position_at_end(bbcond)
    builder.cbranch(condition, bbbody, bbelse_end)

    # Move to the end block
    builder.position_at_end(bbend)
