import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const ListFiles = () => {
  const [files, setFiles] = useState([]);

  useEffect(() => {
    // Fetch data from Django API endpoint
    const fetchData = async () => {

        // Fetch the CSRF token and set it in Axios headers
        const csrftoken = getCookie('csrftoken');
        axios.defaults.headers.common['X-CSRFToken'] = csrftoken;

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

  const handleDelete = async (fileName) => {
    try {
      // Call the API to delete the file
      const response = await axios.delete(`/api/delete-csv/?file_name=${fileName}`);
      console.log(response.data); // Log the response from the server

      // Update the files state to reflect the deletion
      setFiles((prevFiles) => prevFiles.filter((file) => file.file_name !== fileName));
    } catch (error) {
      console.error('Error deleting file:', error);
    }
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
              <th>Delete</th>
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
                <td>
                  <button onClick={() => handleDelete(file.file_name)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No files available.</p>
      )}
      <br />
      <Link to="/">Go back to the home page</Link>
    </div>
  );
};

function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}

export default ListFiles; 