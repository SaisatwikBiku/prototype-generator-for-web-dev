# app.py - Main application file for the Web Prototype Generator

'''
This code is being built simultaneously by all team members.

The contribution is clearly mentioned in the following Format: '{Team Member Name} - Team Member's Contribution'

Whenever a Team member make any change pushes the code, they will highlight their part of the contribution with comments.

This source code has few components created using ChatGPT-4o and they are clearly mentioned.
'''

from flask import Flask, render_template, request, jsonify, send_file
import google.generativeai as genai
import requests
import nltk
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Sathvika Chitti: Setup and Configuration

# Download NLTK resources if not already downloaded
nltk.download('stopwords')
nltk.download('punkt')

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyCZbyF-hRHTxcoiCpKMAMpqZSTsgR68BDo")

# Unsplash API Access Key
UNSPLASH_ACCESS_KEY = 'DLuEnJUi2bDtoz2AD3GzcjH382l8_3VwPX75lMXrsT0'

# Kona Venkata Sylesh: Image Fetching Helper Function

# Helper function to fetch images from Unsplash
def fetch_images(description, num_images=3):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(description)
    keywords = [word for word in words if word.lower() not in stop_words and word.isalpha()]
    search_query = ", ".join(keywords[:5])

    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": search_query,
        "per_page": num_images,
        "client_id": UNSPLASH_ACCESS_KEY,
        "orientation": "landscape"
    }
    response = requests.get(url, params=params)
    image_urls = []

    if response.status_code == 200:
        data = response.json()
        for result in data['results']:
            image_urls.append(result['urls']['regular'])

    return image_urls

# Sai Satwik Bikumandla: Prototype Generation Helper Function

# Helper function to generate prototype with Gemini API
def generate_prototype(description, logo_url=None, functionality=False, multiple_pages=False):
    image_urls = fetch_images(description)
    images_html = "".join([f'<img src="{url}" alt="Image related to {description}" style="width:100%; height:auto;">' for url in image_urls])

    # Build the detailed prompt for front-end prototype generation - Used GenAI's Assistance to improve this prompt- First written a rough prompt then gave to ChatGPT-4o and refined the old prompt
    prompt = f"""
    As an expert in professional web development, create a comprehensive, high-fidelity HTML, CSS, and JavaScript codebase that meets the following project description: {description}.

    The code should adhere to the following requirements:
    1. A well-structured HTML5 document starting with <!DOCTYPE html> and including all essential sections like <head>, <body>, semantic tags (<header>, <main>, <section>, <footer>), with thoughtful use of <div> and <span> elements as needed for layout precision.
    2. A highly responsive design with finely-tuned media queries that seamlessly adapts to mobile, tablet, and desktop screens, ensuring all elements scale gracefully.
    3. Utilize CSS Grid or Flexbox exclusively for a clean, modern layout, with each section logically organized and aligned. Aim for balanced spacing and alignment that achieves a polished, pixel-perfect look.
    4. Placement and formatting of the following images within the layout, styled with appropriate dimensions, padding, and alignment to maintain aesthetic balance: {images_html}.
    5. Embedded, self-contained CSS styles that avoid external libraries (e.g., Bootstrap). Select a refined, modern color palette that enhances readability and supports a cohesive design theme.
    6. Implement JavaScript for interactivity in a clean, modular way. Focus on essential features like form handling, content toggling, button actions, and a smooth navigation experience.
    7. A minimalist, accessible navigation bar positioned at the top of the layout, and a footer with relevant content at the bottom. The navigation bar should include hover and active states to indicate current page sections.
    8. Consistent, visually appealing typography using a Google font like 'Roboto' or 'Open Sans', with deliberate choices in font size, weight, and spacing to enhance readability and professionalism.
    9. Attention to detail in UI consistency, ensuring all sizes, colors, and spacing choices contribute to a unified and professional design. Maintain uniform margins, padding, and alignment for all elements.
    10. The output should be a complete and standalone 'index.html' file, with embedded CSS and JavaScript, containing no comments or additional text, ready for immediate use. There should not be any other text other than the executable code.
    """

    if logo_url:
        prompt += f"""
        Incorporate the provided logo prominently in the layout following modern design practices: {logo_url}. 
        - Position the logo in an optimal location, such as the top-left corner, making it clear yet balanced within the header.
        - Adjust the logo dimensions to ensure clarity and proportion across screen sizes, using padding to maintain visual separation from other elements.
        - Style the logo in harmony with the chosen theme, allowing it to naturally complement the page’s color scheme.
        """

    if functionality:
        prompt += """
        Integrate JavaScript-based interactivity to enhance the user experience. Required interactive features include:
        - A greeting pop-up upon page load, with dismissible functionality, styled in alignment with the page theme.
        - Responsive interactive elements, such as buttons and forms, that trigger modals or alerts as appropriate to the page content.
        - Menu functionality for the navigation bar, enabling smooth scrolling and navigation among sections.
        """

    prompt += """
    Ensure the HTML, CSS, and JavaScript code is clean, optimized, and adheres to best practices in modern web development.
    - Focus on both User Interface (UI) and User Experience (UX), prioritizing ease of use and aesthetics.
    - Output should be a complete HTML document, starting with <!DOCTYPE html> and ending with </html>, formatted to provide a pixel-perfect, professional finish.
    """


    generation_config = {
        "temperature": 1.6,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    chat_session = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    ).start_chat(
        history=[
            {"role": "user", "parts": [prompt]}
        ]
    )

    response = chat_session.send_message("Generate the web prototype")
    return response.text

# Jyotsana Parkhedkar: SQL Schema Generation Helper Function

# Helper function to generate SQL schema based on HTML code
def generate_sql_schema(html_code):
    prompt = f"""
    You are a database design assistant. Based on the following HTML code for a web page, generate an SQL schema that includes tables, primary keys, and necessary fields to support the functionality of this page.

    HTML Code:
    {html_code}

    Only output SQL code. Do not include explanations.
    """

    generation_config = {
        "temperature": 1.2,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    chat_session = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    ).start_chat(
        history=[
            {"role": "user", "parts": [prompt]}
        ]
    )

    response = chat_session.send_message("Generate SQL schema")
    return response.text

# Sai Ram Navuluri: Main Routes Setup

@app.route('/')
def index():
    return render_template('index.html')

# Sai Satwik Bikumandla: Prototype Generation Route

@app.route('/generate-prototype', methods=['POST'])
def generate_prototype_route():
    data = request.get_json()

    description = data.get('description')
    logo_url = data.get('logo')
    functionality = data.get('functionality', False)
    database = data.get('database', False)
    multiple_pages = data.get('multiplePages', False)

    try:
        # First API Call - Generate the front-end code
        generated_code = generate_prototype(description, logo_url, functionality, multiple_pages)

        sql_schema = None
        # Second API Call - Generate SQL schema if requested
        if database:
            sql_schema = generate_sql_schema(generated_code)
            with open('schema.sql', 'w') as file:
                file.write(sql_schema)

        return jsonify({"generated_code": generated_code, "sql_schema": database})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Shreyash Govind Mungilwar: SQL Schema Download Route

@app.route('/download-schema')
def download_schema():
    if os.path.exists('schema.sql'):
        return send_file('schema.sql', as_attachment=True)
    else:
        return jsonify({"error": "SQL schema not found"}), 404

# Krishna Sree: Application Run Configuration

if __name__ == '__main__':
    app.run(debug=True, port=5005)  # Change port if required
