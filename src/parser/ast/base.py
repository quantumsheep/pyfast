from dataclasses import dataclass
import os


@dataclass(kw_only=True)
class SourceFile:
    filename: str | None = None
    content: str


@dataclass(kw_only=True)
class SourcePosition:
    file: SourceFile
    line: int
    column: int

    def error(self, message: str):
        relative_filename_path = (
            os.path.relpath(self.file.filename, os.getcwd())
            if self.file.filename
            else ""
        )
        position = f"{relative_filename_path}:{self.line}:{self.column}"

        lines = self.file.content.split("\n")

        line_start = max(0, self.line - 2)
        line_end = min(len(lines), self.line + 1)
        lines = lines[line_start:line_end]

        lines.insert(
            2 if self.line > 1 else 1,
            " " * (self.column - 1) + f"\033[1m\033[31m^ {message}\033[0m",
        )

        lines.insert(-1, "")

        # Remove empty lines at the start and end
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop(-1)

        issue_lines = "\n".join(lines)
        return f"\033[1m\033[31mError\033[0m\033[1m: {message}\033[0m\n --> {position}:\n\n{issue_lines}\n"


@dataclass(kw_only=True)
class AST:
    source_position: SourcePosition
