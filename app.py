from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import requests

# Initialize the Flask app
app = Flask(__name__)

# API keys
GENAI_API_KEY = 'AIzaSyBlz1KHvma3-tfMXXemw9rYLsF-i4-EwKw'
UNSPLASH_ACCESS_KEY = 'DLuEnJUi2bDtoz2AD3GzcjH382l8_3VwPX75lMXrsT0'

# Configure the Gemini API
genai.configure(api_key=GENAI_API_KEY)

# Function to fetch image URLs based on user-provided image categories from Unsplash API
def fetch_images_from_categories(image_categories, num_images=3):
    image_urls = set()  # Use a set to ensure unique image URLs
    for category in image_categories.split(','):
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            params={
                "query": category.strip(),
                "per_page": num_images,
                "client_id": UNSPLASH_ACCESS_KEY,
                "orientation": "landscape"
            }
        )
        if response.status_code == 200:
            data = response.json()
            for result in data.get('results', []):
                image_urls.add(result['urls']['regular'])
                
        # Stop once we have enough unique images
        if len(image_urls) >= num_images:
            break
    return list(image_urls)[:num_images]

# Function to generate web prototype using Gemini API with improved prompt and user-provided image categories
def generate_prototype(description, website_type, colors, sections, features, logo_url, image_categories):
    try:
        # Fetch relevant images based on user-provided categories
        image_urls = fetch_images_from_categories(image_categories)
        image_html_tags = "".join(
            [f'<img src="{url}" alt="{category.strip()}" class="responsive-img" />' for url, category in zip(image_urls, image_categories.split(','))]
        )

        # Improved structured prompt for Gemini API
        structured_prompt = f"""
        You are a professional web developer assistant. Generate fully executable HTML, CSS, and JavaScript code based on these details:

        1. **Project Requirements**:
           - Website type: {website_type}
           - Color theme: {colors}
           - Sections: {sections}
           - Interactive features: {features}
           - Client description: {description}
           - Logo URL (if provided): {logo_url or "None"}

        2. **Image Integration**:
           - Use these images in the design, positioned appropriately and sized responsively:
           {image_html_tags}

        3. **Output Specifications**:
           - HTML structure with appropriate semantic tags (<header>, <main>, <section>, <footer>).
           - Internal CSS for a cohesive, modern look. Style images responsively.
           - Simple JavaScript for interactivity, such as form handling or button functionality.
           - Ensure responsive design for both mobile and desktop.
        
        **Output**: Return only a full HTML file `index.html` with embedded CSS and JavaScript. Avoid additional explanations or symbols.
        """

        # Set configuration for the Gemini API generation
        generation_config = {
            "temperature": 1.3,
            "top_p": 0.9,
            "top_k": 50,
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
    image_categories = request.form.get('image_categories')  # Added field for image category selection

    # Generate the prototype using the form responses
    try:
        generated_code = generate_prototype(description, website_type, colors, sections, features, logo_url, image_categories)
        return jsonify({"generated_code": generated_code})
    except Exception as e:
        return jsonify({"error": f"Error in /generate-prototype: {e}"}), 500

if __name__ == '__main__':
    # Set the port dynamically with fallback to 5002
    app.run(debug=True, port=5002)
