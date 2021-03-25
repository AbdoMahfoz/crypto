import React, { Component } from "react";
import "./App.css";

const Input = (props) => (
  <div className="row" style={{ margin: "5px 0px" }}>
    <div className="form-group">
      <label className="input-label">{props.label}</label>
      <input
        name={props.name}
        value={props.value}
        onChange={props.onChange}
        style={{ float: "right" }}
        className="form-control"
      />
    </div>
    <br />
  </div>
);

class App extends Component {
  state = {
    isLoading: false,
    num_vars: "",
    num_clauses: "",
    clause_res: null,
    solution_res: null,
  };
  handleGenerate = () => {
    if (this.state.num_vars === "" || this.state.num_clauses === "") {
      alert("Please enter number of variables and number of clauses");
      return;
    }
    this.setState({ isLoading: true });
    fetch(
      `generate?num_vars=${this.state.num_vars}&num_clauses=${this.state.num_clauses}`,
      { mode: "no-cors" }
    )
      .then((data) => data.json())
      .then((data) =>
        this.setState({
          isLoading: false,
          clause_res: data.clauses,
          solution_res: data.solution,
        })
      );
  };
  handleOnChange = (event) => {
    var val = event.target.value;
    if (val !== "") {
      if (!/^[0-9]+$/.test(val)) {
        return;
      }
    }
    this.setState({ [event.target.name]: val });
  };
  render() {
    return (
      <div className="container">
        <div className="jumbotron">
          <h1 className="title-header">SAT research helper</h1>
          <div className="container-fluid">
            <Input
              name="num_vars"
              label="Number of variables"
              value={this.state.num_vars}
              onChange={this.handleOnChange}
            />
            <Input
              name="num_clauses"
              label="Number of clauses"
              value={this.state.num_clauses}
              onChange={this.handleOnChange}
            />
            <div className="container">
              <button
                onClick={this.handleGenerate}
                style={{ width: "100%" }}
                className="btn btn-secondary"
                disabled={this.state.isLoading}
              >
                {this.state.isLoading ? (
                  <div className="spinner-border">
                    <span className="sr-only" />
                  </div>
                ) : (
                  "Generate"
                )}
              </button>
            </div>
            {this.state.clause_res != null && (
              <div style={{ marginTop: "10px" }}>
                <label style={{ fontWeight: "bold" }}>Clauses: </label>
                <p>{this.state.clause_res}</p>
              </div>
            )}
            {this.state.solution_res != null && (
              <div>
                <label style={{ fontWeight: "bold" }}>Solution: </label>
                <p>{this.state.solution_res}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }
}

export default App;
