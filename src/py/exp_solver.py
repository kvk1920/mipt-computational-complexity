from evaluator import Evaluator
from timeit import default_timer as timer
import sys


def solve(expr, verbose: bool = False, show_progress: bool = False) -> None:
    start_time = timer()
    ev = Evaluator(expr)
    best = 0
    desc = None
    nxt = 10
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
        if show_progress and i * 100 / (2 ** len(ev.variables)) >= nxt:
            print(round(i * 100 / (2 ** len(ev.variables)), 2), "%", sep='', file=sys.stderr)
            nxt += 10
    print(len(ev.variables), best, timer() - start_time, sep='\t')
    if verbose:
        print(desc, file=sys.stderr)


def main(verbose: bool, show_progress: bool) -> None:
    cnt = 0
    for line in sys.stdin:
        if verbose:
            print(line.strip(), file=sys.stderr)
        solve(line.strip(), verbose=verbose, show_progress=show_progress)
        if show_progress:
            cnt += 1
            print("solved:", cnt, file=sys.stderr)


if '__main__' == __name__:
    main('-v' in sys.argv, '-p' in sys.argv)

