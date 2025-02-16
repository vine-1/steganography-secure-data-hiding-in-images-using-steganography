import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import ttk, messagebox

def bits_to_int(bits):
    # Convert a list of bits to an integer.
    return int("".join(str(b) for b in bits), 2)

def bits_to_str(bits):
    # Convert a list of bits into a string (8 bits per character).
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        chars.append(chr(int("".join(str(b) for b in byte), 2)))
    return "".join(chars)

def decrypt():
    img_path = "encrypted.png"
    if not os.path.exists(img_path):
        messagebox.showerror("Error", "Encrypted image 'encrypted.png' not found!")
        return
    image = cv2.imread(img_path)
    if image is None:
        messagebox.showerror("Error", "Failed to load 'encrypted.png'.")
        return

    flat = image.flatten()
    bits = [flat[i] & 1 for i in range(len(flat))]

    # Extract header: first 16 bits for passcode length.
    passcode_len_bits = bits[:16]
    passcode_len = bits_to_int(passcode_len_bits)
    start = 16

    # Next passcode_len * 8 bits store the passcode.
    passcode_bits = bits[start:start + passcode_len * 8]
    stored_passcode = bits_to_str(passcode_bits)

    input_passcode = passcode_entry.get()
    if input_passcode != stored_passcode:
        messagebox.showerror("Error", "Incorrect passcode!")
        return

    # Next 32 bits store the secret message length.
    start += passcode_len * 8
    message_len_bits = bits[start:start + 32]
    message_len = bits_to_int(message_len_bits)
    start += 32

    # Next message_len * 8 bits are the secret message.
    message_bits = bits[start:start + message_len * 8]
    secret_message = bits_to_str(message_bits)

    secret_message_label.config(text=f"Secret Message: {secret_message}")

# GUI Setup
root = tk.Tk()
root.title("Steganography - Decrypt")
root.geometry("400x300")
style = ttk.Style(root)
style.theme_use('clam')

frame = ttk.Frame(root, padding="20")
frame.pack(expand=True)

ttk.Label(frame, text="Enter Passcode:").grid(row=0, column=0, sticky="w", pady=5)
passcode_entry = ttk.Entry(frame, width=40, show="*")
passcode_entry.grid(row=1, column=0, pady=5)

decrypt_button = ttk.Button(frame, text="Decrypt", command=decrypt)
decrypt_button.grid(row=2, column=0, pady=10)

secret_message_label = ttk.Label(frame, text="Secret Message: ", wraplength=350)
secret_message_label.grid(row=3, column=0, pady=10)

root.mainloop()