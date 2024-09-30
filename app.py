from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

app = Flask(__name__)

# paste Gemini API here..
genai.configure(api_key="AIzaSyCZbyF-hRHTxcoiCpKMAMpqZSTsgR68BDo")  

# Paste Unsplash API Access Key here.
UNSPLASH_ACCESS_KEY = 'DLuEnJUi2bDtoz2AD3GzcjH382l8_3VwPX75lMXrsT0'

# Download NLTK resources if not already downloaded
nltk.download('stopwords')
nltk.download('punkt')

# Function to extract keywords from description
def extract_keywords(description):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(description)
    keywords = [word for word in words if word.lower() not in stop_words and word.isalpha()]
    return ", ".join(keywords[:5])  # Select top 5 keywords to keep it relevant

# Function to fetch image URLs based on keywords in the description
def fetch_images(keywords, num_images=3):
    url = f"https://api.unsplash.com/search/photos"
    params = {
        "query": keywords,
        "per_page": num_images,
        "client_id": UNSPLASH_ACCESS_KEY,
        "orientation": "landscape"  # Ensures a consistent layout for landing pages
    }
    
    response = requests.get(url, params=params)
    image_urls = []

    if response.status_code == 200:
        data = response.json()
        for result in data['results']:
            # Fetch regular-sized images that fit in boxed layout
            image_urls.append(result['urls']['regular'])
    
    return image_urls

# Function to generate web prototype using Gemini API
def generate_prototype(description):
    # Extract relevant keywords from the user's description
    keywords = extract_keywords(description)
    
    # Fetch relevant images based on the extracted keywords
    image_urls = fetch_images(keywords)
    
    # Enhance the prompt to include the actual image URLs and define dimensions
    images_html = "".join([f'<img src="{url}" alt="{keywords}" style="width:100%; height:auto;">' for url in image_urls])
    
    improved_prompt = f"""
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

    The response should only contain HTML, CSS, and JavaScript code, and no explanations or additional text.
    """

    generation_config = {
        "temperature": 1.6,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Generate the web prototype based on the description using the Gemini API
    chat_session = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    ).start_chat(
        history=[
            {"role": "user", "parts": [improved_prompt]}
        ]
    )
    
    response = chat_session.send_message("Generate the web prototype")
    return response.text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-prototype', methods=['POST'])
def generate_prototype_route():
    description = request.form.get('description')

    # Generate the prototype using the description
    try:
        generated_code = generate_prototype(description)
        return jsonify({"generated_code": generated_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
