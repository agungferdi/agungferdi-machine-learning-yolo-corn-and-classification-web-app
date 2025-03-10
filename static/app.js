let cumulativeCount = 0;

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const cameraButton = document.getElementById('cameraButton');
    const resultsSection = document.getElementById('resultsSection');
    const resultImage = document.getElementById('resultImage');
    const goodCorn = document.getElementById('goodCorn');
    const whiteFungus = document.getElementById('whiteFungus');
    const blackFungus = document.getElementById('blackFungus');
    const cornFragments = document.getElementById('cornFragments');
    const totalKernels = document.getElementById('totalKernels');
    const resetButton = document.getElementById('resetButton');
    const cumulativeCountDisplay = document.getElementById('cumulativeCount');

    uploadForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData();
        const fileInput = document.getElementById('fileInput').files[0];
        formData.append('file', fileInput);
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => showResults(data))
        .catch(error => console.error('Error:', error));
    });

    cameraButton.addEventListener('click', function() {
        fetch('/camera', {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => showResults(data))
        .catch(error => console.error('Error:', error));
    });

    resetButton.addEventListener('click', function() {
        cumulativeCount = 0;
        cumulativeCountDisplay.textContent = `Cumulative Count: ${cumulativeCount}`;
        resetButton.style.display = 'none';
    });
});

function showResults(data) {
    const resultImage = document.getElementById('resultImage');
    const goodCorn = document.getElementById('goodCorn');
    const whiteFungus = document.getElementById('whiteFungus');
    const blackFungus = document.getElementById('blackFungus');
    const cornFragments = document.getElementById('cornFragments');
    const totalKernels = document.getElementById('totalKernels');
    const resultsSection = document.getElementById('resultsSection');
    const resetButton = document.getElementById('resetButton');
    const cumulativeCountDisplay = document.getElementById('cumulativeCount');
    
    if (data.error) {
        alert(data.error);
    } else {
        resultImage.src = `/static/${data.image}`;
        goodCorn.textContent = `${data.counts.jagung}`;
        whiteFungus.textContent = `${data.counts.putih}`;
        blackFungus.textContent = `${data.counts.hitam}`;
        cornFragments.textContent = `${data.counts.serpihan}`;
        totalKernels.textContent = `${data.total}`;

        
        cumulativeCount += data.total;
        cumulativeCountDisplay.textContent = `Cumulative Count: ${cumulativeCount}`;

        resultsSection.style.display = 'block';
        resetButton.style.display = 'inline-block';
    }
}