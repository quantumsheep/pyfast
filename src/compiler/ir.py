from __future__ import annotations
from dataclasses import dataclass

from llvmlite import ir

from parser.ast import ast


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


class Scope:
    def __init__(self, parent: Scope | None = None):
        self.parent = parent
        self.values = dict[str, ir.Value | ir.Type]()

    def __getitem__(self, name: str) -> ir.Value | ir.Type | None:
        if name in self.values:
            return self.values[name]

        if self.parent is not None:
            return self.parent[name]

        return None

    def __setitem__(self, name: str, value: ir.Value | ir.Type):
        self.values[name] = value


class IntermediateRepresentation:
    def __init__(self, program_ast: ast.ProgramAST):
        self.scope = Scope()
        self.module = ir.Module(name=program_ast.filepath)

        string_type = ir.IdentifiedStructType(self.module.context, name="libpy.str")
        string_type.set_body(
            PyTypeInt64.llvm_type,
            PyTypeInt8.llvm_type.as_pointer(),
        )
        self.module.context.identified_types[string_type.name] = string_type
        self.scope[string_type.name] = string_type

        main_function_type = ir.FunctionType(PyTypeInt32.llvm_type, ())
        main_function = ir.Function(self.module, main_function_type, name="main")

        main_block = main_function.append_basic_block(name="entry")
        main_builder = ir.IRBuilder(main_block)

        for statement in program_ast.statements:
            self.generate_statement(main_builder, statement)

        main_builder.ret(PyTypeInt32.llvm_type(0))

    def generate_statement(self, builder: ir.IRBuilder, statements: ast.StatementAST):
        if isinstance(statements, ast.PassStatementAST):
            return

        if isinstance(statements, ast.ExpressionsStatementAST):
            for expression in statements.expressions:
                self.generate_expression(builder, expression)
            return

        if isinstance(statements, ast.BreakStatementAST):
            raise NotImplementedError()

        if isinstance(statements, ast.ContinueStatementAST):
            raise NotImplementedError()

        raise NotImplementedError(statements)

    def generate_expression(
        self,
        builder: ir.IRBuilder,
        expression: ast.ExpressionAST,
    ) -> ir.Value:
        if isinstance(expression, ast.CallExpressionAST):
            left_expression = self.generate_expression(builder, expression.expression)
            arguments = [
                self.generate_expression(builder, argument.expression)
                for argument in expression.arguments
            ]

            return builder.call(left_expression, arguments)

        if isinstance(expression, ast.NameLiteralExpressionAST):
            value = self.scope[expression.value]
            if value is None:
                raise ValueError(f"Undefined variable {expression.value}")

            if not isinstance(value, ir.Value):
                raise ValueError(f"Can't use type {value} as a value")

            return value

        if isinstance(expression, ast.CombinatoryStringLiteralExpressionAST):
            for value in expression.values:
                if isinstance(value, ast.StringLiteralExpressionAST):
                    global_raw_string_type = ir.ArrayType(
                        PyTypeInt8.llvm_type,
                        len(value.value) + 1,
                    )
                    global_raw_string = ir.GlobalVariable(
                        module=self.module,
                        typ=global_raw_string_type,
                        name="str",
                    )
                    global_raw_string.linkage = "private"
                    global_raw_string.global_constant = True
                    global_raw_string.unnamed_addr = True
                    global_raw_string.align = 1  # type: ignore
                    global_raw_string.initializer = ir.Constant(  # type: ignore
                        typ=global_raw_string_type,
                        constant=bytearray(value.value.encode("utf-8")),
                    )

                    global_string_type = self.scope["libpy.str"]
                    global_string = ir.GlobalVariable(
                        module=self.module,
                        typ=global_string_type,
                        name="str.2",
                    )
                    global_string.linkage = "private"
                    global_string.global_constant = True
                    global_string.unnamed_addr = True
                    global_string.initializer = ir.Constant(  # type: ignore
                        global_string_type,
                        [
                            PyTypeInt64.llvm_type(len(value.value)),
                            global_raw_string.gep(
                                [PyTypeInt32.llvm_type(0), PyTypeInt32.llvm_type(0)]
                            ),
                        ],
                    )

                    return global_string

        raise NotImplementedError(expression)
