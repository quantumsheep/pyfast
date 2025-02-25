import os
import sys
from parser import ast
from parser.driver import parse
from typing import Any

from compiler import compiler
from pyfast.command import Command


def command() -> Command:
    command = Command(
        name="build",
        description="PyFast Python compiler",
        func=run,
    )

    command.add_positional(name="filename", help="Python file to compile")
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

        object_bytes = compiler.emit_object(verified_module)
        with open("output.o", "wb") as f:
            f.write(object_bytes)
    except Exception as e:
        if verbose:
            raise e

        print(e)
        sys.exit(1)
