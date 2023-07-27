import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ListFiles = () => {
  const [files, setFiles] = useState([]);

  useEffect(() => {
    // Fetch data from Django API endpoint
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/list-files/');
        setFiles(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const handleDownload = (fileName) => {
    // Construct the URL to download the file
    const downloadURL = `/media/${fileName}`;

    // Create a temporary link and click it to initiate the download
    const link = document.createElement('a');
    link.href = downloadURL;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div>
      <h2>Uploaded Files:</h2>
      {files.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>File Name</th>
              <th>Uploaded At</th>
              <th>Download</th>
            </tr>
          </thead>
          <tbody>
            {files.map((file) => (
              <tr key={file.id}>
                <td>{file.id}</td>
                <td>{file.file_name}</td>
                <td>{new Date(file.uploaded_at).toLocaleDateString()}</td>
                <td>
                  <button onClick={() => handleDownload(file.file_name)}>Download</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No files available.</p>
      )}
    </div>
  );
};

export default ListFiles;
