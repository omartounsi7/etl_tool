import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Papa from 'papaparse';
import { Link } from 'react-router-dom';

const CsvTable = () => {
  const [csvData, setCsvData] = useState([]);
  const [headers, setHeaders] = useState([]);
  const [rowData, setRowData] = useState('');
  const [colData, setColData] = useState('');
  const [numberData, setNumberData] = useState('');
  const [opData, setOpData] = useState('add');
  const [errorMessage, setErrorMessage] = useState('');

  useEffect(() => {
    fetchCsvData();
    const csrftoken = getCookie('csrftoken');
    axios.defaults.headers.common['X-CSRFToken'] = csrftoken;
  }, []);

  const fetchCsvData = async () => {
    try {
      const response = await axios.get('/api/get-csv/');
      const parsedCsvData = parseCsvData(response.data.csv_data);
      setCsvData(parsedCsvData.data);
      setHeaders(parsedCsvData.meta.fields);
    } catch (error) {
      console.error('Error fetching CSV data:', error);
    }
  };

  const parseCsvData = (csvData) => {
    return Papa.parse(csvData, {
      header: true,
      skipEmptyLines: true,
      dynamicTyping: true,
    });
  };

  const renderTableHeaders = () => {
    return (
      <tr>
        {headers.map((header) => (
          <th key={header}>{header}</th>
        ))}
      </tr>
    );
  };

  const renderTableRows = () => {
    return csvData.map((row, index) => (
      <tr key={index}>
        {headers.map((header) => (
          <td key={header}>{row[header]}</td>
        ))}
      </tr>
    ));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/api/transform-csv/', {
        row: rowData,
        col: colData,
        number: numberData,
        op: opData,
      });

      // If the request is successful, update the CSV data with the response data
      setCsvData(parseCsvData(response.data.csv_data).data);
      setErrorMessage('');
    } catch (error) {
      console.error('Error transforming CSV field:', error);
      setErrorMessage('An error occurred while transforming the data. You may have tried to transform an field text or out of bounds field.'); // Update the error message state
    }
  };

  return (
    <div>
      <h1>Your CSV file</h1>
      <table>
        <thead>{renderTableHeaders()}</thead>
        <tbody>{renderTableRows()}</tbody>
      </table>

      <br /><br />

      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}

      <form onSubmit={handleSubmit}>
        <label>
          Row:
          <input type="text" value={rowData} onChange={(e) => setRowData(e.target.value)} />
        </label>
        <br />
        <label>
          Column:
          <input type="text" value={colData} onChange={(e) => setColData(e.target.value)} />
        </label>
        <br />
        <label>
          Number:
          <input type="number" value={numberData} onChange={(e) => setNumberData(e.target.value)} />
        </label>
        <br />
        <label>
          Operation:
          <select value={opData} onChange={(e) => setOpData(e.target.value)}>
            <option value="add">Addition (+)</option> 
            <option value="sub">Subtraction (-)</option>
            <option value="mul">Multiplication (*)</option>
            <option value="div">Division (/)</option>
          </select>
        </label>
        <br />
        <button type="submit">Apply Transformation</button>
      </form>
      <p>Rows and columns are one-indexed.</p>

      <br />
      <Link to="/upload">Upload another file</Link>
      <br />
      <Link to="/">Go back to the home page</Link>
    </div>
  ); 
};

function getCookie(name) {
  const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return cookieValue ? cookieValue.pop() : '';
}

export default CsvTable;
