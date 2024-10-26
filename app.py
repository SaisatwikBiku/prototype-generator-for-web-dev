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

    # Build the detailed prompt for front-end prototype generation - Used GenAI to improve this prompt
    prompt = f"""
    As a skilled web development assistant, your role is to generate fully executable, high-quality HTML, CSS, and JavaScript code that aligns with the following description: {description}.

    Your output should include:
    1. A well-structured HTML5 document with properly organized sections, including <head>, <body>, and semantic tags such as <header>, <main>, <section>, and <footer>.
    2. A fully responsive design that adapts seamlessly across mobile and desktop screens. Use media queries to ensure the layout remains user-friendly and functional on all device sizes.
    3. Modern layout techniques such as Flexbox or CSS Grid for clean, efficient layout management. Follow best practices to create an intuitive, easy-to-navigate user interface.
    4. Incorporate the following images in the specified sections of the layout, ensuring correct dimensions and positioning for a polished, boxed design:
       {images_html}
    5. Utilize internal CSS styles to keep the code self-contained, avoiding external libraries like Bootstrap. Apply a modern, clean color scheme that complements the described theme.
    6. Embed JavaScript for interactivity, implementing only necessary and relevant functions (e.g., for form handling, toggling content visibility, or button actions). Ensure JavaScript code is clean and minimally dependent on external functions.
    7. Include a clear navigation bar at the top, structured sections based on content requirements, and a footer. Use well-balanced spacing, margins, and padding to maintain a visually harmonious layout.
    8. Maintain appealing typography with well-sized fonts, balanced line spacing, and weights that enhance readability. Include a modern Google font like 'Roboto' or 'Open Sans' to give the design a professional finish.
    """

    if logo_url:
        prompt += f"\nPlace the following logo prominently within the layout, following modern web design standards: {logo_url}. \n- Position the logo in an intuitive and visually balanced location, such as the top-left corner of the header, ensuring it aligns with the overall page structure. \n- Apply appropriate formatting to integrate the logo seamlessly with the design, including responsive sizing and padding to maintain clarity and proportion on various screen sizes.\n - Ensure the logo is styled consistently with the theme and layout, complementing the page's color scheme and aesthetic."

    if functionality:
        prompt += "\nEnsure the webpage includes all necessary JavaScript for interactivity, creating a dynamic user experience. Implement the following interactive features:\n - A welcome pop-up that appears when the page loads, greeting the user and enhancing engagement. This pop-up should be dismissible and styled to match the page theme. \n- Add interactive elements, such as buttons and forms, that use pop-up modals or alerts relevant to the page content. These elements should be intuitive and provide feedback or additional information when interacted with. \n - Design pop-ups to appear contextually, ensuring they enhance navigation and user experience without overwhelming the layout. "

    prompt += """
    Provide high-quality, professional code that adheres to modern web development standards, using well-structured UI components and best practices for clean, maintainable design.
    - Ensure the prototype is fully functional, with JavaScript handling all interactive elements.
    - Balance the focus on both User Interface (UI) and User Experience (UX), creating an interface that is visually appealing and intuitive to navigate.
    - The response should consist solely of an HTML document with embedded CSS and JavaScript. No additional explanations or comments are needed.
    - The output should be a complete and ready-to-run 'index.html' file, starting with <!DOCTYPE html> and ending with </html>.
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
