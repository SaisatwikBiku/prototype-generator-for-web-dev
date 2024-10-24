// Form submission to generate prototype
document.getElementById('prototypeForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const description = document.getElementById('description').value;
    const loadingSpinner = document.getElementById('loading-spinner');
    const generatedCodePre = document.getElementById('generated-code-pre');

    if (!description) {
        alert('Please enter a description.');
        return;
    }

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
    .then(response => {
        if (!response.ok) {
            throw new Error('Error: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        // Hide the loading spinner
        loadingSpinner.style.display = 'none';

        if (data.generated_code) {
            // Display the generated prototype code
            generatedCodePre.textContent = data.generated_code;
        } else {
            generatedCodePre.textContent = 'Error: ' + (data.error || 'Unknown error');
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
    if (!generatedCode) {
        alert('No code to copy!');
        return;
    }

    navigator.clipboard.writeText(generatedCode)
    .then(() => {
        alert("Code copied to clipboard!");
    })
    .catch(err => {
        alert("Failed to copy: " + err);
    });
});

// Run the generated code in a new pop-up window
document.getElementById('run-button').addEventListener('click', function() {
    const generatedCode = document.getElementById('generated-code-pre').textContent;
    if (!generatedCode) {
        alert('No code to run!');
        return;
    }

    // Open a new window
    const newWindow = window.open('', '_blank');

    // Write the generated code into the new window's document
    newWindow.document.open();
    newWindow.document.write(generatedCode);
    newWindow.document.close();
});

// Toggle dark mode and save preference to local storage
const toggleSwitch = document.getElementById('dark-mode-toggle');
const currentTheme = localStorage.getItem('theme');

if (currentTheme) {
    document.body.classList.add(currentTheme);
}

// Toggle theme on button click and save to local storage
toggleSwitch.addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');

    let theme = 'light';
    if (document.body.classList.contains('dark-mode')) {
        theme = 'dark-mode';
    }
    localStorage.setItem('theme', theme);
});

// Show "Go to Top" button when scrolling
const goToTopBtn = document.getElementById('go-to-top');

window.onscroll = function() {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        goToTopBtn.style.display = 'block'; // Show the button when scrolled down
    } else {
        goToTopBtn.style.display = 'none'; // Hide the button when near the top
    }
};

// Scroll to the top when the "Go to Top" button is clicked
goToTopBtn.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' }); // Smooth scrolling to top
});
