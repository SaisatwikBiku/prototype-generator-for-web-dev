# Getting Started with Web Prototype Generator

The **Web Prototype Generator** is a collaborative project that allows users to generate responsive website prototypes based on client descriptions. It includes features such as HTML/CSS/JavaScript prototype generation, optional SQL schema generation, and API integrations with Gemini and Unsplash.

---

## Features

- **Automated Prototype Generation**: Generates HTML/CSS/JavaScript code based on a descriptive prompt, making it easy to visualize website layouts.
- **Image Integration**: Automatically fetches relevant images from Unsplash based on keywords from the user’s description.
- **Optional Database Schema**: Generates an SQL schema for database design based on the generated HTML structure.
- **Interactive Interface**: Allows users to input a description, answer additional questions about functionality, and preview the generated code.
- **Dark Mode Support**: Offers a dark mode toggle for a better user experience.

---

## Code Contributions and Collaboration

This code is being built simultaneously by all team members. 

Each team member’s contribution is marked within the code using the format:

'{Team Member Name} - Team Member's Contribution'


Whenever a team member makes any changes and pushes the code, they will highlight their part of the contribution with comments. This approach ensures clear attribution and facilitates effective collaboration among all team members.

### Important Note
Some components of this code were generated using ChatGPT-4, specifically to assist with prompt generation and API integrations. These parts are clearly annotated in the code to distinguish them from manually written sections.

---

## Project Structure and Team Contributions

## Codebase Organization

The codebase is organized as follows:

### `app.py` - Main Application Code
The main backend logic for the application, including routes, helper functions, and API configurations.

1. **Krishna Sree Guguloth - Setup and Configuration**
   - Initializes the Flask application.
   - Configures the Gemini API and Unsplash API access keys.
   - Downloads required NLTK resources for processing.

2. **Shreyash Govind Mungilwar - Image Fetching Helper Function**
   - Implements the `fetch_images` function to retrieve relevant images from Unsplash based on keywords extracted from the user’s description.

3. **Sai Satwik Bikumandla - Prototype Generation Helper Function**
   - Writes the `generate_prototype` function, which calls the Gemini API to generate HTML prototypes based on the user description and configuration.
   - Constructs a detailed prompt to guide the API in generating the front-end code with specified requirements.

4. **Jyotsana R Parkhedkar - SQL Schema Generation Helper Function**
   - Adds the `generate_sql_schema` function, which generates an SQL schema based on the HTML structure, supporting any backend requirements.

5. **Joshna Gurram - Main Routes Setup**
   - Creates the `/` route to render the homepage (`index.html`).

6. **Sathvika Chiti - Prototype Generation Route**
   - Builds the `/generate-prototype` route, which processes form data and calls the `generate_prototype` and `generate_sql_schema` functions.
   - Manages data received from the user, including descriptions, logos, functionality requests, and database options.

7. **Venkata Sylesh Kona - SQL Schema Download Route**
   - Implements the `/download-schema` route, which serves the generated SQL schema to users as a downloadable file.

8. **Sai Ram Navuluri - Application Run Configuration**
   - Configures the application to run on port 5005 with debug mode enabled.

---

### `index.html` - Frontend HTML Structure
The main HTML template for the user interface, with contributions from each team member for different sections.

1. **Krishna Sree Guguloth - Favicon and Stylesheet Linking**
   - Sets up the favicon and links the main stylesheet.

2. **Shreyash Govind Mungilwar - Sentinel Element for Intersection Observer**
   - Adds an intersection observer sentinel for handling dynamic content loading.

3. **Sai Satwik Bikumandla - Navigation Bar**
   - Implements the navigation bar with links to different sections of the application.

4. **Sai Ram Navuluri - Prototype Generator Section**
   - Creates the form and input elements for users to describe their prototype needs.

5. **Joshna Gurram - Popup Modal for Additional Questions**
   - Builds the modal that asks users for additional specifications like logo, functionality, and database requirements.

6. **Venkata Sylesh Kona - Generated Code Section**
   - Displays the generated prototype code and includes buttons for copying or running the code.

7. **Shreyash Govind Mungilwar - Project Overview Section**
   - Writes the project overview explaining the purpose and functionality of the tool.

8. **Sai Ram Navuluri - Contact Us Section**
   - Creates a contact list with team member emails for users to reach out.

---

### `styles.css` - Main Stylesheet
Defines the styling for each part of the application, with specific contributions for different components.

1. **Krishna Sree Guguloth - General Styles**
   - Sets up basic styles for body, font, and resets to ensure consistent look across browsers.

2. **Shreyash Govind Mungilwar - Dark Mode Styles**
   - Implements dark mode styling for the body, navigation, and other elements.

3. **Sai Satwik Bikumandla - Navigation Styles**
   - Styles the navigation bar, including spacing, colors, and hover effects.

4. **Jyotsana R Parkhedkar - Highlighted Navigation Styles**
   - Adds styling for highlighted nav items with oval borders and color transitions.

5. **Joshna Gurram - Dark Mode Navigation Link Colors**
   - Specifies color adjustments for links in dark mode.

6. **Venkata Sylesh Kona - Container and Section Styles**
   - Defines the layout and appearance of main container and section elements.

7. **Sathvika Chiti - Sub-section Styles**
   - Styles sub-sections within the main sections for improved UI structure.

8. **Sai Ram Navuluri - Modal Styles**
   - Creates styling for modals, including background overlay, positioning, and form elements.

---

### `script.js` - Frontend Interactivity
JavaScript to handle user interactions, modal visibility, dark mode toggle, and other client-side functionality.

1. **Sai Ram Navuluri - Form Submission and Modal Display**
   - Handles form submission to generate a prototype and shows the modal for additional questions.

2. **Krishna Sree Guguloth - Logo URL Field Toggle**
   - Adds functionality to toggle the visibility of the logo URL input field based on user choice.

3. **Jyotsana R Parkhedkar - Close Modal Functionality**
   - Implements functionality to close the modal when the user clicks the close button.

4. **Sathvika Chiti - Additional Questions and Data Submission**
   - Collects user responses from the modal and sends data to the backend.

5. **Venkata Sylesh Kona - Copy Generated Code**
   - Adds the function to copy generated code to the clipboard for user convenience.

6. **Joshna Gurram - Run Generated Code in a New Window**
   - Opens the generated code in a new browser window for preview.

7. **Shreyash Govind Mungilwar - Dark Mode Toggle**
   - Toggles dark mode and saves the user's theme preference to local storage.

8. **Sai Satwik Bikumandla - Go to Top Button**
   - Handles the display and functionality of the "Go to Top" button.

---

Each team member’s contributions are clearly marked within the codebase to facilitate collaborative development and accountability.


### `templates/index.html`
The main HTML template, which serves as the user interface for the application. Here, team members have divided the HTML sections to manage form inputs, modal interactions, navigation, and content display.

### `static/styles.css`
This file contains all CSS for styling the application. Each team member contributes specific sections for layout, colors, typography, and responsive design.

### `static/script.js`
The JavaScript file handles client-side interactivity, including form submission, dark mode toggling, modals, and other UI interactions. Each function is attributed to a specific team member to keep contributions clear.

---

## Available Scripts

In the project directory, you can run:

### `python app.py`

Runs the app in development mode.\
Open [http://localhost:5005](http://localhost:5005) to view it in the browser.

---

## Dependencies

- **Flask**: Web framework for handling routes and server-side rendering.
- **NLTK**: Used for natural language processing of user descriptions.
- **requests**: Library for handling API calls to Unsplash.
- **google.generativeai**: Library for interacting with the Gemini API for prototype generation.

---

## API Integrations

- **Gemini API**: Used to generate HTML, CSS, and JavaScript code for website prototypes based on user descriptions.
- **Unsplash API**: Fetches relevant images for the prototype based on extracted keywords from user inputs.

---

## Learn More

To learn more about Flask, check out the [Flask documentation](https://flask.palletsprojects.com/).

To learn about the APIs used, visit:
- [Gemini API Documentation](https://developers.google.com/generative-ai)
- [Unsplash API Documentation](https://unsplash.com/documentation)

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

Special thanks to OpenAI's ChatGPT-4 for assisting with prompt creation and certain API integration components. These AI-generated components are noted in the codebase for transparency.

---

