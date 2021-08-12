import numpy as np
from pysat.solvers import Glucose3
from sys import argv
from random import Random
from zipfile import ZipFile
from io import BytesIO


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

def shuffle_clauses(clauses: "list[list[int]]", count: int = 1) -> "list[list[list[int]]]":
    if count <= 1:
        return __shuffle_helper(clauses)
    res = []
    for _ in range(count):
        res.append(__shuffle_helper(clauses))
    return res

def __shuffle_helper(clauses: "list[list[int]]") -> "list[list[int]]":
    positives = {}
    negatives = {}
    for i in range(len(clauses)):
        for var in clauses[i]:
            if var > 0:
                if var in positives:
                    positives[var] += 1
                else:
                    positives[var] = 1
            else:
                if abs(var) in negatives:
                    negatives[abs(var)] += 1
                else:
                    negatives[abs(var)] = 1
    res = []
    new_clause = []
    rand = Random()
    rand.seed()
    for clause in clauses:
        for val in clause:
            if val > 0:
                dic = positives
            else:
                dic = negatives
            k = rand.choice(list(dic.keys()))
            new_clause.append(k if val > 0 else (k * -1))
            dic[k] -= 1
            if dic[k] == 0:
                del dic[k]
        res.append(list(new_clause))
        new_clause.clear()
    return res

def load_clauses_from_file(file: str) -> "list[list[int]]":
    lines = file.splitlines()
    clasues = []
    for i in range(len(lines)):
        line = lines[i].strip().lower()
        while '  ' in line:
            line = line.replace('  ', ' ')
        if i == 0:
            if line.startswith('p cnf'):
                try:
                    n, c = tuple(int(x) for x in line[len('p cnf'):].strip().split(' '))
                    if n > 0 and c > 2:
                        continue
                except Exception:
                    pass
            raise Exception("Invalid values in first line")
        try:
            nums = [int(x.strip()) for x in line.split(' ')]
        except Exception:
            raise Exception(f"Line #{i} included non integral values")
        if nums[-1] != 0:
            raise Exception(f"Line #{i} wasn't terminated with a 0")
        clasues.append(nums[:-1])
    return clasues

def clauses_to_file(clauses: "list[list[int]]") -> str:
    lines = []
    var_count = 0
    for clause in clauses:
        var_count = max(var_count, max(clause))
        lines.append(" ".join(str(x) for x in clause) + " 0")
    lines.insert(0, f"p cnf {var_count} {len(lines)}")
    return '\n'.join(lines)

def zip_clauses(clauses: "list[list[list[int]]]"):
    res = BytesIO()
    zipfile = ZipFile(res, "w")
    for i in range(len(clauses)):
        zipfile.writestr(f"{i+1}.txt", clauses_to_file(clauses[i]))
    zipfile.close()
    res.seek(0)
    return res.read()

def load_clauses(case: str) -> "list[tuple[int]]":
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
    failed_clauses = []
    failed_clauses_idx = []
    for idx in range(len(clauses)):
        found_true = False
        for x in clauses[idx]:
            if x * truth_table[abs(x)] > 0:
                found_true = True
                break
        if not found_true:
            failed_clauses.append(clauses[idx])
            failed_clauses_idx.append(idx)
    if len(failed_clauses) == 0:
        return True, None, None
    else:
        return False, failed_clauses, failed_clauses_idx


def generate_clauses(n, m=-1):
    clauses = generate_clause_space(n)
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
    return clauses, solution


def clause_to_string(clause):
    clause = ' v '.join([f"x{y}" if y > 0 else f"-x{abs(y)}" for y in clause])
    return clause


def generate_clauses_strings(n, m=-1):
    clauses, solution = generate_clauses(n, m)
    all_possible_clauses = len(clauses)
    clauses = [clause_to_string(x) for x in clauses]
    clauses = '(' + ') ^ ('.join(clauses) + ')'
    solution = ", ".join([f"x{n} = True" if n > 0 else f"x{abs(n)} = False" for n in solution])
    return clauses, solution, all_possible_clauses


def print_clauses(n, m=-1):
    clauses, solution, all_possible_clauses = generate_clauses_strings(n, m)
    print(f"Number of all possible clauses = {all_possible_clauses}")
    print('Problem: ' + clauses)
    print("Solution: " + solution)


def validate_solution_with_print(case, solution):
    clauses = load_clauses(case)
    solution = load_solution(solution)
    status, clause, idx = validate_solution(clauses, solution)
    if status:
        print("Solution is valid")
    else:
        print("Invalid Solution\nThe following clause wasn't true: (" +
              " v ".join(f'x{i}' if i > 0 else f'-x{abs(i)}' for i in clause) +
              f") which is clause #{idx}")


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
        validate_solution_with_print(case, solution)
    else:
        n = int(input(prompt[3]))
        m = int(input(prompt[4]))
        print_clauses(n, m)
