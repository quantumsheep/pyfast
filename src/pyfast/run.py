import os
import sys
from parser import ast
from parser.driver import parse
from typing import Any

from compiler import compiler
from pyfast.command import Command


def command() -> Command:
    command = Command(
        name="run",
        description="Run a Python script",
        func=run,
    )

    command.add_positional(name="filename", help="Python script to run")
    command.add_flag(
        short="-v",
        long="--verbose",
        help="Enable verbose mode",
    )
    command.add_flag(
        long="--print-ast",
        help="Print AST",
    )

    return command


def run(args: dict[str, Any]) -> None:
    filename: str = args["filename"]
    verbose: bool = args["verbose"]

    if not os.path.exists(filename):
        print(f"File {filename} does not exist")
        sys.exit(1)

    filename = os.path.abspath(filename)

    try:
        program_ast = parse(filename)

        if args["print_ast"]:
            tree = ast.to_tree(program_ast)
            print(tree.show(stdout=False, sorting=False))

        compiler.initialize()
        module = compiler.generate_ir_module(program_ast)

        try:
            verified_module = compiler.parse_and_verify_module(module)
        except Exception as e:
            if verbose:
                print(module)
            raise e

        if verbose:
            print(verified_module)

        return_value = compiler.run(verified_module)
        sys.exit(return_value)
    except Exception as e:
        if verbose:
            raise e

        print(e)
        sys.exit(1)
