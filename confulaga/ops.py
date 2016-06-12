from confulaga.values import Value
from .rules import Rule
from .inputs import Input
from .outputs import Output, OutputType


def star(rule: Rule) -> Rule:
    class _Rule(Rule):
        def __init__(self):
            super().__init__('({})*'.format(rule.name))

        # noinspection PyShadowingBuiltins
        def parse(self, input: Input) -> Output:
            result = Value(self.name, None)
            next_input = input

            while not next_input.eof():
                output = rule.parse(next_input)
                output_type = output.type

                if output_type == OutputType.ok:
                    next_input, value = output.payload

                    if result is None:
                        result = value
                    else:
                        result = Value.join(result, value)
                elif output_type == OutputType.no_match:
                    break
                else:
                    return output

            return Output(OutputType.ok, next_input, result)

    return _Rule()


def opt(rule: Rule) -> Rule:
    class _Rule(Rule):
        def __init__(self):
            super().__init__('({})?'.format(rule.name))

        # noinspection PyShadowingBuiltins
        def parse(self, input: Input) -> Output:
            output = rule.parse(input)
            output_type = output.type

            if output_type == OutputType.no_match:
                return Output(OutputType.ok, input, Value(rule.name, None))
            else:
                return output

    return _Rule()
