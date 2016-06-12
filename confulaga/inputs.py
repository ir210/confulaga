import re

from typing import List

from confulaga import Cursor


class Input:
    def __init__(self, source: str, cursor: Cursor = None, ignore_list: List['Sanitizer'] = None):
        self.source = source
        self.cursor = cursor or Cursor.zero()
        self.sanitizers = ignore_list or []

    @property
    def offset(self) -> int:
        return self.cursor.pos

    @property
    def text(self) -> str:
        return self.source[self.cursor.pos:]

    @property
    def col(self) -> int:
        return self.cursor.col

    @property
    def row(self) -> int:
        return self.cursor.row

    @property
    def line(self) -> str:
        end_index = self.source.find('\n', self.cursor.row_start)

        if end_index == -1:
            return self.source[self.cursor.row_start:]
        else:
            return self.source[self.cursor.row_start:end_index]

    def eof(self) -> bool:
        the_rest = self.source[self.cursor.pos:]
        return not the_rest or re.match(r'^\s+$', the_rest) is not None

    def sanitize(self) -> 'Input':
        pos = self.cursor.pos
        substring = self.source[pos:]

        while True:
            found = False

            for sanitizer in self.sanitizers:
                found, pos = sanitizer.sanitize(found, pos, substring)
                substring = self.source[pos:] if found else substring

            if not found:
                break

        return self.consume_until(pos)

    def consume_until(self, new_pos: int) -> 'Input':
        return Input(self.source, self.cursor.advance(self.source, new_pos), self.sanitizers)


class Sanitizer:
    def __init__(self, pattern):
        self.pattern = pattern

    def sanitize(self, found: bool, pos: int, text: str) -> (bool, int):
        m = self.pattern.match(text)

        if m:
            pos += m.end()
            return True, pos
        else:
            return found, pos
