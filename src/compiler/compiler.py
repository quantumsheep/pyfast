from typing import Any
from compiler.visitor import Visitor
from parser import ast
import llvmlite.binding as llvm
from llvmlite import ir


def initialize():
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()


def generate_ir_module(program: ast.ProgramAST) -> ir.Module:
    visitor = Visitor()
    visitor.walk_program(program)
    visitor.finish()
    return visitor.module


def parse_and_verify_module(module: ir.Module) -> llvm.ModuleRef:
    llvm_module_ref = llvm.parse_assembly(str(module))
    llvm_module_ref.verify()
    return llvm_module_ref


def run(module_ref: llvm.ModuleRef) -> int:
    engine = create_execution_engine()

    engine.add_module(module_ref)
    engine.finalize_object()
    engine.run_static_constructors()

    # Look up the function pointer (a Python int)
    func_ptr = engine.get_function_address("main")

    # Run the function via ctypes
    from ctypes import CFUNCTYPE, c_int

    cfunc = CFUNCTYPE(c_int)(func_ptr)
    return int(cfunc())


def emit_object(module: llvm.ModuleRef) -> bytes:
    target_machine = create_target_machine()
    return target_machine.emit_object(module)


def create_target_machine():
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()

    return target_machine


def create_execution_engine():
    target_machine = create_target_machine()

    # And an execution engine with an empty backing module
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine
