import os
from scan import scan
import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
from PIL import Image, ImageTk
import cv2

filename = ""
pdf_images = []
pdf_labels = []
current_page = 0
scan_job = None
canvas_image_id = None  # current image on the canvas
camera = None  # global camera object

# --- PDF Display Helpers ---
def clear_pdf_display():
    global canvas_image_id, pdf_images, current_page
    if canvas_image_id is not None:
        canvas.delete(canvas_image_id)
        canvas_image_id = None
    pdf_images.clear()
    current_page = 0

def display_page(page_num):
    global pdf_images, current_page, canvas_image_id
    if 0 <= page_num < len(pdf_images):
        if canvas_image_id is not None:
            canvas.delete(canvas_image_id)
        img = pdf_images[page_num]
        # Center image horizontally
        canvas_image_id = canvas.create_image(canvas.winfo_width()//2, 0, anchor="n", image=img)
        current_page = page_num
        page_label.config(text=f"Page {current_page+1} of {len(pdf_images)}")
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.yview_moveto(0)

def is_camera_running():
    print("Starting camera...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera failed to start.")
        return False
    cap.release()
    print("Camera running.")
    return True

# --- PDF Loading ---
def doc_picker():
    global filename, pdf_images, current_page, scan_job, camera
    filetypes = [("PDF files", "*.pdf")]
    filename = filedialog.askopenfilename(
        title="Select a Document",
        filetypes=filetypes
    )
    if filename:
        print("PDF selected")
        label.config(text=f"Selected File:\n{filename}")
        # Start and keep camera open
        print("Starting camera...")
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            print("Camera failed to start.")
            messagebox.showerror("Camera Error", "Could not start camera. Please check your webcam.")
            camera = None
            return
        # Wait for camera to be ready and able to read a frame
        import time
        max_attempts = 20
        for attempt in range(max_attempts):
            ret, _ = camera.read()
            if ret:
                print("Camera running.")
                break
            time.sleep(0.1)
        else:
            print("Camera failed to provide frame.")
            messagebox.showerror("Camera Error", "Camera could not provide a frame. Please check your webcam.")
            camera.release()
            camera = None
            return
        if scan_job is None:
            scan_job = root.after(2000, scan_and_monitor)
        load_pdf(filename)
    else:
        label.config(text="No file selected.")

def load_pdf(path):
    global pdf_images, current_page
    clear_pdf_display()
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
        doc.close()
        display_page(0)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load PDF: {e}")

def show_page(page_num):
    display_page(page_num)

def next_page():
    if current_page + 1 < len(pdf_images):
        show_page(current_page + 1)

def prev_page():
    if current_page - 1 >= 0:
        show_page(current_page - 1)

# --- PDF Closing ---
def close_pdf():
    global pdf_images, current_page, scan_job, camera, canvas_image_id
    clear_pdf_display()
    current_page = 0
    label.config(text="PDF closed due to detected phone/camera.")
    page_label.config(text="")
    # Stop scanning when PDF is closed
    if scan_job is not None:
        root.after_cancel(scan_job)
        scan_job = None
    # Release camera
    if camera is not None:
        camera.release()
        camera = None

# --- Scanning ---
def scan_and_monitor():
    global camera
    if camera is None:
        return
    # Pass the open camera to scan()
    if not scan(camera):
        close_pdf()
        messagebox.showwarning("Security Alert", "Phone or camera detected! PDF has been closed.")
    else:
        global scan_job
        scan_job = root.after(2000, scan_and_monitor)  # Check every 2 seconds

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

# scrolling

def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
canvas.bind_all("<MouseWheel>", _on_mousewheel)

def _on_mousewheel_linux(event):
    if event.num == 4:
        canvas.yview_scroll(-1, "units")
    elif event.num == 5:
        canvas.yview_scroll(1, "units")
canvas.bind_all("<Button-4>", _on_mousewheel_linux)
canvas.bind_all("<Button-5>", _on_mousewheel_linux)

nav_frame = tk.Frame(root)
nav_frame.pack(pady=5)

prev_btn = tk.Button(nav_frame, text="Previous", command=prev_page)
prev_btn.grid(row=0, column=0, padx=5)

page_label = tk.Label(nav_frame, text="")
page_label.grid(row=0, column=1, padx=5)

next_btn = tk.Button(nav_frame, text="Next", command=next_page)
next_btn.grid(row=0, column=2, padx=5)

root.mainloop()

