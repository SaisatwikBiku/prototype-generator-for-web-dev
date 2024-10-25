// Function to show/hide custom input fields based on dropdown selection
function showCustomInput(dropdown, customInputId) {
    const customInputField = document.getElementById(customInputId);
    if (dropdown.value === 'custom') {
        customInputField.style.display = 'block';
    } else {
        customInputField.style.display = 'none';
    }
}

// Form submission to generate prototype
document.getElementById('prototypeForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const description = document.getElementById('description').value;
    const websiteType = document.getElementById('website-type').value;
    const websiteTypeCustom = document.getElementById('website-type-custom').value;
    const colors = document.getElementById('colors').value;
    const colorsCustom = document.getElementById('colors-custom').value;
    const sections = document.getElementById('sections').value;
    const sectionsCustom = document.getElementById('sections-custom').value;
    const features = document.getElementById('features').value;
    const featuresCustom = document.getElementById('features-custom').value;
    const logoUrl = document.getElementById('logo-url').value;
    const loadingSpinner = document.getElementById('loading-spinner');
    const generatedCodePre = document.getElementById('generated-code-pre');

    // Construct the full prompt using either custom inputs or selected options
    const finalWebsiteType = websiteType === 'custom' ? websiteTypeCustom : websiteType;
    const finalColors = colors === 'custom' ? colorsCustom : colors;
    const finalSections = sections === 'custom' ? sectionsCustom : sections;
    const finalFeatures = features === 'custom' ? featuresCustom : features;

    if (!description || !finalWebsiteType || !finalColors || !finalSections || !finalFeatures) {
        alert('Please complete all the required fields.');
        return;
    }

    // Show the loading spinner
    loadingSpinner.style.display = 'inline-block';
    loadingSpinner.innerHTML = '<div class="spinner"></div>';

    // Send the form data to the backend for generating the prototype
    fetch('/generate-prototype', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'description': description,
            'website_type': finalWebsiteType,
            'colors': finalColors,
            'sections': finalSections,
            'features': finalFeatures,
            'logo_url': logoUrl
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
