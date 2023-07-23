import React from "react";
import UploadFile from "./UploadFile";
import { Routes, Route, Link } from "react-router-dom";
import CsvTable from "./CsvTable";

export default function HomePage() {
  return (
    <div>
      <h1>Welcome to my custom ETL tool.</h1>
      <Routes>
        <Route path="/upload-success" element={<CsvTable />} /> 
        <Route path="/upload" element={<UploadFile />} />
        <Route path="/" element={
        <><p>You are currently on the home page.</p>
        <h3>To start, please click on the link below to upload a csv file.</h3>
        <nav>
          <ul>
            <li>
              <Link to="/upload">Upload file</Link>
            </li>
          </ul>
        </nav>
        </>
        }/>
      </Routes>
    </div>
  );
}
