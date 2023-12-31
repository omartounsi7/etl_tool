import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link, useNavigate  } from "react-router-dom";
import './upload.css';
import getCookie from './cookies';

const UploadFile = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch the CSRF token and set it in Axios headers
    const csrftoken = getCookie('csrftoken');
    axios.defaults.headers.common['X-CSRFToken'] = csrftoken;
  }, []);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleFileUpload = (fileName) => {
    const formData = new FormData();
    formData.append('csv_file', selectedFile);

    const uploadURL = 'http://127.0.0.1:9000/api/upload-csv/';

    axios.post(uploadURL, formData)
      .then((response) => {
        // Handle successful response
        console.log('File uploaded successfully:', response);
        setSuccessMessage('File uploaded successfully!');
        setErrorMessage(null); // Clear previous error message
        // Redirect to another page
        navigate(`/display-file/${fileName}`);
      })
      .catch((error) => {
        // Handle error
        console.error('Error uploading file:', error);
        setErrorMessage('Error uploading file. Please try again.');
        setSuccessMessage(null); // Clear previous success message
      });
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setSelectedFile(e.dataTransfer.files[0]);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
  };

  return (
    <div>
      {successMessage && <p>{successMessage}</p>}
      {errorMessage && <p>{errorMessage}</p>}
      <h3>Please upload a file:</h3>
      <div
        className="drop-container"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        {selectedFile ? (
          <p>{selectedFile.name}</p>
        ) : (
          <p>Drag and drop a file here or click to select a file.</p>
        )}
      </div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={() => handleFileUpload(selectedFile.name)}>Upload</button>
      <br></br><br></br>
      <Link to="/">Go back to the home page</Link>
    </div>
  );
};

export default UploadFile;


