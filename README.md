# html-pdf-desktop-converter

A sleek CustomTkinter desktop application utilizing WeasyPrint to seamlessly batch-convert HTML layouts and entire folders into print-ready PDFs with full CSS styling.

## 🚀 Features
* **Modern GUI Layout:** Built using CustomTkinter with dynamic Light/Dark/System theme mapping.
* **Batch & Folder Processing:** Drop an array of files or scan an entire root directory automatically.
* **Smart Version Indexing:** Automatically appends numeric markers (`file1.pdf`, `file2.pdf`) to prevent file overwrites.
* **Cross-Platform Explore Tool:** Prompts to launch your native OS File Explorer immediately after extraction.


## 🛠️ Prerequisites (Windows)
To run this application on Windows, you must install the **GTK3 Runtime Engine** to support the WeasyPrint PDF layout engine:
1. Download and run the runtime setup file from  https://github.com/tschoonj/gtk-for-windows-runtime-environment-installer/releases.
2. Ensure you install it to the default system path: `C:\Program Files\GTK3-Runtime Win64`.


## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Pasindu-vsc/HTML-to-pdf-.git
   ```
2. **Go into thhe cloned folder**
   ```bash
   cd HTML-to-pdf-
   ```
3. **Set up a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   # On Windows activate with:
   venv\Scripts\activate
   # On Linux/macOS activate with:
   source venv/bin/activate
   ```

4. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 How to Run
Execute the application from your project root directory by running :
```bash
   python html_to_pdf.py
```

## 📝 License
This project is licensed under the MIT License - feel free to use, modify, and distribute it as you wish!