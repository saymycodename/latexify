document.addEventListener('DOMContentLoaded', () => {
    // Get references to DOM elements
    const uploadForm = document.getElementById('uploadForm');
    const imageInput = document.getElementById('imageInput');
    const dropZone = document.getElementById('dropZone'); // Drag and drop zone
    const imagePreviewContainer = document.getElementById('imagePreviewContainer'); // Preview container
    const imagePreview = document.getElementById('imagePreview');
    const submitButton = document.getElementById('submitButton');
    const buttonText = document.getElementById('buttonText'); // Span for button text
    const loader = document.getElementById('loader'); // Loader element inside button
    const resultArea = document.getElementById('resultArea');
    const latexResult = document.getElementById('latexResult');
    const errorArea = document.getElementById('errorArea');
    const errorMessage = document.getElementById('errorMessage').querySelector('span'); // Get the span inside errorMessage
    const copyButton = document.getElementById('copyButton');

    let currentFile = null; // Variable to hold the selected file

    // --- Helper Functions --- 

    const showLoading = () => {
        buttonText.textContent = 'Converting...'; // Change text
        loader.style.display = 'inline-block'; // Show loader next to text
        submitButton.disabled = true;
        resultArea.classList.add('hidden');
        resultArea.classList.remove('show');
        errorArea.classList.add('hidden');
    };

    const hideLoading = () => {
        buttonText.textContent = 'LaTeXify'; // Reset text
        loader.style.display = 'none'; // Hide loader
        submitButton.disabled = false;
    };

    const showError = (message) => {
        // Update the span inside the error message p element
        errorMessage.textContent = message;
        errorArea.classList.remove('hidden');
        resultArea.classList.add('hidden'); 
        resultArea.classList.remove('show');
    };

    const showResult = (latexCode) => {
        latexResult.value = latexCode;
        resultArea.classList.remove('hidden');
        // Add the show class to trigger the animation
        setTimeout(() => {
            resultArea.classList.add('show');
        }, 10); // Small delay to ensure the transition works
        errorArea.classList.add('hidden'); 
    };

    // Function to handle file selection (from input or drop)
    const handleFileSelect = (file) => {
        if (file && file.type.startsWith('image/')) {
            currentFile = file; // Store the file
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                imagePreview.style.display = 'block';
                imagePreviewContainer.classList.remove('hidden');
            }
            reader.readAsDataURL(file);
            // Reset state
            resultArea.classList.add('hidden');
            resultArea.classList.remove('show');
            errorArea.classList.add('hidden');
            latexResult.value = '';
        } else {
            showError('Please select a valid image file.');
            currentFile = null;
            imagePreview.style.display = 'none';
            imagePreviewContainer.classList.add('hidden');
        }
    };

    // --- Event Listeners --- 

    // Trigger hidden file input click when drop zone is clicked
    dropZone.addEventListener('click', () => {
        imageInput.click();
    });

    // Handle file selection via file input
    imageInput.addEventListener('change', (event) => {
        if (event.target.files && event.target.files[0]) {
            handleFileSelect(event.target.files[0]);
        }
    });

    // Drag and Drop Event Listeners
    dropZone.addEventListener('dragenter', (event) => {
        event.preventDefault();
        event.stopPropagation();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragover', (event) => {
        event.preventDefault();
        event.stopPropagation();
        dropZone.classList.add('drag-over'); // Keep highlighted while over
    });

    dropZone.addEventListener('dragleave', (event) => {
        event.preventDefault();
        event.stopPropagation();
        // Only remove class if leaving the zone itself, not its children
        if (event.relatedTarget !== null && !dropZone.contains(event.relatedTarget)) {
             dropZone.classList.remove('drag-over');
        }
    });

    dropZone.addEventListener('drop', (event) => {
        event.preventDefault();
        event.stopPropagation();
        dropZone.classList.remove('drag-over');

        if (event.dataTransfer.files && event.dataTransfer.files[0]) {
            // Assign the dropped file to the input element's files list
            imageInput.files = event.dataTransfer.files;
            // Handle the file selection
            handleFileSelect(event.dataTransfer.files[0]);
        } else {
             showError('Could not process the dropped file.');
        }
    });

    // Handle form submission
    uploadForm.addEventListener('submit', async (event) => {
        event.preventDefault(); 

        if (!currentFile) { // Check if a file has been selected/stored
            showError('Please select or drop an image file first.');
            return;
        }

        showLoading();

        const formData = new FormData();
        formData.append('image', currentFile); // Use the stored file

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            hideLoading();

            if (response.ok && data.latex) {
                showResult(data.latex);
            } else {
                showError(data.error || 'An unknown error occurred during conversion.');
            }

        } catch (error) {
            hideLoading();
            console.error('Fetch error:', error);
            showError('Failed to connect to the server. Please try again later.');
        }
    });

     // Handle copy button click (using title for feedback)
    copyButton.addEventListener('click', () => {
        latexResult.select(); 
        latexResult.setSelectionRange(0, 99999); 

        try {
            navigator.clipboard.writeText(latexResult.value).then(() => {
                const originalTitle = copyButton.title;
                copyButton.title = 'Copied!';
                
                // Add a temporary visual feedback
                copyButton.classList.add('bg-green-50', 'dark:bg-green-900/30', 'text-green-600', 'dark:text-green-400', 'border-green-300', 'dark:border-green-700');
                
                setTimeout(() => {
                    copyButton.title = originalTitle;
                    copyButton.classList.remove('bg-green-50', 'dark:bg-green-900/30', 'text-green-600', 'dark:text-green-400', 'border-green-300', 'dark:border-green-700');
                }, 1500); 
            }).catch(err => {
                console.error('Failed to copy text using Clipboard API: ', err);
                try {
                    document.execCommand('copy');
                    const originalTitle = copyButton.title;
                    copyButton.title = 'Copied!';
                    
                    // Add a temporary visual feedback
                    copyButton.classList.add('bg-green-50', 'dark:bg-green-900/30', 'text-green-600', 'dark:text-green-400', 'border-green-300', 'dark:border-green-700');
                    
                    setTimeout(() => {
                        copyButton.title = originalTitle;
                        copyButton.classList.remove('bg-green-50', 'dark:bg-green-900/30', 'text-green-600', 'dark:text-green-400', 'border-green-300', 'dark:border-green-700');
                    }, 1500);
                } catch (execErr) {
                     console.error('Fallback copy command failed: ', execErr);
                     alert('Failed to copy code. Please copy it manually.');
                }
            });
        } catch (e) {
             console.error('Clipboard API not supported or other error: ', e);
             alert('Failed to copy code. Please copy it manually.');
        }

        window.getSelection().removeAllRanges();
    });

}); 
