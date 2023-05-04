from .model import File, Line, Function


def insert_line(file: File, line: Line) -> None:
    """Inserts a line object into a file object

    Args:
        file (File): File object where Line is inserted
        line (Line): Line object to insert
    """
    if line.lineno in file.lines:
        file.lines[line.lineno] += line
    else:
        file.lines[line.lineno] = line


def insert_function(file: File, function: Function) -> None:
    """Inserts Function object into File object

    Args:
        file (File): _description_
        function (Function): _description_
    """
    if function.name in file.functions:
        file.functions[function.name] += function
    else:
        file.functions[function.name] = function
