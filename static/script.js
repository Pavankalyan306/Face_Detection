// static/script.js
function uploadFile() {
    var fileInput = document.getElementById('fileInput');
    var file = fileInput.files[0];

    if (!file) {
        alert('Please select a file.');
        return;
    }

    // Display the loading animation
    var loadingDiv = document.getElementById('loading');
    loadingDiv.style.display = 'block';

    var formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        var resultDiv = document.getElementById('result');
        resultDiv.innerHTML = data.result;

        // Display the uploaded image
        var uploadedImageContainer = document.getElementById('uploadedImageContainer');
        uploadedImageContainer.innerHTML = `<img id="uploadedImage" src="${URL.createObjectURL(file)}" alt="Uploaded Face" style="max-width: 150px; max-height: 150px;">`;

        // Display the result and known face image
        if (data.name) {
    resultDiv.innerHTML += ` Recognized as: ${data.name}`;

    // Update the known face image container using JavaScript
    var knownFaceImageContainer = document.getElementById('knownFaceImageContainer');
    knownFaceImageContainer.innerHTML = ''; // Clear previous content
    var knownFaceImage = document.createElement('img');
    knownFaceImage.src = `static/known_faces/${data.name}.jpg`;
    knownFaceImage.alt = 'Known Face';
    knownFaceImage.style.maxWidth = '150px';
    knownFaceImage.style.maxHeight = '150px';
    knownFaceImage.style.margin = '0 auto';
    knownFaceImageContainer.appendChild(knownFaceImage);
     }

        // Hide the loading animation after completing the fetch request
        loadingDiv.style.display = 'none';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');

        // Hide the loading animation in case of an error
        loadingDiv.style.display = 'none';
    });
}

function reloadPage() {
    console.log('Reload button clicked');
    location.reload();
}

function resetPage() {
    console.log('Reset button clicked');
    var uploadedImageContainer = document.getElementById('uploadedImageContainer');
    var resultDiv = document.getElementById('result');
    var knownFaceImageContainer = document.getElementById('knownFaceImageContainer');

    // Clear the uploaded image, result, and known face image containers
    uploadedImageContainer.innerHTML = '';
    resultDiv.innerHTML = '';
    knownFaceImageContainer.innerHTML = '';
}
