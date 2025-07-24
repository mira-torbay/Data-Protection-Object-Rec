# Object Recognition PDF Viewer

This application serves as a demonstration of a potential method of preventing unauthorized copying or sharing of a document via the "analog hole" -- physically recording the screen with a separate device. If a phone or camera is detected by the device's webcam while a PDF is open, the document will be closed automatically. The PDF is displayed inside the app with scrolling and page navigation.

## Features
- Select and view PDF files inside the app
- Scroll and navigate through PDF pages
- Webcam detects phones/cameras that may be used to film the screen (using opencv)
- Automatically closes the PDF if a phone/camera is detected, preventing copying by analog means
- Only opens the PDF if the camera is working, and ensures the camera is activated and running before the PDF is opened

## Requirements
- Python 3.8+
- Windows (other OSes may work, but this is tested on Windows)

### Python Packages
- opencv-python
- numpy
- ultralytics
- Pillow
- PyMuPDF

## Installation

1. **Clone or download this repository.**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure your webcam is connected and accessible.**
   - The app will check for a working camera before opening any PDF.

## Running the App

Move into the project directory using:
```bash
cd <path-to-directory>/Data-Protection-Object-Rec
```

From the project directory, run:
```bash
python manage_doc.py
```

## Usage
1. Click the **Browse** button to select a PDF file.
2. The app will print status messages in the console:
   - "PDF selected"
   - "Starting camera..."
   - "Camera running." (if startup successful)
3. The PDF will open in a scrollable viewer. Use **Previous** and **Next** to change pages.
4. If a phone or camera is detected by your webcam, the PDF will be closed automatically.

## Troubleshooting

### Import Errors (fitz, PIL, cv2)
- Make sure you installed all dependencies with `pip install -r requirements.txt`.
- If you see `Unable to import 'fitz'`, try:
  ```bash
  pip install PyMuPDF
  ```
- If you see `Unable to import 'PIL'`, try:
  ```bash
  pip install Pillow
  ```
- If you see `Unable to import 'cv2'`, try:
  ```bash
  pip install opencv-python
  ```

### Camera Not Found
- Ensure your webcam is plugged in and not being used by another application.
- If you have multiple cameras, you may need to adjust the camera index in the code (`cv2.VideoCapture(0)`).

### PDF Not Displaying Correctly
- Make sure the PDF is not password-protected or corrupted.
- The app resizes pages to fit the window width and allows vertical scrolling.

## Notes and Disclaimer
- This app is designed for demonstration and educational purposes.
- It does not implement features such as document copying or sharing prevention, encryption, or manage how PDFs are opened/ensure they are only opened in this app. As such, it is NOT, on its own, a secure method of file management. It is meant as proof-of-concept for a feature that could be implemented in addition to a robust DRM or DLP system.
