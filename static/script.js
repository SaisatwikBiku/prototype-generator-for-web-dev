// Few parts of this scrips consists of GenAI generated code. They are commented.

document.getElementById('prototypeForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const description = document.getElementById('description').value;
    const loadingSpinner = document.getElementById('loading-spinner');
    const generatedCodePre = document.getElementById('generated-code-pre');

    // Show the loading spinner
    loadingSpinner.style.display = 'inline-block';
    loadingSpinner.innerHTML = '<div class="spinner"></div>';

    // Send description to backend and fetch the generated prototype
    fetch('/generate-prototype', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'description': description
        })
    })
    .then(response => response.json())
    .then(data => {
        // Hide the loading spinner
        loadingSpinner.style.display = 'none';

        if (data.generated_code) {
            // Display the generated prototype code
            generatedCodePre.textContent = data.generated_code;
        } else {
            generatedCodePre.textContent = 'Error: ' + (data.error || 'Error');
        }
    })
    .catch(error => {
        // Hide the loading spinner
        loadingSpinner.style.display = 'none';
        generatedCodePre.textContent = 'Error: ' + error.message;
    });
});

// Copy the generated code to clipboard
document.getElementById('copy-button').addEventListener('click', function() {
    const generatedCode = document.getElementById('generated-code-pre').textContent;
    navigator.clipboard.writeText(generatedCode).then(() => {
        alert("Code copied to clipboard!");
    }).catch(err => {
        alert("Failed to copy: " + err);
    });
});

// Run the generated code in a new pop-up window
document.getElementById('run-button').addEventListener('click', function() {
    const generatedCode = document.getElementById('generated-code-pre').textContent;

    // Open a new window
    const newWindow = window.open('', '_blank');

    // Write the generated code into the new window's document
    newWindow.document.open();
    newWindow.document.write(generatedCode);
    newWindow.document.close();
});
