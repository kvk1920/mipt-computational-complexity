from evaluator import Evaluator
import cvxpy as cp
import numpy as np
import scipy.stats as sps
import sys


def calc_negs(literal_0: str, literal_1: str) -> int:
    return (literal_0 + literal_1).count('-')


def split_space(solution):
    n = len(solution)
    r = sps.norm.rvs(size=n)
    return np.array([v.T @ r >= 0 for v in solution])


def solve(expr: str, num_tests: int = 50) -> tuple:
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
    prob.solve(eps=1e-7)
    result = np.linalg.cholesky(x.value + np.diag(np.zeros(n + 1) + 1e-6))
    values, scores = [], []
    for _ in range(num_tests):
        values.append(split_space(result))
        scores.append(max(ev.score(values[-1]), ev.score(np.ones(n + 1) - values[-1])))
    return values, scores


def main():
    for line in open("test"):
        values, scores = solve(line.strip())
        print("2sat:", line.strip(), "mean score:", np.mean(scores), sep='\n')


if '__main__' == __name__:
    main()
