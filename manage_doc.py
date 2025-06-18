import webbrowser
import os
from scan import scan
import tkinter as tk
from tkinter import filedialog, messagebox

filename = ""


def doc_picker():
    filetypes = [("PDF files", "*.pdf")]

    global filename
    filename = filedialog.askopenfilename(
        title="Select a Document",
        filetypes=filetypes
    )

    if filename:
        label.config(text=f"Selected File:\n{filename}")
    else:
        label.config(text="No file selected.")


root = tk.Tk()
root.title("Document Selector")
root.geometry("400x200")

label = tk.Label(root, text="Please select a document file", wraplength=350, justify="center")
label.pack(pady=20)

btn = tk.Button(root, text="Browse", command=doc_picker)
btn.pack(pady=10)

root.mainloop()

webbrowser.open_new(filename)
file_status = "open"

if not scan():
    os.system("taskkill /im msedge.exe /f")  # note: kills ALL Microsoft Edge tasks, should probably make this more specific
    file_status = "closed"

