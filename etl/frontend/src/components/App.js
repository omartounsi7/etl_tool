import React from "react";
import ReactDOM from "react-dom";
import HomePage from "./HomePage";
import { BrowserRouter as Router } from "react-router-dom";

function App() {
  return (
    <div>
      <Router>
        <HomePage />
      </Router>
    </div>
  );
}

const appDiv = document.getElementById("app");
ReactDOM.render(<App />, appDiv);
