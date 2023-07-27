import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Papa from 'papaparse';
import { Link, useParams } from 'react-router-dom';
import getCookie from './cookies';

const CsvTable = () => {
  const [csvData, setCsvData] = useState([]);
  const [headers, setHeaders] = useState([]);
  const [startRowData, setStartRowData] = useState('');
  const [startColData, setStartColData] = useState('');

  const [endRowData, setEndRowData] = useState('');
  const [endColData, setEndColData] = useState('');

  const [numberData, setNumberData] = useState('');
  const [opData, setOpData] = useState('add');
  const [errorMessage, setErrorMessage] = useState('');

  const { fileName } = useParams();

  useEffect(() => {
    fetchCsvData(fileName);
    const csrftoken = getCookie('csrftoken');
    axios.defaults.headers.common['X-CSRFToken'] = csrftoken;
  }, []);

  const fetchCsvData = async () => {
    try {
      const response = await axios.get('/api/get-csv/', { params: { file_name: fileName } });
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
        startRow: startRowData,
        startCol: startColData,
        endRow: endRowData,
        endCol: endColData,
        number: numberData, 
        op: opData,
      });

      // If the request is successful, update the CSV data with the response data
      setCsvData(parseCsvData(response.data.csv_data).data);
      setErrorMessage('');
    } catch (error) {
      console.error('Error transforming CSV field:', error);
      setErrorMessage('An error occurred while transforming the data. You may have entered invalid coordinates or tried to transform a text field or an out of bounds field.'); // Update the error message state
    }
  };

  return (
    <div>
      <h2>Your CSV file</h2>
      <h3>{fileName}</h3>
      <table>
        <thead>{renderTableHeaders()}</thead>
        <tbody>{renderTableRows()}</tbody>
      </table>
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
      <p>If you wish to modify one field only, enter the start coordinates and leave the end coordinates blank.</p>
      <form onSubmit={handleSubmit}>
        <label>
          Start row:
          <input type="text" value={startRowData} onChange={(e) => setStartRowData(e.target.value)} />
        </label>
        <br />
        <label>
          Start column:
          <input type="text" value={startColData} onChange={(e) => setStartColData(e.target.value)} />
        </label>
        <br />

        <label>
          End row:
          <input type="text" value={endRowData} onChange={(e) => setEndRowData(e.target.value)} />
        </label>
        <br />
        <label>
          End column:
          <input type="text" value={endColData} onChange={(e) => setEndColData(e.target.value)} />
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

export default CsvTable;
