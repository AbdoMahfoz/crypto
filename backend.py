from flask import Flask, request, render_template
from flask_json import FlaskJSON, json_response
from main import generate_clauses_strings, load_clauses, validate_solution, clause_to_string

app = Flask(__name__)
FlaskJSON(app)


@app.route('/')
def get():
    return render_template("index.html")


@app.route('/generate')
def post():
    try:
        n = int(request.args.get("num_vars"))
        m = int(request.args.get("num_clauses"))
    except (ValueError, KeyError):
        return json_response(status_=400)
    clauses, solution, _ = generate_clauses_strings(n, m)
    return json_response(clauses=clauses, solution=solution)


@app.route('/validate', methods=["POST"])
def validate():
    obj = request.get_json(force=True)
    try:
        clauses = load_clauses(obj["clauses"])
        solution = obj["solution"]
    except (ValueError, KeyError):
        return json_response(status_=400)
    status, clause, idx = validate_solution(clauses, solution)
    if status:
        return json_response(status_=200)
    else:
        return json_response(status_=202, clause=f"({clause_to_string(clause)})", idx=idx)
