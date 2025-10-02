import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image
import threading
from pathlib import Path

class ImageToWebPConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to WebP Converter")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        
        # Variables
        self.input_files = []
        self.output_folder = ""
        self.quality = tk.IntVar(value=80)
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Title Frame
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=20, padx=20, fill="x")
        
        title_label = ttk.Label(
            title_frame,
            text="🖼️ Image to WebP Converter",
            font=("Arial", 16, "bold"),
            foreground="#2c3e50"
        )
        title_label.pack()
        
        # File Selection Frame
        file_frame = ttk.LabelFrame(self.root, text="Select Images", padding=15)
        file_frame.pack(pady=10, padx=20, fill="x")
        
        self.file_list = tk.Listbox(file_frame, height=6, selectmode=tk.MULTIPLE)
        self.file_list.pack(fill="both", expand=True)
        
        file_buttons_frame = ttk.Frame(file_frame)
        file_buttons_frame.pack(fill="x", pady=10)
        
        ttk.Button(
            file_buttons_frame,
            text="📁 Add Files",
            command=self.add_files
        ).pack(side="left", padx=5)
        
        ttk.Button(
            file_buttons_frame,
            text="🗑️ Remove Selected",
            command=self.remove_files
        ).pack(side="left", padx=5)
        
        ttk.Button(
            file_buttons_frame,
            text="📂 Add Folder",
            command=self.add_folder
        ).pack(side="left", padx=5)
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(self.root, text="Conversion Settings", padding=15)
        settings_frame.pack(pady=10, padx=20, fill="x")
        
        # Image Quality
        quality_frame = ttk.Frame(settings_frame)
        quality_frame.pack(fill="x", pady=5)
        
        ttk.Label(quality_frame, text="Image Quality:").pack(side="left")
        ttk.Scale(
            quality_frame,
            from_=1, to=100,
            variable=self.quality,
            orient="horizontal"
        ).pack(side="left", fill="x", expand=True, padx=10)
        
        self.quality_label = ttk.Label(quality_frame, text="80%")
        self.quality_label.pack(side="right")
        
        # Output Folder
        output_frame = ttk.Frame(settings_frame)
        output_frame.pack(fill="x", pady=10)
        
        ttk.Label(output_frame, text="Output Folder:").pack(side="left")
        
        self.output_path = ttk.Entry(output_frame, state="readonly")
        self.output_path.pack(side="left", fill="x", expand=True, padx=10)
        
        ttk.Button(
            output_frame,
            text="📁 Choose Folder",
            command=self.choose_output_folder
        ).pack(side="right")
        
        # Progress Frame
        progress_frame = ttk.Frame(self.root)
        progress_frame.pack(pady=10, padx=20, fill="x")
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.pack(fill="x")
        
        self.status_label = ttk.Label(progress_frame, text="Ready for conversion")
        self.status_label.pack(pady=5)
        
        # Control Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20, padx=20, fill="x")
        
        ttk.Button(
            button_frame,
            text="🔄 Start Conversion",
            command=self.start_conversion,
            style="Accent.TButton"
        ).pack(side="right", padx=5)
        
        ttk.Button(
            button_frame,
            text="🗑️ Clear All",
            command=self.clear_all
        ).pack(side="left", padx=5)
        
        # Bind events
        self.quality.trace('w', self.update_quality_label)
        
    def update_quality_label(self, *args):
        self.quality_label.config(text=f"{self.quality.get()}%")
        
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Images for Conversion",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.gif"),
                ("All files", "*.*")
            ]
        )
        if files:
            self.input_files.extend(files)
            self.update_file_list()
            
    def add_folder(self):
        folder = filedialog.askdirectory(title="Select Folder Containing Images")
        if folder:
            supported_formats = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.tif', '*.gif')
            image_files = []
            for fmt in supported_formats:
                image_files.extend(Path(folder).glob(fmt))
                image_files.extend(Path(folder).glob(fmt.upper()))
            
            # Remove duplicates and add to input files
            self.input_files.extend(list(set(image_files)))
            self.update_file_list()
            
    def remove_files(self):
        selected = self.file_list.curselection()
        for index in selected[::-1]:
            if index < len(self.input_files):
                del self.input_files[index]
        self.update_file_list()
        
    def update_file_list(self):
        self.file_list.delete(0, tk.END)
        for file in self.input_files:
            self.file_list.insert(tk.END, str(file))
            
    def choose_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_path.config(state="normal")
            self.output_path.delete(0, tk.END)
            self.output_path.insert(0, folder)
            self.output_path.config(state="readonly")
            
    def clear_all(self):
        self.input_files = []
        self.output_folder = ""
        self.output_path.config(state="normal")
        self.output_path.delete(0, tk.END)
        self.output_path.config(state="readonly")
        self.update_file_list()
        self.progress['value'] = 0
        self.status_label.config(text="Ready for conversion")
        
    def start_conversion(self):
        if not self.input_files:
            messagebox.showwarning("Warning", "Please add files for conversion")
            return
            
        if not self.output_folder:
            messagebox.showwarning("Warning", "Please select output folder")
            return
            
        # Run conversion in separate thread
        thread = threading.Thread(target=self.convert_images)
        thread.daemon = True
        thread.start()
        
    def convert_images(self):
        total_files = len(self.input_files)
        successful = 0
        failed = []
        
        self.progress['value'] = 0
        self.progress['maximum'] = total_files
        
        for index, input_path in enumerate(self.input_files):
            try:
                # Update status
                filename = os.path.basename(input_path)
                self.status_label.config(text=f"Converting {filename}...")
                
                # Open and convert image
                with Image.open(input_path) as img:
                    # Convert to RGB if image is RGBA
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    
                    # Create output filename
                    output_filename = Path(input_path).stem + '.webp'
                    output_path = Path(self.output_folder) / output_filename
                    
                    # Save as WebP
                    img.save(
                        output_path,
                        'WEBP',
                        quality=self.quality.get(),
                        optimize=True
                    )
                
                successful += 1
                
            except Exception as e:
                failed.append(f"{os.path.basename(input_path)}: {str(e)}")
                
            finally:
                # Update progress bar
                self.progress['value'] = index + 1
                self.root.update_idletasks()
        
        # Show results
        self.show_results(successful, total_files, failed)
        
    def show_results(self, successful, total, failed):
        message = f"Successfully converted {successful} out of {total} files!"
        
        if failed:
            message += f"\n\nFailed to convert {len(failed)} files:"
            for fail in failed[:5]:  # Show only first 5 errors
                message += f"\n• {fail}"
            if len(failed) > 5:
                message += f"\n• ...and {len(failed) - 5} more"
        
        self.status_label.config(text="Conversion completed")
        messagebox.showinfo("Conversion Results", message)

if __name__ == "__main__":
    # Create main window
    root = tk.Tk()
    
    # Set theme
    style = ttk.Style()
    style.theme_use('clam')
    
    # Run application
    app = ImageToWebPConverter(root)
    root.mainloop()