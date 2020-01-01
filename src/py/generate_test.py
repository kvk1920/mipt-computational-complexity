import sys
from random import choice


VAR_NAMES: str = 'abcdefghijklmnopqurstuvwxyz'
NEGATIONS = ('', '-')


def generate(variables: int, disjoints: int, expressions: int, verbose: bool = False) -> str:
    res = ''
    for i in range(expressions):
        for j in range(disjoints):
            a = choice(NEGATIONS) + choice(VAR_NAMES[:variables])
            b = choice(NEGATIONS) + choice(VAR_NAMES[:variables])
            if j:
                res += '*'
            res += '({}+{})'.format(a, b)
        res += '\n'
    if verbose:
        print(res, file=sys.stderr)
        print('=' * 80, file=sys.stderr)
    return res


def main() -> None:
    if '--global-test' in sys.argv:
        for disjoints in range(1, 21):
            for variables in range(max(1, disjoints - 6), disjoints + 1):
                print(generate(variables, disjoints, 5), end='')
    else:
        variables = int(sys.argv[1])
        disjoints = int(sys.argv[2])
        expressions = int(sys.argv[3])
        print(generate(variables, disjoints, expressions), end='')


if '__main__' == __name__:
    main()
