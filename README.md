#Confulaga

Confulaga is a parsing library for Python. It will help you create a parser from an LL grammar that you define within
the python script itself.

##Example

Below is an example of how to use Confulaga to create a parser to parse JSON syntax.

``` python
from confulaga import *


WHITESPACE = ignore(r'^[ \t\r\n]+')

STRING = term('\"[^\"]*\"', 'string', lambda x: x[1:-1])
NUMBER = term('[-+]?[0-9]*\\.?[0-9]+([eE][-+]?[0-9]+)?', 'number')

OPEN_BRACE = term(r'\{', name='{')
CLOSE_BRACE = term(r'\}', name='}')
OPEN_BRACKET = term(r'\[', name='[')
CLOSE_BRACKET = term(r'\]', name=']')

TRUE = term('true', name='true')
FALSE = term('false', name='false')
COMMA = term(r',', name=',')
COLON = term(r':', name=':')

f = forwarder(globals())


@rule(FALSE)
def json_false(value):
    return False


@rule(TRUE)
def json_true(value):
    return True


@rule(NUMBER)
def json_number(value):
    number_str = value[0]

    if '.' in number_str or 'e' in number_str or 'E' in number_str:
        return float(number_str)
    else:
        return int(number_str)


@rule(STRING | json_false | json_true | json_number | f('json_array') | f('json_object'))
def json_item(value):
    return value[0]


@rule(opt(json_item + star(COMMA + json_item)))
def json_array_body(value):
    return value[json_item]


@rule(OPEN_BRACKET + json_array_body + CLOSE_BRACKET)
def json_array(value):
    return value[json_array_body][0]


@rule(STRING + COLON + json_item)
def json_object_item(value):
    return value[STRING][0], value[json_item][0]


@rule(opt(json_object_item + star(COMMA + json_object_item)))
def json_object_body(value):
    return value[json_object_item]


@rule(OPEN_BRACE + json_object_body + CLOSE_BRACE)
def json_object(value):
    return {k[0]: k[1] for k in value[json_object_body][0]}


source = '''
    {
        "key 1": 1,
        "key 2": "value2",
        "key 3": [
            "item 1",
            "item 2",
            "item 3"
        ],
        "key 4": true,
        "key 5": false,
        "key 6": 12.3
    }
'''

output = json_item.parse(Input(source, ignore_list=[
    WHITESPACE,
]))

if output.type == OutputType.ok:
    _, value = output.payload
    print(value[0])
else:
    line, message = output.payload
    print(message)
    print(line)
```
