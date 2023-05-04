from functools import cached_property
from typing import Dict

from .utils import merge_dict


class Function:
    __slots__ = (
        "count",
        "name",
        "demangled_name",
        "start_line",
        "end_line",
    )

    def __init__(
        self,
        *,
        name: str,
        demangled_name: str,
        count: int,
        start_line: int,
        end_line: int,
    ) -> None:
        self.count = count
        self.name = name
        self.demangled_name = demangled_name
        self.start_line = start_line
        self.end_line = end_line

    @cached_property
    def is_covered(self) -> bool:
        return self.count > 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Function):
            return False

        return (
            self.name == other.name
            and self.demangled_name == other.demangled_name
            and self.start_line == other.start_line
            and self.end_line == other.end_line
        )

    def __hash__(self) -> int:
        return hash(self.name, self.demangled_name, self.start_line, self.end_line)

    def __add__(self, other: object):
        assert isinstance(other, Function)
        assert self.name == other.name
        assert self.demangled_name == other.demangled_name
        assert self.start_line == other.start_line
        assert self.end_line == other.end_line

        return Function(
            name=self.name,
            demangled_name=self.demangled_name,
            start_line=self.start_line,
            end_line=self.end_line,
            count=self.count + other.count,
        )

    def __repr__(self) -> str:
        return f"Function(name={self.name}, demangled_name={self.demangled_name},\
                count={self.count}, start_line={self.start_line}, end_line={self.end_line})"


class Branch:
    __slots__ = "fallthrough", "throw", "count"

    def __init__(
        self, *, count: int, fallthrough: bool = True, throw: bool = True
    ) -> None:
        self.count = count
        self.fallthrough = fallthrough
        self.throw = throw

    @cached_property
    def is_covered(self):
        return self.count > 0

    def __add__(self, other: object):
        assert isinstance(other, Branch)

        return Branch(
            count=self.count + other.count,
            fallthrough=self.fallthrough | other.fallthrough,
            throw=self.throw | other.throw,
        )

    def __repr__(self) -> str:
        return f"Branch(count={self.count}, fallthrough={self.fallthrough}, throw={self.throw})"


class Line:
    __slots__ = "lineno", "count", "function_name", "branches"

    def __init__(
        self,
        lineno: int,
        count: int,
        function_name: str,
        branches: Dict[int, Branch] | None = None,
    ) -> None:
        self.lineno = lineno
        self.count = count
        self.function_name = function_name
        self.branches = branches if branches is not None else dict()

    @cached_property
    def is_covered(self):
        return self.count > 0

    def __add__(self, other: object):
        assert isinstance(other, Line)
        assert self.lineno == other.lineno
        assert self.function_name == other.function_name

        return Line(
            lineno=self.lineno,
            count=self.count + other.count,
            function_name=self.function_name,
            branches=merge_dict(self.branches, other.branches),
        )


class File:
    __slots__ = "name", "lines", "functions"

    def __init__(
        self,
        name: str,
        lines: Dict[int, Line] | None = None,
        functions: Dict[str, Function] | None = None,
    ) -> None:
        self.name = name
        self.lines = lines if lines is not None else dict()
        self.functions = functions if functions is not None else Dict()

    @cached_property
    def line_coverage(self):
        total = 0
        covered = 0

        for line in self.lines.values():
            total += 1
            if line.is_covered:
                covered += 1

        return total, covered

    @cached_property
    def branch_coverage(self):
        total = 0
        covered = 0

        for line in self.lines.values():
            for branch in line.branches.values():
                total += 1
                if branch.is_covered:
                    covered += 1

        return total, covered

    @cached_property
    def function_coverage(self):
        total = 0
        covered = 0

        for function in self.functions.values():
            total += 1

            if function.is_covered:
                covered += 1

        return total, covered


CovData = Dict[str, str | File]
