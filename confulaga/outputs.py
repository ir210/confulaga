from enum import Enum
from confulaga import Input


class Line:
    # noinspection PyShadowingBuiltins
    def __init__(self, input: Input):
        self.input = input

    def __repr__(self):
        line = self.input.line
        row = self.input.row
        col = self.input.col
        row_col = '[{row}:{col}'.format(row=row, col=col)

        return '{row_col}{line}\n{arrow}'.format(
            row_col=row_col,
            line=line,
            arrow='{}^'.format(' ' * (col + len(row_col))))

    def __str__(self):
        return repr(self)


class OutputType(Enum):
    ok = 0
    no_match = 1
    error = 2


class Output:
    def __init__(self, output_type: OutputType, *payload):
        self.type = output_type
        self.payload = payload
