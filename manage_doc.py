import os
from scan import scan
import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2image import convert_from_path
from PIL import Image, ImageTk

filename = ""
pdf_images = []
pdf_labels = []
current_page = 0


def doc_picker():
    global filename, pdf_images, current_page
    filetypes = [("PDF files", "*.pdf")]
    filename = filedialog.askopenfilename(
        title="Select a Document",
        filetypes=filetypes
    )
    if filename:
        label.config(text=f"Selected File:\n{filename}")
        load_pdf(filename)
    else:
        label.config(text="No file selected.")

def load_pdf(path):
    global pdf_images, pdf_labels, current_page
    for lbl in pdf_labels:
        lbl.destroy()
    pdf_labels.clear()
    pdf_images.clear()
    current_page = 0
    try:
        pages = convert_from_path(path, dpi=100)
        for i, page in enumerate(pages):
            img = ImageTk.PhotoImage(page)
            pdf_images.append(img)
            lbl = tk.Label(pdf_frame, image=img)
            pdf_labels.append(lbl)
            if i == 0:
                lbl.pack()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load PDF: {e}")

def show_page(page_num):
    global pdf_labels, current_page
    if 0 <= page_num < len(pdf_labels):
        pdf_labels[current_page].pack_forget()
        pdf_labels[page_num].pack()
        current_page = page_num
        page_label.config(text=f"Page {current_page+1} of {len(pdf_labels)}")

def next_page():
    if current_page + 1 < len(pdf_labels):
        show_page(current_page + 1)

def prev_page():
    if current_page - 1 >= 0:
        show_page(current_page - 1)

def close_pdf():
    global pdf_labels, pdf_images, current_page
    for lbl in pdf_labels:
        lbl.destroy()
    pdf_labels.clear()
    pdf_images.clear()
    current_page = 0
    label.config(text="PDF closed due to detected phone/camera.")
    page_label.config(text="")

def scan_and_monitor():
    if not scan():
        close_pdf()
        messagebox.showwarning("Security Alert", "Phone or camera detected! PDF has been closed.")
    else:
        root.after(2000, scan_and_monitor)  # Check every 2 seconds

root = tk.Tk()
root.title("Document Selector & Viewer")
root.geometry("600x700")

label = tk.Label(root, text="Please select a document file", wraplength=550, justify="center")
label.pack(pady=10)

btn = tk.Button(root, text="Browse", command=doc_picker)
btn.pack(pady=5)

pdf_frame = tk.Frame(root)
pdf_frame.pack(expand=True, fill="both")

nav_frame = tk.Frame(root)
nav_frame.pack(pady=5)

prev_btn = tk.Button(nav_frame, text="Previous", command=prev_page)
prev_btn.grid(row=0, column=0, padx=5)

page_label = tk.Label(nav_frame, text="")
page_label.grid(row=0, column=1, padx=5)

next_btn = tk.Button(nav_frame, text="Next", command=next_page)
next_btn.grid(row=0, column=2, padx=5)

root.after(2000, scan_and_monitor)
root.mainloop()

