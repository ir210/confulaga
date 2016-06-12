
class Cursor:
    def __init__(self, pos: int, row: int, col: int, row_start: int):
        self.pos = pos
        self.row = row
        self.col = col
        self.row_start = row_start

    @staticmethod
    def zero():
        return Cursor(0, 0, 0, 0)

    def advance(self, source: str, new_pos: int) -> 'Cursor':
        old_pos = self.pos
        current_pos = old_pos
        new_row = self.row
        new_col = self.col
        new_row_start = self.row_start

        while current_pos < new_pos:
            new_line_pos = source.find('\n', current_pos)

            if new_line_pos != -1:
                if new_line_pos >= new_pos:
                    new_col = new_pos - new_row_start
                    break

                new_row += 1
                new_row_start = new_line_pos + 1

                new_col = new_pos - new_row_start
                current_pos = new_line_pos + 1
            else:
                new_col = new_pos - new_row_start
                break

        return Cursor(new_pos, new_row, new_col, new_row_start)
