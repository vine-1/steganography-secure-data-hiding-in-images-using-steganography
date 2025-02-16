import streamlit as st
import cv2
import numpy as np
import os

# --- Utility Functions ---
def int_to_bits(num, bit_length):
    """Convert an integer to a list of bits of given length."""
    return [int(b) for b in format(num, f'0{bit_length}b')]

def str_to_bits(s):
    """Convert a string into its binary representation (8 bits per character)."""
    bits = []
    for char in s:
        bits.extend([int(b) for b in format(ord(char), '08b')])
    return bits

def bits_to_int(bits):
    """Convert a list of bits to an integer."""
    return int("".join(str(b) for b in bits), 2)

def bits_to_str(bits):
    """Convert a list of bits into a string (8 bits per character)."""
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        chars.append(chr(int("".join(str(b) for b in byte), 2)))
    return "".join(chars)

def embed_data(image, data_bits):
    """Embed binary data into the least significant bits (LSB) of an image."""
    flat = image.flatten()
    if len(data_bits) > len(flat):
        st.error("Data too large to embed in this image!")
        return None
    for i in range(len(data_bits)):
        flat[i] = (flat[i] & ~1) | data_bits[i]
    return flat.reshape(image.shape)

def extract_data(image):
    """Extract binary data from the least significant bits (LSB) of an image."""
    flat = image.flatten()
    bits = [flat[i] & 1 for i in range(len(flat))]
    return bits

# --- Streamlit UI ---
st.title("🔒 Image Steganography")

tab1, tab2 = st.tabs(["Encrypt", "Decrypt"])

with tab1:
    st.header("🛠 Encrypt a Message into an Image")
    
    uploaded_file = st.file_uploader("📂 Upload an image (PNG, JPG)", type=["png", "jpg", "jpeg"])
    secret_message = st.text_area("💬 Enter Secret Message")
    
    passcode = st.text_input("🔑 Enter Passcode", type="password", key="encrypt_passcode")

    if uploaded_file and secret_message and passcode:
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Create header: [Passcode Length (16 bits)] + [Passcode] + [Message Length (32 bits)] + [Message]
        header_bits = []
        header_bits.extend(int_to_bits(len(passcode), 16))
        header_bits.extend(str_to_bits(passcode))
        header_bits.extend(int_to_bits(len(secret_message), 32))
        header_bits.extend(str_to_bits(secret_message))

        encoded_image = embed_data(image, header_bits)

        if encoded_image is not None:
            encrypted_path = "encrypted_image.png"
            cv2.imwrite(encrypted_path, encoded_image)
            st.success("✅ Encryption successful! Download your encrypted image.")
            with open(encrypted_path, "rb") as file:
                st.download_button("📥 Download Encrypted Image", file, file_name="encrypted.png", mime="image/png")

with tab2:
    st.header("🔓 Decrypt a Message from an Image")
    
    encrypted_file = st.file_uploader("📂 Upload Encrypted Image", type=["png"])

    input_passcode = st.text_input("🔑 Enter Passcode", type="password", key="decrypt_passcode")

    if encrypted_file and input_passcode:
        image = cv2.imdecode(np.frombuffer(encrypted_file.read(), np.uint8), cv2.IMREAD_COLOR)

        bits = extract_data(image)

        # Extract header
        passcode_len = bits_to_int(bits[:16])
        stored_passcode = bits_to_str(bits[16:16 + passcode_len * 8])

        if input_passcode != stored_passcode:
            st.error("❌ Incorrect Passcode!")
        else:
            start = 16 + passcode_len * 8
            message_len = bits_to_int(bits[start:start + 32])
            secret_message = bits_to_str(bits[start + 32:start + 32 + message_len * 8])

            st.success("✅ Decryption successful! Here is your secret message:")
            st.text_area("📜 Decrypted Message", secret_message)
