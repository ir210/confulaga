import re
import inspect

from typing import Callable, Any, Dict

from .rules import Rule
from .inputs import Input, Sanitizer
from .outputs import Output, OutputType
from .values import Value


def term(pattern: str, name: str=None, transformer: Callable[[str], str]=None) -> Rule:
    class _Rule(Rule):
        ID = re.compile('^{}'.format(pattern))

        def __init__(self):
            super().__init__(name or pattern)

        # noinspection PyShadowingBuiltins
        def parse(self, input: Input) -> Output:
            output = self.__match(input, _Rule.ID)
            type = output.type

            if type == OutputType.ok:
                input, value = output.payload
                _transformer = transformer if transformer else lambda x: x

                return Output(type, input, Value(self.name, _transformer(value.group(0))))
            else:
                line, message = output.payload
                return Output(type, line, 'Expecting {}.'.format(self.name))

    return _Rule()


# noinspection PyShadowingNames
def rule(rule: Rule, name: str=None) -> Callable[[Callable[[Any], Any]], Rule]:
    def w(f: Callable[[Any], Any]) -> Rule:
        class _Rule(Rule):
            def __init__(self):
                super().__init__(name or f.__name__)

            # noinspection PyShadowingBuiltins
            def parse(self, input: Input) -> Output:
                output = rule.parse(input)
                type = output.type

                if type == OutputType.ok:
                    input, value = output.payload
                    return Output(type, input, Value(self.name, f(value)))
                else:
                    return output

        return _Rule()

    return w


def ignore(pattern: str, flags: int=0) -> Sanitizer:
    return Sanitizer(re.compile(pattern, flags))


def forwarder(env) -> Callable[[Dict[str, Any]], Callable[[str], Rule]]:
    def f(rule_name: str) -> Rule:
        class _Rule(Rule):
            def __init__(self):
                super().__init__(rule_name)

            def parse(self, input: Input) -> Output:
                if rule_name not in env:
                    raise LookupError('Cannot find {}'.format(rule_name))

                target_rule = env[rule_name]
                self.name = target_rule.name

                return target_rule.parse(input)

        return _Rule()

    return f


def forward2(rule_name: str) -> Rule:
    class _Rule(Rule):
        def __init__(self):
            super().__init__(rule_name)

        def parse(self, input: Input) -> Output:
            envx = inspect.stack()
            env = envx[0].frame.f_locals

            if rule_name not in env:
                raise LookupError('Cannot find {}'.format(rule_name))

            target_rule = env[rule_name]
            self.name = target_rule.name

            return target_rule.parse(input)

    return _Rule()
