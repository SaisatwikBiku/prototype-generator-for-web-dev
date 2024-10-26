from flask import Flask, render_template, request, jsonify, send_file
import google.generativeai as genai
import requests
import nltk
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK resources if not already downloaded
nltk.download('stopwords')
nltk.download('punkt')

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="AIzaSyCZbyF-hRHTxcoiCpKMAMpqZSTsgR68BDo")

# Unsplash API Access Key
UNSPLASH_ACCESS_KEY = 'DLuEnJUi2bDtoz2AD3GzcjH382l8_3VwPX75lMXrsT0'

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

# Helper function to generate prototype with Gemini API
def generate_prototype(description, logo_url=None, functionality=False, multiple_pages=False):
    image_urls = fetch_images(description)
    images_html = "".join([f'<img src="{url}" alt="Image related to {description}" style="width:100%; height:auto;">' for url in image_urls])

    # Build the detailed prompt for front-end prototype generation
    prompt = f"""
    You are an expert web developer assistant. Your task is to generate fully executable HTML, CSS, and JavaScript code based on the following description: {description}.

    The output must include:
    1. A complete and structured HTML document with sections such as <head>, <body>, and semantic tags like <header>, <section>, <footer>.
    2. Responsive design that works well on both mobile and desktop screens. Use media queries to handle responsiveness.
    3. Use modern design principles, such as Flexbox or CSS Grid, for layout management. Ensure the page follows best practices for a clean and user-friendly interface.
    4. Use the following actual images in the appropriate sections of the prototype (with relevant dimensions for boxed layout):
    {images_html}
    5. Generate internal CSS styles, avoiding external dependencies like Bootstrap, and use a modern, clean color scheme. Make sure the colors are complementary to the theme described.
    6. Include any required JavaScript functionality for interactive elements (e.g., buttons, forms, navigation bars). Write simple, clean JavaScript functions for interactivity, such as form handling or toggling content visibility.
    7. The generated page should have a clear navigation bar at the top, sections based on the content provided, and a footer. Ensure the page has proper spacing, margins, and padding for a balanced look.
    8. Ensure good typography with appropriate font sizes, line heights, and weights. Use a Google font like 'Roboto' or 'Open Sans' for a modern look.
    """

    if logo_url:
        prompt += f"\nInclude the following logo at the top of the page: {logo_url}. Add the logo at appropriate area of the page and keep it properly formatted along with the overall webpage"

    if functionality:
        prompt += "\nEnsure the page is fully functional with necessary JavaScript interactivity. Use Pop-Ups. Once the page is opened, there should be a Pop-Up which welcomes the user to the webpage. Place interactive elements and functional buttons with pop-ups relevant to the page content."

    prompt += """
    Give high quality code by following web development principles with modern web interfaces and structured UI components. The prototype should have functionalities implemented using JavaScript. Emphasize equally on User Interface and Functionality.
    The response should only contain HTML code with CSS, and JavaScript embedded in it. No explanations or additional text are required. Output should be index.html file. The response should begin with <!DOCTYPE html> and must end with </html>.
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

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/download-schema')
def download_schema():
    if os.path.exists('schema.sql'):
        return send_file('schema.sql', as_attachment=True)
    else:
        return jsonify({"error": "SQL schema not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5005)  # Change port if required
