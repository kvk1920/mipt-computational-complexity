class Evaluator:

    @staticmethod
    def parse_disjoint(disjoint):
        var = disjoint.lstrip('(').rstrip(')').split('+')
        return (var[0], var[1])

    def __init__(self, expr):
        all_vars = expr.encode('ascii', 'ignore')\
            .translate(None, b'+-*()').decode()
        self.variables = set(all_vars)
        self.disjoints = list(map(Evaluator.parse_disjoint, expr.split('*')))

    def score(self, value_set):
        values = dict(zip(self.variables, value_set))
        res = 0
        for disjoint in self.disjoints:
            x = values.get(disjoint[0][-1], False)
            y = values.get(disjoint[1][-1], False)
            if '-' == disjoint[0][0]:
                x = not x
            if '-' == disjoint[1][0]:
                y = not y
            if x or y:
                res += 1
        return res

    def get_values(self, value_set):
        values = dict(zip(self.variables, value_set))
        res = ''
        for v in self.variables:
            res += '{} = {};\n'.format(v, values.get(v, False))
        return res

    def evaluate(self, value_set):
        values = dict(zip(self.variables, value_set))
        res = 0
        for x, y in self.disjoints:
            vx = values.get(x[-1], False)
            vy = values.get(y[-1], False)
            if '-' == x[0]:
                vx = not vx
            if '-' == y[0]:
                vy = not vy
            if vx or vy:
                res += 1
        return res
