# LaTeXify

LaTeXify is a simple web application that converts images containing mathematical content (equations, formulas, tables) into compilable LaTeX code using the Google Gemini API.

## Features

*   Upload images (PNG, JPG, etc.)
*   Convert image content to LaTeX code via Google Gemini Pro Vision API.
*   Display the generated LaTeX code.
*   Simple, clean UI inspired by Shadcn design principles (using Tailwind CSS).
*   Copy generated LaTeX code to clipboard.
*   Image preview before uploading.

## Project Structure

```
/latexify
|-- app.py                 # Flask backend logic
|-- requirements.txt       # Python dependencies
|-- .env.example           # Example environment variables file
|-- .env                   # Actual environment variables (needs creation)
|-- README.md              # This file
|-- /templates
|   |-- index.html         # Main HTML page
|-- /static
|   |-- /css
|   |   |-- style.css      # Custom CSS (optional)
|   |-- /js
|   |   |-- script.js      # Frontend JavaScript logic
```

## Setup and Installation

1.  **Clone the repository (or download the files):**
    ```bash
    # If using git
    git clone <repository_url>
    cd latexify
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your Google API Key:**
    *   Obtain an API key from Google AI Studio: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
    *   Rename the `.env.example` file to `.env`.
    *   Open the `.env` file and replace `"YOUR_API_KEY_HERE"` with your actual Google API Key.
        ```.env
        GOOGLE_API_KEY="YOUR_ACTUAL_API_KEY"
        ```

## Running the Application

1.  **Ensure your virtual environment is activated.**

2.  **Run the Flask development server:**
    ```bash
    python app.py
    ```

3.  **Open your web browser** and navigate to `http://127.0.0.1:5000` (or the address provided in the terminal).

## How to Use

1.  Click the "Choose File" button to select an image from your device.
2.  A preview of the selected image will appear.
3.  Click the "Convert to LaTeX" button.
4.  Wait for the conversion process (a loader will be displayed).
5.  The generated LaTeX code will appear in the text area below.
6.  Click the "Copy Code" button to copy the LaTeX to your clipboard.
7.  If an error occurs, an error message will be displayed.

## Notes

*   The quality of the LaTeX conversion depends heavily on the clarity of the input image and the capabilities of the Gemini Pro Vision model.
*   The application uses the Flask development server, which is not suitable for production deployment. For production, consider using a production-grade WSGI server like Gunicorn or uWSGI behind a reverse proxy like Nginx.
*   Error handling is basic. Further improvements could include more specific error messages and retry mechanisms.
*   The prompt sent to the Gemini API is generic. It might need adjustments for specific types of images or desired LaTeX output formats. 