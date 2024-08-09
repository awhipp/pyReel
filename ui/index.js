const apiUrl = 'http://localhost:8000';

async function getAllFiles() {
    const response = await fetch(`${apiUrl}/files`);
    const data = await response.json();
    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
}

async function checkFiles() {
    const response = await fetch(`${apiUrl}/files/check`);
    const data = await response.json();
    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
}

async function scanAndSaveFiles() {
    const directory = prompt("Enter directory path to scan:");
    const response = await fetch(`${apiUrl}/files/scan`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ directory })
    });
    const data = await response.json();
    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
}

async function processUnconvertedFiles() {
    const response = await fetch(`${apiUrl}/files/process`, {
        method: 'POST'
    });
    const data = await response.json();
    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
}

async function processSingleFile() {
    const filePath = prompt("Enter file path to process:");
    const response = await fetch(`${apiUrl}/files/process/single`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ file_path: filePath })
    });
    const data = await response.json();
    document.getElementById('output').innerText = JSON.stringify(data, null, 2);
}
