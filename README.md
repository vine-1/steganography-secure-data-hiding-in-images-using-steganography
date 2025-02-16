Image Steganography Using LSB Technique

Overview

This project implements Least-Significant-Bit (LSB) steganography to securely hide a secret message and passcode inside an image. It provides a Streamlit-based web UI for easy encryption and decryption, making it simple for users to encode and retrieve hidden data.

Features

✅ Encryption: Embeds a secret message and passcode into mypic.jpg and saves the output as encrypted.png.

✅ Decryption: Retrieves the hidden message from encrypted.png when the correct passcode is entered.

✅ Streamlit Web UI: A modern and interactive web interface for easy use.

✅ Secure Data Storage: Uses a structured header to store passcode length, passcode, and message length for accurate extraction.

Requirements

Python 3.x

OpenCV (for image processing)

NumPy (for numerical operations)

Streamlit (for the web-based UI)

Installation

Clone the repository:

git clone https://github.com/your-repository/steganography.git
cd steganography

Install dependencies:

pip install -r requirements.txt

Place an image (mypic.jpg) in the project directory.

Usage

Run the Application

Start the Streamlit app by running:

streamlit run steganography.py

Then open http://localhost:8501/ in your browser.

Encryption

Upload an image (mypic.jpg).

Enter your secret message and passcode.

Click Encrypt to generate encrypted.png.

Decryption

Load encrypted.png.

Enter the correct passcode.

Retrieve the hidden message.

Requirements File (requirements.txt)

streamlit
opencv-python-headless
numpy

License

This project is open-source and free to use.

