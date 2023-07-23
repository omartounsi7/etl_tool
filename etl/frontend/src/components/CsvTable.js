import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Papa from 'papaparse';

const CsvTable = () => {
  const [csvData, setCsvData] = useState([]);
  const [headers, setHeaders] = useState([]);

  useEffect(() => {
    fetchCsvData();
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

  return (
    <div>
      <h1>CSV File</h1>
      <table>
        <thead>{renderTableHeaders()}</thead>
        <tbody>{renderTableRows()}</tbody>
      </table>
    </div>
  );
};

export default CsvTable;
