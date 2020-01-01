from evaluator import Evaluator
from timeit import default_timer as timer
import cvxpy as cp
import numpy as np
import sys


def calc_negs(literal_0: str, literal_1: str) -> int:
    return (literal_0 + literal_1).count('-')


def split_space(solution):
    n = len(solution)
    r = np.random.normal(size=n)
    r /= np.sqrt((r ** 2).sum())
    return np.array([v.T @ r >= 0 for v in solution])


def solve(expr: str, num_tests: int = 50, verbose:bool = False) -> tuple:
    start_time = timer()
    ev = Evaluator(expr)
    n = len(ev.variables)
    w = np.zeros((n + 1, n + 1))
    used_vars = ev.get_variables()
    for var_0, var_1 in ev.disjoints:
        for var in (var_0, var_1):
            w[0][used_vars[var[-1]] + 1] += -1 if var[0] != '-' else 1
        i, j = used_vars[var_0[-1]], used_vars[var_1[-1]]
        w[min(i, j) + 1][max(i, j) + 1] += 1 if calc_negs(var_0, var_1) % 2 == 0 else -1
    x = cp.Variable((n + 1, n + 1), PSD=True)
    prob = cp.Problem(cp.Minimize(cp.trace(w @ x)), [
        cp.diag(x) == np.ones(n + 1),
        x.T == x
    ])
    prob.solve(eps=1e-7, verbose=verbose)
    result = np.linalg.cholesky(x.value + np.diag(np.zeros(n + 1) + 1e-6))
    values, scores = [], []
    time_delta = 0
    for _ in range(num_tests):
        # считаем только первую итерацию, потому что время должно считаться ровно для одного
        # запуска алгоритма
        cur = timer()
        value1 = split_space(result)[1:]
        value2 = not value1
        score1 = ev.score(value1)
        score2 = ev.score(value2)
        if score1 > score2:
            values.append(value1)
            scores.append(score1)
        else:
            values.append(value2)
            scores.append(score2)
        if _:
            time_delta += timer() - cur
    return n, values, scores, timer() - start_time - time_delta


def main(show_progress: bool = False, verbose: bool = False):
    cnt = 0
    for line in sys.stdin:
        n, values, scores, time = solve(line.strip(), verbose=verbose)
        print(n, np.mean(scores), time, sep='\t')
        if show_progress:
            cnt += 1
            print(cnt, file=sys.stderr)


if '__main__' == __name__:
    main(show_progress='-p' in sys.argv, verbose='-v' in sys.argv)
