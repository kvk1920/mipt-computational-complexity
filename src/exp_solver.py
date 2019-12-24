from evaluator import Evaluator
import sys


def solve(expr, verbose):
    ev = Evaluator(expr)
    best = 0
    desc = None
    for i in range(2 ** len(ev.variables)):
        values = []
        j = i
        while j:
            values.append(j % 2 == 1)
            j /= 2
        cur = ev.score(values)
        if cur > best:
            desc = ev.get_values(values)
            best = cur
    print(best)
    if verbose:
        print(desc, file=sys.stderr)


def main(verbose):
    for line in sys.stdin:
        if verbose:
            print(line.strip(), file=sys.stderr)
        solve(line.strip(), verbose)


if '__main__' == __name__:
    main('-v' in sys.argv)

