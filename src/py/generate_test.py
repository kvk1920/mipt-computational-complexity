import sys
from random import choice


VAR_NAMES = 'abcdefghijklmnopqurstuvwxyz'
NEGATIONS = ('', '-')


def main(variables, disjoints, expressions):
    res = ''
    for i in range(expressions):
        for j in range(disjoints):
            a = choice(NEGATIONS) + choice(VAR_NAMES[:variables])
            b = choice(NEGATIONS) + choice(VAR_NAMES[:variables])
            if j:
                res += '*'
            res += '({}+{})'.format(a, b)
        res += '\n'
    print(res, file=sys.stderr)
    print('=' * 80, file=sys.stderr)
    return res


if '__main__' == __name__:
    variables = int(sys.argv[1])
    disjoints = int(sys.argv[2])
    expressions = int(sys.argv[3])
    print(main(variables, disjoints, expressions), end='')
