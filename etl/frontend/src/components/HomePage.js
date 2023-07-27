import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import ListFiles from "./ListFiles"
import CsvTable from "./CsvTable";
import UploadFile from "./UploadFile";

export default function HomePage() {
  return (
    <div>
      <h1>Welcome to my custom ETL tool!</h1>
      <Routes>
        <Route path="/list-files" element={<ListFiles />} /> 
        <Route path="/display-file" element={<CsvTable />} /> 
        <Route path="/upload" element={<UploadFile />} />
        <Route path="/" element={
        <>
        <h3>To start, please choose an option below.</h3>
        <nav>
          <ul>
            <li>
              <Link to="/upload">Upload a new file</Link> 
            </li>
            <li>
              <Link to="/list-files">Retrieve an existing file</Link>
            </li>
          </ul>
        </nav>
        </>
        }/>
      </Routes>
    </div>
  );
}
