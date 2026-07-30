import os
import sys
import subprocess

# --- GTK3 WINDOWS CRASH FIX ---
GTK_PATH = r"C:\Program Files\GTK3-Runtime Win64\bin"
if os.name == 'nt':
    if os.path.exists(GTK_PATH):
        os.add_dll_directory(GTK_PATH)
        if GTK_PATH not in os.environ['PATH']:
            os.environ['PATH'] = GTK_PATH + os.pathsep + os.environ['PATH']
    else:
        print(f"⚠️ Warning: GTK3 Runtime folder not found at {GTK_PATH}.")

import glob
import customtkinter as ctk
from tkinter import filedialog, messagebox
from weasyprint import HTML

# Set up initial visual theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class HTMLToPDFConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Modern HTML to PDF Converter")
        self.geometry("600x480")
        self.resizable(False, False)

        # Storage for selected paths
        self.selected_files = []
        self.selected_folder = ""
        self.last_output_dir = ""  # Tracks where PDFs were saved
        self.mode = None 

        self.setup_ui()

    def setup_ui(self):
        # Top Header Frame (For Title and Theme Selector Alignment)
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(15, 5), padx=20, fill="x")

        # Title Label
        self.title_label = ctk.CTkLabel(self.header_frame, text="HTML to PDF Converter", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(side="left", padx=5)

        # Theme Selector Dropdown
        self.theme_menu = ctk.CTkOptionMenu(
            self.header_frame, 
            values=["System", "Dark", "Light"], 
            command=self.change_theme,
            width=100
        )
        self.theme_menu.pack(side="right", padx=5)
        self.theme_menu.set("System")

        # Selection Frame
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=10, padx=20, fill="x")

        self.btn_select_files = ctk.CTkButton(self.button_frame, text="Select HTML Files", command=self.select_files)
        self.btn_select_files.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.btn_select_folder = ctk.CTkButton(self.button_frame, text="Select Folder", command=self.select_folder)
        self.btn_select_folder.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.button_frame.grid_columnconfigure((0, 1), weight=1)

        # Status & Path display box
        self.status_box = ctk.CTkTextbox(self, width=540, height=180, activate_scrollbars=True)
        self.status_box.pack(pady=10)
        self.update_status_display("Ready. Please select individual HTML file,HTML files or an entire folder to begin.")

        # Convert Action Button (Navy Blue)
        self.btn_convert = ctk.CTkButton(
            self, 
            text="Convert to PDF", 
            command=self.start_conversion, 
            state="disabled", 
            fg_color="#1B365D",       
            hover_color="#112240"     
        )
        self.btn_convert.pack(pady=15, ipadx=20, ipady=5)

    def change_theme(self, choice):
        """Dynamically toggles light, dark, or system matching style."""
        ctk.set_appearance_mode(choice) [1]

    def update_status_display(self, text):
        self.status_box.configure(state="normal")
        self.status_box.delete("1.0", "end")
        self.status_box.insert("1.0", text)
        self.status_box.configure(state="disabled")

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("HTML files", "*.html;*.htm")])
        if files:
            self.selected_files = list(files)
            self.mode = "files"
            self.btn_convert.configure(state="normal")
            
            display_text = f"Selected Files ({len(self.selected_files)}):\n" + "\n".join([os.path.basename(f) for f in self.selected_files])
            self.update_status_display(display_text)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder = folder
            self.mode = "folder"
            html_files = glob.glob(os.path.join(folder, "*.html")) + glob.glob(os.path.join(folder, "*.htm"))
            
            if not html_files:
                self.update_status_display(f"⚠️ Selected Folder:\n{folder}\n\nError: No .html or .htm files found in this directory!")
                self.btn_convert.configure(state="disabled")
                return

            self.selected_files = html_files
            self.btn_convert.configure(state="normal")
            display_text = f"Selected Folder:\n{folder}\n\nFound {len(html_files)} HTML file(s) ready for conversion."
            self.update_status_display(display_text)

    def get_unique_pdf_path(self, html_path):
        directory = os.path.dirname(html_path)
        base_name, _ = os.path.splitext(os.path.basename(html_path))
        
        pdf_path = os.path.join(directory, f"{base_name}.pdf")
        
        counter = 1
        while os.path.exists(pdf_path):
            pdf_path = os.path.join(directory, f"{base_name}{counter}.pdf")
            counter += 1
            
        return pdf_path

    def start_conversion(self):
        if not self.selected_files:
            return

        self.btn_convert.configure(state="disabled", text="Converting...")
        self.update_idletasks()

        success_count = 0
        log_messages = []
        
        # Keep track of where the files are being saved
        if self.selected_files:
            self.last_output_dir = os.path.dirname(self.selected_files[0])

        for html_file in self.selected_files:
            try:
                output_pdf = self.get_unique_pdf_path(html_file)
                HTML(html_file).write_pdf(output_pdf)
                
                filename_only = os.path.basename(output_pdf)
                log_messages.append(f"✅ Generated: {filename_only}")
                success_count += 1
            except Exception as e:
                log_messages.append(f"❌ Failed {os.path.basename(html_file)}: {str(e)}")

        log_summary = f"Process Completed! ({success_count}/{len(self.selected_files)} successful)\n\n" + "\n".join(log_messages)
        self.update_status_display(log_summary)
        
        self.btn_convert.configure(state="disabled", text="Convert to PDF")
        self.selected_files = []
        self.selected_folder = ""
        
        # Pop up dialog asking to open the folder
        if success_count > 0:
            answer = messagebox.askyesno(
                "Finished", 
                f"Successfully converted {success_count} files!\n\nWould you like to open the output folder?"
            )
            if answer:
                self.open_file_explorer(self.last_output_dir)
        else:
            messagebox.showerror("Error", "No files were successfully converted.")

    def open_file_explorer(self, path):
        """Cross-platform folder opening script tool."""
        try:
            path = os.path.normpath(path)
            if os.name == 'nt':  # Windows
                os.startfile(path)
            elif sys.platform == 'darwin':  # macOS
                subprocess.Popen(['open', path])
            else:  # Linux / Ubuntu
                subprocess.Popen(['xdg-open', path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open directory window: {e}")

if __name__ == "__main__":
    app = HTMLToPDFConverterApp()
    app.mainloop()
