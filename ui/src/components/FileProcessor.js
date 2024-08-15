import React, { useState } from 'react';

const FileProcessor = () => {
  const [output, setOutput] = useState('');

  const apiUrl = 'http://localhost:8000';

  const getAllFiles = async () => {
    const response = await fetch(`${apiUrl}/files`);
    const data = await response.json();
    setOutput(JSON.stringify(data, null, 2));
  };

  const checkFiles = async () => {
    const response = await fetch(`${apiUrl}/files/check`);
    const data = await response.json();
    setOutput(JSON.stringify(data, null, 2));
  };

  const scanAndSaveFiles = async () => {
    const directory = prompt("Enter directory path to scan:");
    const response = await fetch(`${apiUrl}/files/scan`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ directory })
    });
    const data = await response.json();
    setOutput(JSON.stringify(data, null, 2));
  };

  const processUnconvertedFiles = async () => {
    const response = await fetch(`${apiUrl}/files/process-unconverted`);
    const data = await response.json();
    setOutput(JSON.stringify(data, null, 2));
  };

  const processSingleFile = async () => {
    const filePath = prompt("Enter file path to process:");
    const response = await fetch(`${apiUrl}/files/process-single`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ filePath })
    });
    const data = await response.json();
    setOutput(JSON.stringify(data, null, 2));
  };

  return (
    <div>
      <h1>FastAPI File Processor</h1>
      <button onClick={getAllFiles}>Get All Files</button>
      <button onClick={checkFiles}>Check Existing Files</button>
      <button onClick={scanAndSaveFiles}>Scan and Save Files</button>
      <button onClick={processUnconvertedFiles}>Process Unconverted Files</button>
      <button onClick={processSingleFile}>Process Single File</button>
      <div id="output">
        <pre>{output}</pre>
      </div>
    </div>
  );
};

export default FileProcessor;
