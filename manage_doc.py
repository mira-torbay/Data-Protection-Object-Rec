import webbrowser
import os
from scan import scan
import time  # remember to remove this, not needed for actual algorithm

webbrowser.open_new(r'file://C:\Users\mirat\Downloads\Mira_Torbay_Technical_Resume_June_2025.pdf')
file_status = "open"

if not scan():
    os.system("taskkill /im msedge.exe /f")  # note: kills ALL Microsoft Edge tasks, should probably make this more specific
    file_status = "closed"

