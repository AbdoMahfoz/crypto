import numpy as np
from pysat.solvers import Glucose3
from sys import argv


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


def load_case(case: str):
    case = case.replace('(', '')
    case = case.replace(')', '')
    case = case.replace('x', '')
    clauses = [tuple(int(x) for x in y.split('v')) for y in case.split('^')]
    return clauses


def load_solution(solution: str):
    return [int(x) for x in solution.split(',')]


def validate_solution(clauses, solution):
    truth_table = {}
    for v in solution:
        truth_table[abs(v)] = 1 if v > 0 else -1
    for idx in range(len(clauses)):
        found_true = False
        for x in clauses[idx]:
            if x * truth_table[abs(x)] > 0:
                found_true = True
                break
        if not found_true:
            print("The following clause wasn't true: (" +
                  " v ".join(f'x{i}' if i > 0 else f'-x{abs(i)}' for i in clauses[idx]) +
                  f") which is clause #{idx}")
            return False
    return True


def generate_clauses(n, m=-1):
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
    clauses_str = '(' + ') ^ ('.join(clauses) + ')'
    solution_str = ", ".join([f"x{n} = True" if n > 0 else f"x{abs(n)} = False" for n in solution])
    return clauses_str, solution_str


def print_clauses(n, m=-1):
    clauses, solution = generate_clauses(n, m)
    print('Problem: ' + clauses)
    print("Solution: " + solution)


def validate_case(case, solution):
    clauses = load_case(case)
    solution = load_solution(solution)
    if validate_solution(clauses, solution):
        print("Solution is valid")
    else:
        print("Invalid solution")


if __name__ == "__main__":
    if len(argv) > 1 and argv[1] == "--no-prompt":
        prompt = ['' for _ in range(5)]
    else:
        prompt = [
            'Input 1 for generating cases and 2 for validating solution: ',
            'Enter case: ',
            'Enter solution: ',
            'Enter number of variables: ',
            'Enter number of clauses or -1 to generate all possible clauses: '
        ]
    mode = int(input(prompt[0]))
    if mode == 2:
        case = input(prompt[1])
        solution = input(prompt[2])
        validate_case(case, solution)
    else:
        n = int(input(prompt[3]))
        m = int(input(prompt[4]))
        print_clauses(n, m)
