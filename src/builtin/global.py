from builtin import sys


def print(
    *values: object,
    sep: str | None = " ",
    end: str | None = "\n",
    # file: SupportsWrite[str] | None = None,
    flush: bool = False,
):
    for value in values:
        sys.stdout.write(str(value))

        if sep is not None:
            sys.stdout.write(sep)

    if end is not None:
        sys.stdout.write(end)

    if flush:
        sys.stdout.flush()


def input(prompt: object = "") -> str:
    sys.stdout.write(str(prompt))
    return sys.stdin.readline()


print("Hello, world!")
