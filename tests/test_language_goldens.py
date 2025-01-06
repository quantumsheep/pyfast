import os
import unittest

import pytest

from compiler import compiler
from parser import ast
from parser.driver import parse

UPDATE_GOLDENS = os.environ.get("UPDATE_GOLDENS") == "true"


def run_golden(filename: str):
    program_ast = parse(filename)
    program_ast_tree = str(ast.to_tree(program_ast).show(stdout=False, sorting=False))

    compiler.initialize()
    module = compiler.generate_ir_module(program_ast)
    verified_module = compiler.parse_and_verify_module(module)

    lines = [
        f"Code with transformations:",
        str(program_ast),
        "",
        "-" * 80,
        f"AST:",
        program_ast_tree,
        "",
        "-" * 80,
        f"IR:",
        str(verified_module),
    ]
    expected = "\n".join(lines)

    if UPDATE_GOLDENS or not os.path.exists(f"{filename}.golden"):
        with open(f"{filename}.golden", "w") as f:
            f.write(expected)
    else:
        with open(f"{filename}.golden", "r") as f:
            golden = f.read()

        assert expected == golden


for filename in os.listdir("tests/testdata/language"):
    if filename.endswith(".py"):
        filename = os.path.join("tests/testdata/language", filename)
        test_name = f"test_{filename}"

filenames = os.listdir("tests/testdata/language")
filenames = [filename for filename in filenames if filename.endswith(".py")]


@pytest.mark.parametrize("filename", filenames)
def test_language(filename: str):
    run_golden(os.path.join("tests/testdata/language", filename))
