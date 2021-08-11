from flask import Flask, request, render_template
from flask.helpers import send_file
from flask.wrappers import Response
from flask_json import FlaskJSON, json_response
from main import generate_clauses_strings, load_clauses, validate_solution, clause_to_string
from os import getenv

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
    status, errored_clauses, idx = validate_solution(clauses, solution)
    if status:
        return json_response(status_=200)
    else:
        return json_response(status_=202, clause=[f"({clause_to_string(x)})" for x in errored_clauses], idx=idx)

@app.route('/shuffle', methods=["POST"])
def shuffle():
    try:
        file = request.files["file"]
    except Exception:
        return json_response(status_=400)
    file.seek(0)
    data = file.read().decode("utf-8")
    file.close()
    return Response(data)

if __name__ == "__main__":
    port = getenv("PORT", "5000")
    app.run(host="0.0.0.0", port=port)
