import numpy as np
from pysat.solvers import Glucose3


def __generator_helper(i, n, tmp_ans, final_ans):
    if i == 3:
        final_ans.append(tuple(tmp_ans))
        return
    for j in range(abs(tmp_ans[-1]) + 1 if len(tmp_ans) > 0 else 1, n - 1 + i, 1):
        tmp_ans.append(j)
        __generator_helper(i + 1, n, tmp_ans, final_ans)
        tmp_ans[-1] = j * -1
        __generator_helper(i + 1, n, tmp_ans, final_ans)
        tmp_ans.pop(-1)


def generate_clause_space(n):
    tmp_ans = []
    final_ans = []
    __generator_helper(0, n, tmp_ans, final_ans)
    return final_ans


def solve(clauses):
    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)
    if not solver.solve():
        return False, []
    return True, solver.get_model()


def print_clauses(n, m=-1):
    clauses = generate_clause_space(n)
    print(f"Number of all possible clauses = {len(clauses)}")
    trials = 1
    while True:
        if m != -1:
            idxs = np.random.choice(np.arange(0, len(clauses)), m)
            clauses = [clauses[i] for i in idxs]
        status, solution = solve(clauses)
        if not status:
            if m == -1 or trials > 20:
                print("Unsolvable")
                return
            else:
                trials += 1
                continue
        break
    clauses = [' v '.join([f"x{y}" if y > 0 else f"-x{abs(y)}" for y in x]) for x in clauses]
    print('Problem: (' + ') ^ ('.join(clauses) + ')')
    print("Solution: " + ", ".join([f"x{n} = True" if n > 0 else f"x{abs(n)} = False" for n in solution]))


if __name__ == "__main__":
    print_clauses(*[int(x) for x in input().split()])
