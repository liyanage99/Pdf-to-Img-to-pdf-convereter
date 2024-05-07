import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2image import convert_from_path
from PIL import Image
import os

# Specify Poppler bin directory
poppler_dir = r'C:\Program Files\poppler-24.02.0\Library\bin'  # Update XX with the installed version
os.environ["PATH"] += os.pathsep + poppler_dir

def convert_pdf_to_images(pdf_path, output_folder, image_format):
    try:
        images = convert_from_path(pdf_path)
        for i, image in enumerate(images):
            image_path = os.path.join(output_folder, f"page_{i + 1}.{image_format.lower()}")
            image.save(image_path, image_format.upper())
        messagebox.showinfo("Conversion Complete", "PDF successfully converted to images!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def convert_images_to_pdf(image_paths, output_pdf_path):
    try:
        images = []
        for image_path in image_paths:
            img = Image.open(image_path)
            images.append(img.convert("RGB"))
        
        if images:
            images[0].save(output_pdf_path, save_all=True, append_images=images[1:])
            messagebox.showinfo("Conversion Complete", "Images successfully converted to PDF!")
        else:
            messagebox.showwarning("Warning", "No images selected for conversion!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def select_pdf_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        pdf_entry.delete(0, tk.END)
        pdf_entry.insert(0, file_path)

def select_output_folder():
    output_folder = filedialog.askdirectory()
    if output_folder:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_folder)

def select_images():
    image_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if image_paths:
        images_entry.delete(0, tk.END)
        images_entry.insert(0, ", ".join(image_paths))

def convert_button_clicked():
    pdf_path = pdf_entry.get()
    output_folder = output_entry.get()
    image_format = format_var.get()

    if pdf_path and output_folder:
        convert_pdf_to_images(pdf_path, output_folder, image_format)
    elif images_entry.get() and output_entry.get():
        image_paths = images_entry.get().split(", ")
        output_pdf_path = os.path.join(output_entry.get(), "images_to_pdf.pdf")
        convert_images_to_pdf(image_paths, output_pdf_path)
    else:
        messagebox.showwarning("Warning", "Please select input files and output folder!")

# Create main window
window = tk.Tk()
# window.geometry("400x300")
window.resizable(False, False)

window.title("PDF/Image Converter")

# Create widgets for PDF to Image conversion
tk.Label(window, text="Convert PDF to Images", font=("Helvetica", 12, "bold")).pack(pady=(10, 5))

tk.Label(window, text="Select PDF File:").pack(pady=(5, 2))
pdf_entry = tk.Entry(window, width=50)
pdf_entry.pack(padx=10, pady=(0, 5))
tk.Button(window, text="Browse", command=select_pdf_file).pack(pady=(0, 10))

tk.Label(window, text="Select Output Folder:").pack(pady=(5, 2))
output_entry = tk.Entry(window, width=50)
output_entry.pack(padx=10, pady=(0, 5))
tk.Button(window, text="Browse", command=select_output_folder).pack(pady=(0, 10))

tk.Label(window, text="Select Image Format:").pack(pady=(5, 2))
format_var = tk.StringVar(value="JPEG")  # Default format
format_menu = tk.OptionMenu(window, format_var, "JPEG", "PNG")
format_menu.pack(pady=(0, 10))

# Create widgets for Image to PDF conversion
tk.Label(window, text="Convert Images to PDF", font=("Helvetica", 12, "bold")).pack(pady=(10, 5))

tk.Label(window, text="Select Image Files:").pack(pady=(5, 2))
images_entry = tk.Entry(window, width=50)
images_entry.pack(padx=10, pady=(0, 5))
tk.Button(window, text="Browse", command=select_images).pack(pady=(0, 10))

tk.Button(window, text="Convert", command=convert_button_clicked).pack(pady=(20, 10))

# Start the main loop
window.mainloop()