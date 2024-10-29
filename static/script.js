//This code is being built simultaneously by all team members.

//The contribution is clearly mentioned in the following Format: '{Team Member Name} - Team Member's Contribution'

//Whenever a Team member make any change pushes the code, they will highlight their part of the contribution with comments.

//This source code has few components created using ChatGPT-4o and they are clearly mentioned.


// Sai Ram Navuluri - Form submission to generate prototype with additional questions
document.getElementById('prototypeForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const description = document.getElementById('description').value;

    if (!description) {
        alert('Please enter a description.');
        return;
    }

    // Show the modal for additional questions
    const modal = document.getElementById('additionalQuestionsModal');
    modal.style.display = 'block';
});

// Krishna Sree Guguloth - Toggle logo URL field based on the user's choice
document.querySelectorAll('input[name="logo"]').forEach(radio => {
    radio.addEventListener('change', function() {
        const logoURLField = document.getElementById('logoURL');
        logoURLField.style.display = this.value === 'Yes' ? 'block' : 'none';
    });
});

// Jyotsana R Parkhedkar - Close modal when the user clicks the close button
document.querySelector('.close').addEventListener('click', function() {
    const modal = document.getElementById('additionalQuestionsModal');
    modal.style.display = 'none';
});

// Sathvika Chiti - Handle additional questions and send data to the backend
document.getElementById('submitAdditionalQuestions').addEventListener('click', function() {
    const description = document.getElementById('description').value;

    // Retrieve values with checks to ensure elements are selected
    const logo = document.querySelector('input[name="logo"]:checked');
    const functionality = document.querySelector('input[name="functionality"]:checked');
    const database = document.querySelector('input[name="database"]:checked');

    // Ensure all required fields are selected
    if (!logo || !functionality || !database) {
        alert('Please answer all questions before submitting.');
        return;
    }

    const logoURL = logo.value === 'Yes' ? document.getElementById('logoURL').value : null;
    
    const loadingSpinner = document.getElementById('loading-spinner');
    const generatedCodePre = document.getElementById('generated-code-pre');
    const downloadSQLBtn = document.getElementById('download-sql-btn');

    // Close the modal after collecting the answers
    document.getElementById('additionalQuestionsModal').style.display = 'none';

    // Show the loading spinner
    loadingSpinner.style.display = 'inline-block';
    loadingSpinner.innerHTML = '<div class="spinner"></div>';

    // Send the collected data to the backend
    fetch('/generate-prototype', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            description: description,
            logo: logo.value === 'Yes' ? logoURL : null,
            functionality: functionality.value === 'Yes',
            database: database.value === 'Yes'
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

            // Show the SQL download button if a database schema was requested
            if (database.value === 'Yes') {
                downloadSQLBtn.style.display = 'inline-block';
            } else {
                downloadSQLBtn.style.display = 'none';
            }
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

// Venkata Sylesh Kona - Copy the generated code to clipboard
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

// Joshna Gurram - Run the generated code in a new pop-up window
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

// Shreyash Govind Mungilwar - Toggle dark mode and save preference to local storage
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

// Sai Satwik Bikumandla - Show "Go to Top" button when scrolling
const goToTopBtn = document.getElementById('go-to-top');

window.onscroll = function() {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        goToTopBtn.style.display = 'block'; // Show the button when scrolled down
    } else {
        goToTopBtn.style.display = 'none'; // Hide the button when near the top
    }
};

// Sai Satwik Bikumandla - Scroll to the top when the "Go to Top" button is clicked
goToTopBtn.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' }); // Smooth scrolling to top
});

// Jyotsana R Parkhedkar - Function to download SQL schema if generated
function downloadSQL() {
    window.location.href = '/download-schema';
}
