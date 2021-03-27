import React, { Component } from "react";
import "./App.css";

const Input = (props) => (
  <div className="row" style={{ margin: "5px 0px" }}>
    <div className="col-md-6 col-sm-12 col-xs-12 input-label-container">
      <label className="input-label">{props.label}</label>
    </div>
    <div className="col-md-6 col-sm-12 col-xs-12">
      <input
        type="text"
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
    isValidationLoading: false,
    num_vars: "",
    val_num_vars: "",
    num_clauses: "",
    val_clause: "",
    val_clause_tmp: null,
    clause_res: null,
    solution_res: null,
    validation_res: null,
    validation_res_clause: null,
    validation_res_idx: null,
    validation_vars: [],
  };
  resize_validation_vars = (oldSize, newSize, oldVars) => {
    const vars = [];
    for (var i = 0; i < newSize; i++) {
      if (oldSize > i) {
        vars[i] = oldVars[i];
      } else {
        vars[i] = 1;
      }
    }
    return vars;
  };
  handleGenerate = () => {
    if (this.state.num_vars === "" || this.state.num_clauses === "") {
      alert("Please enter number of variables and number of clauses");
      return;
    }
    this.setState({ isLoading: true, clause_res: null, solution_res: null });
    fetch(
      `generate?num_vars=${this.state.num_vars}&num_clauses=${this.state.num_clauses}`
    )
      .then((data) => data.json())
      .then((data) => {
        this.setState((prevState) => ({
          isLoading: false,
          clause_res: data.clauses,
          solution_res: data.solution,
          val_clause:
            prevState.validation_vars.length === 0
              ? data.clauses
              : prevState.val_clause,
          val_num_vars:
            prevState.validation_vars.length === 0
              ? this.state.num_vars
              : prevState.val_num_vars,
          validation_vars:
            prevState.validation_vars.length === 0
              ? this.resize_validation_vars(
                  prevState.val_num_vars,
                  this.state.num_vars,
                  prevState.validation_vars
                )
              : prevState.validation_vars,
        }));
        this.res_ref.scrollIntoView({ behavior: "smooth" });
      })
      .catch((e) => {
        this.setState({ isLoading: false });
        alert(
          "An error occurred while processing your request, please try again later"
        );
        console.log(e);
      });
  };
  handleValidation = () => {
    if (
      this.state.val_clause === "" ||
      this.state.validation_vars.length === 0
    ) {
      alert(
        "Please enter the clauses and the number of variables to validate your solution"
      );
      return;
    }
    const payload = {
      clauses: this.state.val_clause,
      solution: this.state.validation_vars.map((v, i) =>
        v === 1 ? i + 1 : -(i + 1)
      ),
    };
    this.setState({ isValidationLoading: true, validation_res: null });
    fetch(`validate`, { method: "POST", body: JSON.stringify(payload) })
      .then((response) => {
        if (response.status === 200) {
          this.setState({ validation_res: true, isValidationLoading: false });
          return true;
        } else {
          return response.json();
        }
      })
      .then((data) => {
        if (data === true) {
          return;
        }
        this.setState((prevState) => ({
          validation_res: false,
          validation_res_clause: data.clause,
          validation_res_idx: data.idx,
          isValidationLoading: false,
          val_clause_tmp: prevState.val_clause,
        }));
        this.res_ref.scrollIntoView({ behavior: "smooth" });
      })
      .catch((e) => {
        this.setState({ isValidationLoading: false });
        alert(
          "An error occurred while processing your request, please try again later"
        );
        console.log(e);
      });
  };
  handleOnChange = (event) => {
    var val = event.target.value;
    if (val !== "") {
      if (!/^[0-9]+$/.test(val)) {
        return;
      }
    }
    if (event.target.name === "val_num_vars") {
      if (val === "") {
        val = 0;
      } else {
        val = parseInt(val);
      }
      this.setState((prevState) => {
        var old_val = 0;
        if (prevState.val_num_vars !== "") {
          old_val = parseInt(prevState.val_num_vars);
        }
        const vars = this.resize_validation_vars(
          old_val,
          val,
          prevState.validation_vars
        );
        return {
          val_num_vars: event.target.value,
          validation_vars: vars,
        };
      });
    } else {
      this.setState({ [event.target.name]: val });
    }
  };
  handleRadioChanged = (event) => {
    var { name, value, checked } = event.target;
    value = parseInt(value);
    if (!checked) value = !value;
    const idx = parseInt(name.substr(3));
    this.setState((prevState) => ({
      validation_vars: prevState.validation_vars.map((v, i) =>
        i === idx ? value : v
      ),
    }));
  };
  handleKeyPress = (event) => {
    if (event.key === "Enter") {
      this.handleGenerate();
    }
  };
  render_elements = (source, separator, redIdx = -1) => {
    const elements = source.split(separator);
    return elements.map((v, i) => (
      <div className="d-md-inline-block d-sm-block d-block">
        <label
          style={{
            wordBreak: "keep-all",
            color: redIdx === i ? "red" : "white",
          }}
        >
          {v}
        </label>
        {i !== elements.length - 1 && (
          <label
            style={{
              wordBreak: "keep-all",
              margin: "0px 0.5rem",
            }}
          >
            {separator}
          </label>
        )}
      </div>
    ));
  };
  render() {
    return (
      <div
        className="container page-container"
        onKeyPress={this.handleKeyPress}
      >
        <div className="sat-card">
          <h1 className="title-header">SAT research helper</h1>
          <div className="container-fluid">
            <div className="row">
              <div className="col-md-6 col-sm-12">
                <h3 style={{ textAlign: "center" }}>Clause generation</h3>
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
                <div style={{ padding: "0px 10px" }}>
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
                <p style={{ fontStyle: "italic", padding: "20px" }}>
                  Generated clause will automatically be fed into validation if
                  the validation fields are blank
                </p>
              </div>
              <div className="col-md-1 col-sm-12 col-xs-12">
                <div className="d-md-block d-sm-none d-none vertical-line" />
                <hr className="d-sm-block d-md-none" />
              </div>
              <div className="col-md-5 col-sm-12">
                <h3 style={{ textAlign: "center" }}>Solution validation</h3>
                <Input
                  name="val_clause"
                  label="Clauses"
                  value={this.state.val_clause}
                  onChange={(event) =>
                    this.setState({ val_clause: event.target.value })
                  }
                />
                <Input
                  name="val_num_vars"
                  label="Number of variables"
                  value={this.state.val_num_vars}
                  onChange={this.handleOnChange}
                />
                {this.state.validation_vars.map((val, i) => (
                  <div
                    key={i}
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      paddingRight: "10px",
                      paddingLeft: "1px",
                    }}
                  >
                    <label style={{ marginLeft: "10px" }}>X{i + 1}</label>
                    <div style={{ display: "inline" }}>
                      <div style={{ display: "inline-block" }}>
                        <input
                          name={"rad" + i}
                          type="radio"
                          value={1}
                          checked={val}
                          onChange={this.handleRadioChanged}
                        />
                        <label style={{ marginLeft: "10px" }}>True</label>
                      </div>
                      <div style={{ display: "inline-block" }}>
                        <input
                          name={"rad" + i}
                          type="radio"
                          value={0}
                          checked={!val}
                          onChange={this.handleRadioChanged}
                        />
                        <label style={{ marginLeft: "10px" }}>False</label>
                      </div>
                    </div>
                  </div>
                ))}
                <div style={{ padding: "0px 10px" }}>
                  <button
                    onClick={this.handleValidation}
                    style={{ width: "100%" }}
                    className="btn btn-secondary"
                    disabled={this.state.isValidationLoading}
                  >
                    {this.state.isValidationLoading ? (
                      <div className="spinner-border">
                        <span className="sr-only" />
                      </div>
                    ) : (
                      "Validate Solution"
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
          {(this.state.clause_res != null ||
            this.state.validation_res != null) && (
            <React.Fragment>
              <hr />
              <h1 className="title-header">Results</h1>
            </React.Fragment>
          )}
          {this.state.clause_res != null && (
            <React.Fragment>
              <h3 style={{ textAlign: "center" }}>Generation</h3>
              <div
                style={{
                  marginTop: "10px",
                }}
              >
                <label
                  className="d-none d-sm-none d-md-inline"
                  style={{ fontWeight: "bold" }}
                >
                  Clauses:
                </label>
                <label
                  className="d-block d-sm-block d-md-none"
                  style={{
                    fontWeight: "bold",
                    width: "100%",
                    textAlign: "center",
                  }}
                >
                  Clauses
                </label>
                <div style={{ display: "flex", justifyContent: "center" }}>
                  <div>
                    {this.render_elements(this.state.clause_res, " ^ ")}
                  </div>
                </div>
              </div>
              <div>
                <label
                  className="d-none d-sm-none d-md-inline"
                  style={{ fontWeight: "bold" }}
                >
                  Solution:
                </label>
                <label
                  className="d-block d-sm-block d-md-none"
                  style={{
                    fontWeight: "bold",
                    width: "100%",
                    textAlign: "center",
                  }}
                >
                  Solution
                </label>
                <div style={{ display: "flex", justifyContent: "center" }}>
                  <div>
                    {this.render_elements(this.state.solution_res, ", ")}
                  </div>
                </div>
              </div>
            </React.Fragment>
          )}
          {this.state.validation_res != null && (
            <React.Fragment>
              <h3 style={{ textAlign: "center", marginTop: "15px" }}>
                Validation
              </h3>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-around",
                  alignItems: "center",
                  flexDirection: "column",
                  width: "100%",
                }}
              >
                {this.state.validation_res ? (
                  <label style={{ color: "green" }}>Solution is valid!</label>
                ) : (
                  <React.Fragment>
                    <label>
                      Invalid solution! Clauses marked in red represent the
                      clauses that evaluated to false
                    </label>
                    <div>
                      {this.render_elements(
                        this.state.val_clause_tmp,
                        "^",
                        this.state.validation_res_idx
                      )}
                    </div>
                  </React.Fragment>
                )}
              </div>
            </React.Fragment>
          )}
          <div ref={(e) => (this.res_ref = e)}></div>
        </div>
      </div>
    );
  }
}

export default App;
