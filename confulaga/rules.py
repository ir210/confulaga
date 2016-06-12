import abc

from .outputs import Output, OutputType, Line
from .inputs import Input
from .values import Value


class Rule(metaclass=abc.ABCMeta):
    def __init__(self, name: str):
        self.name = name

    # noinspection PyShadowingBuiltins
    @abc.abstractmethod
    def parse(self, input: Input) -> Output:
        pass

    # noinspection PyShadowingBuiltins
    def __match(self, input: Input, pattern) -> Output:
        sanitized_input = input.sanitize()
        matcher = pattern.match(sanitized_input.text)

        if not matcher:
            return Output(OutputType.no_match, Line(input), 'Expecting {}'.format(pattern))

        new_pos = sanitized_input.offset + matcher.end()
        new_input = sanitized_input.consume_until(new_pos)

        return Output(OutputType.ok, new_input, matcher)

    def __repr__(self) -> str:
        return 'Rule({})'.format(self.name)

    def __add__(self, other: 'Rule') -> 'Rule':
        return SequentialRule(self, other)

    def __or__(self, other: 'Rule') -> 'Rule':
        return ChoiceRule(self, other)

    def __getitem__(self, new_name: str) -> 'Rule':
        class _Rule(Rule):
            def __init__(self, original_rule: Rule):
                super(_Rule, self).__init__(new_name)
                self.original_rule = original_rule

            # noinspection PyShadowingBuiltins
            def parse(self, input: Input) -> Output:
                return self.original_rule.parse(input)

        return _Rule(self)


class SequentialRule(Rule):
    def __init__(self, left_rule: Rule, right_rule: Rule):
        super().__init__('{} then {}'.format(left_rule.name, right_rule.name))
        self.left_rule = left_rule
        self.right_rule = right_rule

    # noinspection PyShadowingBuiltins
    def parse(self, input: Input) -> Output:
        left_output = self.left_rule.parse(input)
        left_output_type = left_output.type

        if left_output_type == OutputType.ok:
            next_input, left_value = left_output.payload

            right_output = self.right_rule.parse(next_input)
            right_output_type = right_output.type

            if right_output_type == OutputType.ok:
                next_input, right_value = right_output.payload
                value = Value.join(left_value, right_value)

                return Output(OutputType.ok, next_input, value)
            elif right_output_type == OutputType.no_match:
                return Output(OutputType.error, *right_output.payload)
            else:
                return right_output
        else:
            return left_output


class ChoiceRule(Rule):
    def __init__(self, left_rule: Rule, right_rule: Rule):
        super().__init__('{} or {}'.format(left_rule.name, right_rule.name))
        self.left_rule = left_rule
        self.right_rule = right_rule

    # noinspection PyShadowingBuiltins
    def parse(self, input: Input) -> Output:
        left_output = self.left_rule.parse(input)
        left_output_type = left_output.type

        if left_output_type == OutputType.no_match:
            return self.right_rule.parse(input)
        else:
            return left_output
