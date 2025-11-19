import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from pathlib import Path
from PIL import Image
import threading
import pillow_heif

# Audio/Video processing
from moviepy.editor import VideoFileClip, AudioFileClip

# Register HEIF opener for Apple formats
pillow_heif.register_heif_opener()

# Set Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class MacConverterPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Config ---
        self.title("Mac Converter Pro")
        self.geometry("1100x780")
        
        # --- Modern Color Palette (Midnight & Indigo) ---
        self.colors = {
            "bg_main": "#0f172a",     # Slate 900 (Main Background)
            "bg_sidebar": "#1e293b",  # Slate 800 (Sidebar)
            "accent": "#6366f1",      # Indigo 500 (Primary Brand Color)
            "accent_hover": "#4f46e5",# Indigo 600
            "btn_default": "#334155", # Slate 700
            "btn_hover": "#475569",   # Slate 600
            "text": "#f8fafc",        # Slate 50
            "text_dim": "#94a3b8",    # Slate 400
            "item_bg": "#1e293b",     # Slate 800 (List Items)
            "success": "#10b981",     # Emerald
            "warning": "#f59e0b",     # Amber
            "error": "#ef4444"        # Red
        }
        self.configure(fg_color=self.colors["bg_main"])

        # --- Layout Grid ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- State Data ---
        self.files_to_convert = []
        self.file_widgets = {}
        
        # --- Format Definitions ---
        self.format_categories = {
            "Image": ["PNG", "JPEG", "JPG", "WEBP", "ICNS", "PDF", "TIFF", "BMP", "ICO", "HEIC"],
            "Audio": ["MP3", "WAV", "FLAC", "AAC", "M4A", "OGG", "WMA", "AIFF"],
            "Video": ["MP4", "MOV", "AVI", "MKV", "WEBM", "WMV", "FLV", "MPEG", "GIF"]
        }

        self.valid_inputs = {
            "image": ['.jpg', '.jpeg', '.png', '.heic', '.webp', '.bmp', '.tiff', '.ico', '.pdf'],
            "video": ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.wmv', '.flv', '.mpeg', '.gif'],
            "audio": ['.mp3', '.wav', '.flac', '.m4a', '.ogg', '.wma', '.aiff', '.aac']
        }

        # --- Build UI ---
        self.create_sidebar()
        self.create_main_area()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=0, fg_color=self.colors["bg_sidebar"])
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1) 

        # Logo / Brand
        self.logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.logo_frame.grid(row=0, column=0, padx=30, pady=(50, 40), sticky="w")
        
        ctk.CTkLabel(
            self.logo_frame, 
            text="MAC", 
            font=ctk.CTkFont(family="SF Pro Display", size=32, weight="bold"),
            text_color=self.colors["text"],
            height=30
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            self.logo_frame, 
            text="CONVERTER PRO", 
            font=ctk.CTkFont(family="SF Pro Display", size=14, weight="bold"),
            text_color=self.colors["accent"],
            height=20
        ).pack(anchor="w")

        # --- File Controls ---
        self.create_btn("Add Files", self.add_files, 1, "+")
        self.create_btn("Add Folder", self.add_folder, 2, "📂")
        self.create_btn("Clear Queue", self.clear_list, 3, "🗑️")

        # --- Separator ---
        ctk.CTkFrame(self.sidebar, height=2, fg_color=self.colors["btn_default"]).grid(row=4, column=0, sticky="ew", padx=30, pady=30)

        # --- Settings Section ---
        self.settings_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.settings_frame.grid(row=5, column=0, sticky="ew", padx=20)

        ctk.CTkLabel(self.settings_frame, text="OUTPUT SETTINGS", text_color=self.colors["text_dim"], 
                    font=("Arial", 11, "bold")).pack(anchor="w", padx=10, pady=(0, 10))

        # Mode Switcher
        self.mode_switch = ctk.CTkSegmentedButton(
            self.settings_frame,
            values=["Image", "Audio", "Video"],
            command=self.update_format_menu,
            selected_color=self.colors["accent"],
            selected_hover_color=self.colors["accent_hover"],
            unselected_color=self.colors["btn_default"],
            unselected_hover_color=self.colors["btn_hover"],
            text_color=self.colors["text"],
            font=("Arial", 12, "bold"),
            height=40,
            corner_radius=8
        )
        self.mode_switch.pack(fill="x", padx=5, pady=5)
        self.mode_switch.set("Image")

        # Format Dropdown
        self.format_menu = ctk.CTkOptionMenu(
            self.settings_frame,
            values=self.format_categories["Image"],
            fg_color=self.colors["btn_default"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["accent_hover"],
            text_color=self.colors["text"],
            height=45,
            corner_radius=10,
            anchor="center",
            font=("Arial", 14, "bold"),
            dropdown_font=("Arial", 13)
        )
        self.format_menu.pack(fill="x", padx=5, pady=(15, 0))

        # --- Main Action ---
        self.btn_convert = ctk.CTkButton(
            self.sidebar,
            text="START CONVERSION",
            font=ctk.CTkFont(size=15, weight="bold"),
            height=65,
            corner_radius=12,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            command=self.start_conversion_thread,
            border_width=1,
            border_color="#475569" # Subtle highlight
        )
        self.btn_convert.grid(row=9, column=0, padx=25, pady=40, sticky="ew")

        # --- Signature ---
        self.lbl_sig = ctk.CTkLabel(
            self.sidebar, 
            text="Built by Arjun Sarkar", 
            text_color=self.colors["text_dim"], 
            font=("Arial", 10)
        )
        self.lbl_sig.grid(row=11, column=0, pady=20)

    def create_btn(self, text, cmd, row, icon):
        btn = ctk.CTkButton(
            self.sidebar, 
            text=f"  {icon}    {text}", 
            command=cmd,
            fg_color="transparent", 
            hover_color=self.colors["btn_default"],
            text_color=self.colors["text"], 
            anchor="w", 
            height=50, 
            corner_radius=10,
            font=("Arial", 14)
        )
        btn.grid(row=row, column=0, padx=20, pady=4, sticky="ew")

    def update_format_menu(self, value):
        new_values = self.format_categories[value]
        self.format_menu.configure(values=new_values)
        self.format_menu.set(new_values[0])

    def create_main_area(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)
        
        # Header
        self.head = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.head.pack(fill="x", pady=(0, 25))
        
        title_box = ctk.CTkFrame(self.head, fg_color="transparent")
        title_box.pack(side="left")
        
        ctk.CTkLabel(title_box, text="Queue", font=("SF Pro Display", 36, "bold"), text_color=self.colors["text"]).pack(anchor="w")
        ctk.CTkLabel(title_box, text="Drag files here or use the sidebar", font=("Arial", 14), text_color=self.colors["text_dim"]).pack(anchor="w")

        self.lbl_status = ctk.CTkLabel(
            self.head, 
            text="Ready", 
            font=("Arial", 13, "bold"), 
            text_color=self.colors["text"],
            fg_color=self.colors["bg_sidebar"], 
            corner_radius=20, 
            padx=20, 
            pady=8
        )
        self.lbl_status.pack(side="right", anchor="n", pady=10)

        # List Area
        self.scroll_list = ctk.CTkScrollableFrame(
            self.main_frame, 
            fg_color="transparent", # Transparent to show main bg
            corner_radius=0
        )
        self.scroll_list.pack(fill="both", expand=True)
        
        # Hack for custom scrollbar visuals (CTK defaults are okay, but this keeps it clean)
        self.scroll_list._scrollbar.configure(width=0) 

        # Progress Area
        self.progress_frame = ctk.CTkFrame(self.main_frame, fg_color=self.colors["bg_sidebar"], corner_radius=15, height=60)
        self.progress_frame.pack(fill="x", pady=(20, 0))
        self.progress_frame.pack_propagate(False) # Fix height

        self.progress_lbl = ctk.CTkLabel(self.progress_frame, text="Progress", font=("Arial", 12, "bold"), text_color=self.colors["text_dim"])
        self.progress_lbl.pack(side="left", padx=20)
        
        self.progress = ctk.CTkProgressBar(
            self.progress_frame, 
            height=12, 
            corner_radius=6, 
            progress_color=self.colors["accent"], 
            fg_color=self.colors["bg_main"],
            border_width=0
        )
        self.progress.set(0)
        self.progress.pack(side="right", fill="x", expand=True, padx=20)

    # --- Logic ---

    def add_files(self):
        files = filedialog.askopenfilenames()
        for f in files: self.add_item(f)
        self.update_count()

    def add_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            all_valid = self.valid_inputs['image'] + self.valid_inputs['video'] + self.valid_inputs['audio']
            for root, _, files in os.walk(folder):
                for file in files:
                    if Path(file).suffix.lower() in all_valid:
                        self.add_item(os.path.join(root, file))
            self.update_count()

    def add_item(self, filepath):
        if filepath in self.files_to_convert: return
        self.files_to_convert.append(filepath)
        
        # Create Row (Card Style)
        row = ctk.CTkFrame(
            self.scroll_list, 
            fg_color=self.colors["item_bg"], 
            corner_radius=16, 
            height=70,
            border_width=1,
            border_color="#334155"
        )
        row.pack(fill="x", pady=6, padx=5)
        
        # Determine Icon & Color
        ext = Path(filepath).suffix.lower()
        icon, color = "📄", self.colors["text_dim"]
        if ext in self.valid_inputs['audio']: icon, color = "🎵", "#f472b6" # Pink
        elif ext in self.valid_inputs['video']: icon, color = "🎬", "#60a5fa" # Blue
        elif ext in self.valid_inputs['image']: icon, color = "🖼️", "#34d399" # Emerald

        # Icon Box
        icon_box = ctk.CTkFrame(row, width=50, height=50, fg_color=self.colors["bg_main"], corner_radius=12)
        icon_box.pack(side="left", padx=(10, 15), pady=10)
        icon_box.pack_propagate(False)
        ctk.CTkLabel(icon_box, text=icon, font=("Arial", 20)).pack(expand=True)

        # Text Info
        info_box = ctk.CTkFrame(row, fg_color="transparent")
        info_box.pack(side="left", fill="both", expand=True, pady=10)
        
        ctk.CTkLabel(info_box, text=Path(filepath).name, text_color=self.colors["text"], 
                    font=("SF Pro Display", 14, "bold"), anchor="w").pack(fill="x")
        
        ctk.CTkLabel(info_box, text=f"{ext.upper()} File", text_color=self.colors["text_dim"], 
                    font=("Arial", 11), anchor="w").pack(fill="x")
        
        # Delete Button
        btn = ctk.CTkButton(
            row, 
            text="×", 
            width=35, 
            height=35, 
            fg_color="transparent", 
            hover_color=self.colors["error"], 
            text_color=self.colors["text_dim"], 
            font=("Arial", 20), 
            corner_radius=10,
            command=lambda p=filepath: self.remove_item(p)
        )
        btn.pack(side="right", padx=15)
        
        self.file_widgets[filepath] = row

    def remove_item(self, filepath):
        if filepath in self.files_to_convert: self.files_to_convert.remove(filepath)
        if filepath in self.file_widgets:
            self.file_widgets[filepath].destroy()
            del self.file_widgets[filepath]
        self.update_count()

    def clear_list(self):
        self.files_to_convert = []
        self.file_widgets = {}
        for w in self.scroll_list.winfo_children(): w.destroy()
        self.update_count()
        self.progress.set(0)
        self.progress_lbl.configure(text="Progress")

    def update_count(self):
        self.lbl_status.configure(text=f"{len(self.files_to_convert)} Files Ready")

    def start_conversion_thread(self):
        if not self.files_to_convert: return messagebox.showwarning("Empty Queue", "Please add files first.")
        
        out_dir = filedialog.askdirectory()
        if not out_dir: return

        self.btn_convert.configure(state="disabled", text="PROCESSING...", fg_color=self.colors["btn_default"])
        threading.Thread(target=self.convert_process, args=(out_dir,), daemon=True).start()

    def convert_process(self, out_dir):
        mode = self.mode_switch.get()
        fmt = self.format_menu.get().lower()
        
        total = len(self.files_to_convert)
        success = 0
        skipped = 0
        errors = []

        for i, filepath in enumerate(self.files_to_convert):
            self.progress_lbl.configure(text=f"Converting {i+1} of {total}...", text_color=self.colors["accent"])
            
            if filepath in self.file_widgets:
                self.file_widgets[filepath].configure(border_width=2, border_color=self.colors["accent"])

            try:
                ext = Path(filepath).suffix.lower()
                stem = Path(filepath).stem
                out_path = os.path.join(out_dir, f"{stem}.{fmt}")
                
                # --- IMAGE MODE ---
                if mode == "Image":
                    if ext in self.valid_inputs['image']:
                        with Image.open(filepath) as img:
                            if fmt == 'icns':
                                if img.mode != 'RGBA': img = img.convert('RGBA')
                                img = img.resize((1024, 1024), Image.Resampling.LANCZOS)
                                img.save(out_path, format='ICNS')
                            else:
                                if fmt in ['jpeg', 'jpg', 'bmp'] and img.mode in ('RGBA', 'LA'):
                                    img = img.convert('RGB')
                                img.save(out_path, quality=95)
                        success += 1
                        self.mark_row(filepath, "success")
                    else:
                        skipped += 1
                        self.mark_row(filepath, "warning")

                # --- VIDEO MODE ---
                elif mode == "Video":
                    if ext in self.valid_inputs['video']:
                        clip = VideoFileClip(filepath)
                        if fmt == 'gif':
                            clip.write_gif(out_path, verbose=False, logger=None)
                        else:
                            codec = 'libvpx' if fmt == 'webm' else 'libx264'
                            clip.write_videofile(out_path, codec=codec, audio_codec='aac', verbose=False, logger=None)
                        clip.close()
                        success += 1
                        self.mark_row(filepath, "success")
                    else:
                        skipped += 1
                        self.mark_row(filepath, "warning")

                # --- AUDIO MODE ---
                elif mode == "Audio":
                    if ext in self.valid_inputs['audio'] or ext in self.valid_inputs['video']:
                        clip = AudioFileClip(filepath)
                        clip.write_audiofile(out_path, verbose=False, logger=None)
                        clip.close()
                        success += 1
                        self.mark_row(filepath, "success")
                    else:
                        skipped += 1
                        self.mark_row(filepath, "warning")

            except Exception as e:
                errors.append(f"{stem}: {e}")
                self.mark_row(filepath, "error")

            self.progress.set((i + 1) / total)

        self.after(0, lambda: self.finish(success, skipped, errors))

    def mark_row(self, filepath, status):
        if filepath in self.file_widgets:
            color = self.colors.get(status, self.colors["item_bg"])
            try: 
                # If success/error, fill the card slightly
                if status == "success":
                    self.file_widgets[filepath].configure(border_color=self.colors["success"], border_width=2)
                elif status == "error":
                    self.file_widgets[filepath].configure(border_color=self.colors["error"], border_width=2)
                elif status == "warning":
                    self.file_widgets[filepath].configure(border_color=self.colors["warning"], border_width=2)
            except: pass

    def finish(self, success, skipped, errors):
        self.btn_convert.configure(state="normal", text="START CONVERSION", fg_color=self.colors["accent"])
        self.progress_lbl.configure(text="Completed", text_color=self.colors["success"])
        self.lbl_status.configure(text="All Done")
        
        msg = f"Completed: {success}"
        if skipped > 0: msg += f"\nSkipped: {skipped} (Incompatible)"
        if errors: msg += f"\nErrors: {len(errors)}"
        
        messagebox.showinfo("Report", msg)

if __name__ == "__main__":
    app = MacConverterPro()
    app.mainloop()