import os
from scan import scan
import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
from PIL import Image, ImageTk

filename = ""
pdf_images = []
pdf_labels = []
current_page = 0
scan_job = None

# --- PDF Display Helpers ---
def clear_pdf_display():
    for lbl in pdf_labels:
        lbl.destroy()
    pdf_labels.clear()
    pdf_images.clear()

def display_page(page_num):
    global pdf_labels, current_page
    if 0 <= page_num < len(pdf_labels):
        for i, lbl in enumerate(pdf_labels):
            lbl.pack_forget()
        pdf_labels[page_num].pack()
        current_page = page_num
        page_label.config(text=f"Page {current_page+1} of {len(pdf_labels)}")
        # Scroll to top
        canvas.yview_moveto(0)

# --- PDF Loading ---
def doc_picker():
    global filename, pdf_images, current_page, scan_job
    filetypes = [("PDF files", "*.pdf")]
    filename = filedialog.askopenfilename(
        title="Select a Document",
        filetypes=filetypes
    )
    if filename:
        label.config(text=f"Selected File:\n{filename}")
        # start scanning after PDF is selected, before opening
        if scan_job is None:
            scan_job = root.after(2000, scan_and_monitor)
        load_pdf(filename)
    else:
        label.config(text="No file selected.")

def load_pdf(path):
    global pdf_images, pdf_labels, current_page
    clear_pdf_display()
    current_page = 0
    try:
        doc = fitz.open(path)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=100)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            # Resize to fit canvas width
            canvas_width = canvas.winfo_width() or 550
            scale = canvas_width / img.width
            new_height = int(img.height * scale)
            img_resized = img.resize((canvas_width, new_height), Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(img_resized)
            pdf_images.append(tk_img)
            lbl = tk.Label(canvas_frame, image=tk_img)
            pdf_labels.append(lbl)
            if i == 0:
                lbl.pack()
        doc.close()
        display_page(0)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load PDF: {e}")

def show_page(page_num):
    display_page(page_num)

def next_page():
    if current_page + 1 < len(pdf_labels):
        show_page(current_page + 1)

def prev_page():
    if current_page - 1 >= 0:
        show_page(current_page - 1)

def close_pdf():
    global pdf_labels, pdf_images, current_page, scan_job
    clear_pdf_display()
    current_page = 0
    label.config(text="PDF closed due to detected phone/camera.")
    page_label.config(text="")
    # stop scanning when PDF is closed
    if scan_job is not None:
        root.after_cancel(scan_job)
        scan_job = None

def scan_and_monitor():
    if not scan():
        close_pdf()
        messagebox.showwarning("Security Alert", "Phone or camera detected! PDF has been closed.")
    else:
        global scan_job
        scan_job = root.after(2000, scan_and_monitor)  # check every 2 seconds

root = tk.Tk()
root.title("Document Selector & Viewer")
root.geometry("600x700")

label = tk.Label(root, text="Please select a document file", wraplength=550, justify="center")
label.pack(pady=10)

btn = tk.Button(root, text="Browse", command=doc_picker)
btn.pack(pady=5)

# --- Scrollable PDF Frame ---
pdf_frame = tk.Frame(root)
pdf_frame.pack(expand=True, fill="both")

canvas = tk.Canvas(pdf_frame, width=550, height=500)
canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(pdf_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

canvas_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
canvas_frame.bind("<Configure>", on_canvas_configure)

nav_frame = tk.Frame(root)
nav_frame.pack(pady=5)

prev_btn = tk.Button(nav_frame, text="Previous", command=prev_page)
prev_btn.grid(row=0, column=0, padx=5)

page_label = tk.Label(nav_frame, text="")
page_label.grid(row=0, column=1, padx=5)

next_btn = tk.Button(nav_frame, text="Next", command=next_page)
next_btn.grid(row=0, column=2, padx=5)

root.mainloop()

