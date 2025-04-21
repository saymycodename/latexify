# LaTeXify

LaTeXify is a simple web application that converts images containing mathematical content (equations, formulas, tables) into compilable LaTeX code.

## Features

*   Upload images (PNG, JPG, etc.)
*   Convert image content to LaTeX code.
*   Display the generated LaTeX code.
*   Simple, clean UI.
*   Copy generated LaTeX code to clipboard.
*   Image preview before uploading.

## Project Structure

```
/latexify
|-- app.py                 # Flask backend logic
|-- requirements.txt       # Python dependencies
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

## How to Use

1.  Click the "Choose File" button to select an image from your device.
2.  A preview of the selected image will appear.
3.  Click the "Convert to LaTeX" button.
4.  Wait for the conversion process (a loader will be displayed).
5.  The generated LaTeX code will appear in the text area below.
6.  Click the "Copy Code" button to copy the LaTeX to your clipboard.
7.  If an error occurs, an error message will be displayed.

## Notes

*   The quality of the LaTeX conversion depends heavily on the clarity of the input image.
