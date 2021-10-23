import functools
import operator
from os import read


class Exp(object):
    def __init__(self, operator, operands):
        self.operator = operator
        self.operands = operands

    def __repr__(self):
        return f'Exp{repr(self.operator)}, {repr(self.operands)}'

    def __str__(self):
        operand_strs = ', '.join(map(str, self.operands))
        return f'{self.operator}({operand_strs})'


def calc_apply(operator, operands):
    if operator in ['+', 'add']:
        return sum(operands)
    elif operator in ['*', 'mul']:
        return functools.reduce(lambda x, y: x*y, operands)
    elif operator in ['-', 'sub']:
        if len(operands) == 0:
            raise TypeError(operator + " requires at least 1 argument")
        if len(operands) == 1:
            return -operands[0]
        return operands[0] - sum(operands[1:])
    elif operator in ['/', 'div']:
        if len(operands) != 2:
            return TypeError(operator + ' requires 2 arguments')
        return operands[0] / operands[1]


def calc_eval(exp):
    if isinstance(exp, (int, float)):
        return exp
    elif isinstance(exp, Exp):
        operands = [calc_eval(operand) for operand in exp.operands]
        return calc_apply(exp.operator, operands)


def tokenize(line):
    line = line.replace('(', ' ( ').replace(')', " ) ").replace(',', ' ')
    return line.split()


known_operators = ['+', '-', '*', '/', 'add', 'sub', 'mul', 'div']


def token_analyze(tokens):
    operands = []
    # token = tokens.pop(0)
    while tokens[0] != ')':
        operands.append(token_parse(tokens))
        # token = tokens.pop(0)
    tokens.pop(0)
    return operands


def token_parse(tokens):
    token = tokens[0]
    if token.isdigit():
        return int(tokens.pop(0))
    elif token in known_operators:
        operator = tokens.pop(0)
        tokens.pop(0)
        return Exp(operator, token_analyze(tokens))


def calc_parse(line):
    tokens = tokenize(line)
    return token_parse(tokens)


def read_eval_print_loop():
    while True:
        try:
            expression_tree = calc_parse(input('calc>'))
            print(calc_eval(expression_tree))
        except TypeError as err:
            print(type(err).__name__ + ':', err)
        except (KeyboardInterrupt, EOFError):
            print('Calculation completed.')


if __name__ == '__main__':
    read_eval_print_loop()

# print(calc_eval(Exp('add', [1, 2])))
# print(calc_eval(Exp('add', [1, Exp('mul', [2, 3, 4])])))
