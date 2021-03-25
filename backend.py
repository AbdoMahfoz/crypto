from flask import Flask, request, render_template
from flask_json import FlaskJSON, json_response
from main import generate_clauses

app = Flask(__name__)
FlaskJSON(app)


@app.route('/')
def get():
    return render_template("index.html")


@app.route('/generate')
def post():
    n = int(request.args.get("num_vars"))
    m = int(request.args.get("num_clauses"))
    clauses, solution = generate_clauses(n, m)
    return json_response(clauses=clauses, solution=solution)
