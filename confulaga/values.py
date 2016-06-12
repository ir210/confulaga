from typing import Any


class Value:
    def __init__(self, names: str, values: Any):
        self.names = [names]
        self.values = [values]

    @classmethod
    def join(cls, left: 'Value', right: 'Value') -> 'Value':
        o = cls(None, None)
        o.names = [*left.names, *right.names]
        o.values = [*left.values, *right.values]
        return o

    def __getitem__(self, index):
        if isinstance(index, str):
            return self._get_item_by_name(index)
        elif hasattr(index, 'name'):
            return self._get_item_by_name(index.name)
        else:
            return self.values[index]

    def __iter__(self):
        return iter(self.values)

    def __repr__(self):
        return 'Value({})'.format(self.values)

    def _get_item_by_name(self, name):
        values = zip(self.names, self.values)
        return [v[1] for v in values if v[0] == name]
