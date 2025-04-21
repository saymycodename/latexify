import os
import io
import re # Import regex module
import logging # Import logging module
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Configure basic logging
logging.basicConfig(level=logging.INFO)

# Configure the Flask app
app = Flask(__name__)
# Set a secret key for session management (optional but recommended)
app.secret_key = os.urandom(24)
# Configure Google Generative AI
# It is strongly recommended to store your API key in an environment variable
# Ensure you have a .env file with GOOGLE_API_KEY="YOUR_API_KEY"
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please create a .env file.")

genai.configure(api_key=api_key)

# Initialize the Gemini Pro Vision model
# This model is capable of understanding both text and images
# Using gemini-pro-vision as it's suitable for image inputs
model = genai.GenerativeModel('gemini-2.0-flash-lite')

# Define the detailed system prompt
# Use r""" for raw string to treat backslashes literally
latex_system_prompt = r"""
You are an expert technical writer and LaTeX specialist. Your task is to take the provided text and convert it into a clean, professional LaTeX document. The final code should be ready-to-compile, easy to read, and make expert use of LaTeX features for academic, business, or technical audiences.

Instructions:
Analyze the Input Identify and correctly map structural elements (titles, headings, subheadings, lists, tables, paragraphs, emphasis, and mathematical content).Recognize any context, such as business, academic, or scientific tone, and adapt formatting as is.Build Document Structure Start with a standard, clean LaTeX preamble including a suitable \documentclass (e.g., article or report), and load any required packages (e.g., geometry, amsmath, booktabs, hyperref, enumitem, etc.).Ensure margins are generous and content is well-spaced for readability.Add metadata (title, author, date) if available; otherwise, leave these blank or add placeholders.Convert Content Map top-level titles to \title and \maketitle.Render headings and subheadings using the correct sectioning commands (\section, \subsection, etc.) or \section* for untitled sections.Convert bullet lists, numbered lists, and tables using the appropriate environments.Render mathematical expressions in proper math mode ($...$ or $$...$$).Bold or italicize text as needed using \textbf{} or \emph{}.For tables, use booktabs for clean lines and adjust column widths for readability.Add contextual notes or comments in the LaTeX code where formatting choices are non-obvious.Polish and ReviewCheck for code readability (indentation, spacing, comments).Avoid unnecessary LaTeX complexity; keep it maintainable.Only use necessary packages; avoid bloat.If the text contains placeholders (e.g., “add your idea here”), style them in the output as comments.Use inline comments to explain any non-trivial conversions.Best Practices and Tips:For business/tech contexts: use \usepackage{array} for versatile tables and geometry for better layout.For scientific/math: add amsmath and use proper math environments.Hyperlink any URLs using \href from hyperref.Use enumitem for advanced list formatting, if needed.For long tables or wide content, consider the tabularx package for balanced widths.
"""

@app.route('/')
def index():
    """
    Renders the main page of the application.
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    """
    Handles image upload, sends it to Gemini API for LaTeX conversion,
    and returns the result.
    """
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({"error": "No image selected"}), 400

    if file:
        try:
            # Read the image file
            img_bytes = file.read()
            img = Image.open(io.BytesIO(img_bytes))

            # Use the detailed system prompt
            prompt_parts = [latex_system_prompt, img]

            # Send the image and prompt to the Gemini API
            app.logger.info("Sending request to Gemini API...")
            response = model.generate_content(prompt_parts, stream=True)
            response.resolve() # Wait for the streaming response to complete

            # Log the raw response for debugging
            try:
                raw_text = response.text
                app.logger.info(f"Raw Gemini API response text: {raw_text}")
            except Exception as log_err:
                # Handle cases where accessing response.text might fail
                # (e.g., blocked content, other errors)
                app.logger.warning(f"Could not access response.text: {log_err}")
                # Check for prompt feedback which might indicate blocking
                if response.prompt_feedback and response.prompt_feedback.block_reason:
                     block_reason = response.prompt_feedback.block_reason.name
                     app.logger.error(f"Gemini API request blocked due to: {block_reason}")
                     return jsonify({"error": f"The request was blocked by the safety filter ({block_reason}). Please try a different image."}), 400
                raw_text = "" # Default to empty if text cannot be retrieved

            # Enhanced extraction logic
            latex_code = ""
            if raw_text:
                # Attempt to find code within ```latex ... ``` or ``` ... ```
                match = re.search(r"```(?:latex)?\n?(.*?)\n?```", raw_text, re.DOTALL | re.IGNORECASE)
                if match:
                    latex_code = match.group(1).strip()
                    app.logger.info("Extracted LaTeX from markdown block.")
                else:
                    # If no markdown block found, assume the whole text is the code
                    # (as requested in the updated prompt)
                    latex_code = raw_text.strip()
                    app.logger.info("No markdown block found, using raw response text.")
            else:
                # Handle cases where the response text was empty or inaccessible
                app.logger.warning("Gemini API response text is empty or was inaccessible.")

            # Check if we successfully got some LaTeX code
            if latex_code:
                 app.logger.info(f"Cleaned LaTeX code length: {len(latex_code)}")
                 return jsonify({"latex": latex_code})
            else:
                 # If still no code after extraction attempts
                 app.logger.error("Failed to extract LaTeX code from the response.")
                 return jsonify({"error": "Failed to extract LaTeX code from the response. The model might not have generated the expected output."}), 500

        # Handle specific API errors like blocked prompts
        except genai.types.generation_types.BlockedPromptException as e:
             app.logger.error(f"Gemini API request explicitly blocked: {e}")
             # Extract block reason if possible
             reason = "Unknown" # Default reason
             if e.__cause__ and hasattr(e.__cause__, 'prompt_feedback') and e.__cause__.prompt_feedback:
                 reason = e.__cause__.prompt_feedback.block_reason.name
             return jsonify({"error": f"The request was blocked by the safety filter ({reason}). Please try a different image."}), 400
        # Handle other potential exceptions during API call or image processing
        except Exception as e:
            # Log the exception for debugging
            app.logger.error(f"Error processing image or calling Gemini API: {e}", exc_info=True) # Include traceback
            return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    # Fallback if 'file' is somehow false after the initial checks
    return jsonify({"error": "File processing failed unexpectedly"}), 500

# Run the Flask app
if __name__ == '__main__':
    # Use debug=True for development environment, allows auto-reload
    # Set debug=False for production
    app.run(debug=True) 