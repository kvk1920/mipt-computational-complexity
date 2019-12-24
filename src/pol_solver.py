from evaluator import Evaluator
import cvxpy


def solve(expr, verbose):
    ev = Evaluator(expr)
    n = len(ev.variables)
    