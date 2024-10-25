from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Initialize the Flask app
app = Flask(__name__)

# API keys (directly defined)
GENAI_API_KEY = 'AIzaSyBlz1KHvma3-tfMXXemw9rYLsF-i4-EwKw'
UNSPLASH_ACCESS_KEY = 'DLuEnJUi2bDtoz2AD3GzcjH382l8_3VwPX75lMXrsT0'

genai.configure(api_key=GENAI_API_KEY)

# Download NLTK resources if not already downloaded
nltk.download('stopwords')
nltk.download('punkt')

# Function to extract keywords from description
def extract_keywords(description):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(description)
    keywords = [word for word in words if word.lower() not in stop_words and word.isalpha()]
    return ", ".join(keywords[:5])  # Select top 5 keywords to keep it relevant

# Function to fetch image URLs based on keywords from Unsplash API
def fetch_images(keywords, num_images=3):
    if not keywords or not UNSPLASH_ACCESS_KEY:
        return []  # Return an empty list if there are no keywords or API key
    
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": keywords,
        "per_page": num_images,
        "client_id": UNSPLASH_ACCESS_KEY,
        "orientation": "landscape"
    }
    
    response = requests.get(url, params=params)
    image_urls = []

    if response.status_code == 200:
        data = response.json()
        if data.get('results'):
            image_urls = [result['urls']['regular'] for result in data['results']]
    return image_urls

# Function to generate web prototype using Gemini API, including form responses in the prompt
def generate_prototype(description, website_type, colors, sections, features, logo_url, image_keywords):
    try:
        # Use provided image_keywords if available, otherwise extract from description
        keywords = extract_keywords(description) if not image_keywords else image_keywords

        # Fetch relevant images from Unsplash
        image_urls = fetch_images(keywords)

        # Place the fetched Unsplash URLs directly into the structured prompt
        image_urls_text = ", ".join(image_urls) if image_urls else "No images found"

        # Generate a structured prompt for the Gemini API
        structured_prompt = f"""
        You are an expert web developer assistant. Your task is to generate fully executable HTML, CSS, and JavaScript code based on the following requirements:
        
        - Website type: {website_type}
        - Colors: {colors}
        - Sections: {sections}
        - Features: {features}
        - Logo URL: {logo_url if logo_url else "No logo provided"}
        - Description of the website: {description}

        The output must include:
        1. A complete and structured HTML document with sections such as <head>, <body>, and semantic tags like <header>, <section>, <footer>.
        2. Responsive design that works well on both mobile and desktop screens. Use media queries to handle responsiveness.
        3. Use modern design principles, such as Flexbox or CSS Grid, for layout management. Ensure the page follows best practices for a clean and user-friendly interface.
        4. Use the following actual images (Unsplash image URLs): {image_urls_text}
        5. Generate internal CSS styles, avoiding external dependencies like Bootstrap, and use a modern, clean color scheme. Make sure the colors are complementary to the theme described.
        6. Include any required JavaScript functionality for interactive elements (e.g., buttons, forms, navigation bars). Write simple, clean JavaScript functions for interactivity, such as form handling or toggling content visibility.
        7. The generated page should have a clear navigation bar at the top, sections based on the content provided, and a footer. Ensure the page has proper spacing, margins, and padding for a balanced look.
        8. Ensure good typography with appropriate font sizes, line heights, and weights. Use a Google font like 'Roboto' or 'Open Sans' for a modern look.

        The response should only contain HTML code with CSS, and JavaScript embedded in it. No explanations or additional text are required. Output should be an index.html file.
        """

        # Set configuration for the Gemini API generation
        generation_config = {
            "temperature": 1.6,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        # Generate the web prototype using Gemini API
        chat_session = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        ).start_chat(
            history=[
                {"role": "user", "parts": [structured_prompt]}
            ]
        )
        
        response = chat_session.send_message("Generate the web prototype")
        return response.text

    except Exception as e:
        return f"Error generating prototype: {e}"

# Route for rendering the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling the prototype generation
@app.route('/generate-prototype', methods=['POST'])
def generate_prototype_route():
    description = request.form.get('description')
    website_type = request.form.get('website_type')
    colors = request.form.get('colors')
    sections = request.form.get('sections')
    features = request.form.get('features')
    logo_url = request.form.get('logo_url')
    image_keywords = request.form.get('image_keywords')  # Added field for image keywords

    # Generate the prototype using the form responses
    try:
        generated_code = generate_prototype(description, website_type, colors, sections, features, logo_url, image_keywords)
        return jsonify({"generated_code": generated_code})
    except Exception as e:
        return jsonify({"error": f"Error in /generate-prototype: {e}"}), 500

if __name__ == '__main__':
    # Set the port dynamically with fallback to 5002
    app.run(debug=True, port=5002)
