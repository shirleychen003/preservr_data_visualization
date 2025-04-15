import os
import sys
import threading
import subprocess
from tkinter import Tk, Toplevel, Label, Frame, Button, filedialog
from tkinter import ttk
from PIL import Image, ImageTk

# Define default fonts and colors
DEFAULT_FONT = ("apple-system", 12)
TITLE_FONT = ("apple-system", 20, "bold")
BG_COLOR = "#f9f9f9"
CARD_BG = "white"
BORDER_COLOR = "#d1d1d1"

class InstagramArchiveApp(Tk):
    """Main application class for Instagram Archive Visual Analysis Tool."""
    
    def __init__(self):
        """Initialize the application window and setup basic configurations."""
        super().__init__()
        self.title("Preservr - Archive Visual Analysis Tool (Instagram)")
        self.configure(bg=BG_COLOR)
        self.geometry("1000x850")
        self.center_window(1000, 850)
        
        # Configure main grid to have two columns; we use rows 0, 1, 2.
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        self.folder_selected = None
        self.json_files = {}
        self.image_label = None

        self.create_widgets()

    def center_window(self, width, height):
        """Center the application window on the screen based on provided dimensions."""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_position = (screen_width - width) // 2
        y_position = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x_position}+{y_position}")

    def create_widgets(self):
        """Create and arrange all UI widgets in the application."""
        # Row 0: Title Label (centered across two columns)
        self.title_label = Label(self, text="Instagram Archive Visual Analysis Tool", font=TITLE_FONT,
                                 bg=BG_COLOR, fg="#333333")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))
        
        # Row 1: Image Display Area (centered; fixed dimensions)
        self.image_frame = Frame(self, width=800, height=500, bg=CARD_BG,
                                 highlightbackground=BORDER_COLOR, highlightthickness=1)
        self.image_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=10)
        self.image_frame.grid_propagate(False)
        
        # Spinner / Progress Indicator using ttk.Progressbar
        self.spinner = ttk.Progressbar(self.image_frame, mode="indeterminate")
        
        # Row 2: Bottom frame containing File Select info and Script Buttons.
        bottom_frame = Frame(self, bg=BG_COLOR)
        bottom_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10)
        # Configure two columns in bottom_frame.
        bottom_frame.grid_columnconfigure(0, weight=1)  # Left: file select and folder label
        bottom_frame.grid_columnconfigure(1, weight=1)  # Right: script buttons

        # Left subframe: File selection
        file_info_frame = Frame(bottom_frame, bg=BG_COLOR)
        file_info_frame.grid(row=0, column=0, padx=(0,10))
        # Button to select folder.
        self.btn_select = Button(file_info_frame, text="Select Folder", command=self.select_folder,
                                 font=DEFAULT_FONT)
        self.btn_select.pack(anchor="w", padx=5, pady=(0,5))
        # Label to display the selected folder info.
        self.folder_label = Label(file_info_frame, text="No folder selected", font=DEFAULT_FONT,
                                  bg=BG_COLOR, anchor="w", justify="left", wraplength=400)
        self.folder_label.pack(anchor="w", padx=5)

        # Right subframe: Script buttons arranged in a 3x2 grid.
        button_frame = Frame(bottom_frame, bg=BG_COLOR)
        button_frame.grid(row=0, column=1, sticky="ne", padx=(10,0))
        
        # Get the directory for scripts based on this file's location.
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        self.script_names = {
            "Most Liked Users (Stories)": os.path.join(parent_dir, "core", "most_liked_users_stories.py"),
            "Most Liked Users (Posts)": os.path.join(parent_dir, "core", "most_liked_users_posts.py"),
            "Most Liked Users (Top 5)": os.path.join(parent_dir, "core", "most_liked_users.py"),
            "Top Post Topics": os.path.join(parent_dir, "core", "top_topics.py"),
            "Follower Age/Gender Distribution": os.path.join(parent_dir, "core", "age_gender_distribution.py"),
            "Followers/Following Analysis": os.path.join(parent_dir, "core", "followers_following.py"),
            
        }

        # Create button grid 
        self.script_buttons = {}
        row_idx, col_idx = 0, 0
        for text, script in self.script_names.items():
            btn = Button(button_frame, text=text, command=lambda s=script: self.run_script(s),
                 font=DEFAULT_FONT)
            btn.grid(row=row_idx, column=col_idx, padx=5, pady=5, sticky="nsew")
            self.script_buttons[text] = btn
            row_idx += 1
            if row_idx >= 3:
                row_idx = 0
                col_idx += 1

        # Ensure the rows in the button frame expand evenly.
        for i in range(3):
            button_frame.grid_rowconfigure(i, weight=1)
        # Ensure the columns in the button frame expand evenly.
        for i in range(2):
            button_frame.grid_columnconfigure(i, weight=1)

    def select_folder(self):
        """Open a dialog for user to select Instagram archive folder and initialize file searching."""
        folder = filedialog.askdirectory()
        if folder:
            self.folder_selected = folder
            self.json_files = self._initialize_json_files()
            self._find_json_files()
            self._update_folder_display()

    def _initialize_json_files(self):
        """Initialize empty dictionary for tracking required JSON files in the archive."""
        return {
            'liked_posts': None,
            'post_comments': None,
            'recommended_topics': None,
            'story_likes': None,
            'audience_insights': None,
            'followers_1': None,
            'following': None
        }

    def _find_json_files(self):
        """Search through selected folder to locate required JSON files."""
        if not self.folder_selected:
            return
        file_mapping = {
            'liked_posts.json': 'liked_posts',
            'recommended_topics.json': 'recommended_topics',
            'story_likes.json': 'story_likes',
            'audience_insights.json': 'audience_insights',
            'followers_1.json': 'followers_1',
            'following.json': 'following'
        }

        # Recursive search
        for root_dir, _, files in os.walk(self.folder_selected):
            for file in files:
                if file in file_mapping and self.json_files[file_mapping[file]] is None:
                    self.json_files[file_mapping[file]] = os.path.join(root_dir, file)

    def _update_folder_display(self):
        """Update the UI to show which required files were found in the selected folder."""
        
        # Build file status lines.
        file_status_lines = []
        
        for key, path in self.json_files.items():
            if key == 'post_comments':  # Skip as before.
                continue
            # Use simple checkmark characters.
            status = "\u2713" if path is not None else "\u2717"
            display_name = f"{key}.json"
            file_status_lines.append(f"{status} {display_name}")
        
        # Show only the basename of the folder to avoid overly long text.
        folder_display = os.path.basename(self.folder_selected) if self.folder_selected else "No folder selected"
        status_text = f"Selected Folder: {folder_display}\n" + "\n".join(file_status_lines)
        self.folder_label.config(text=status_text)

    def run_script(self, script_path):
        """Execute the selected analysis script in a separate thread and handle the UI feedback."""
        if not self.folder_selected:
            self.show_directory_prompt()
            return

        script_name_only = os.path.basename(script_path)
        
        # Check if required files exist before running the script
        if not self.check_required_files(script_name_only):
            return
            
        # Mapping from script filenames to expected output image names.
        
        output_images = {
            "most_liked_users_stories.py": "story_likes_visualization.png",
            "most_liked_users_posts.py": "liked_posts_wordcloud.png",
            "top_topics.py": "top_topics.png",
            "age_gender_distribution.py": "age_gender_distribution.png",
            "most_liked_users.py": "most_liked_users_barchart.png",
        }

        # Show spinner in the image frame and disable script buttons.
        self.spinner.place(relx=0.5, rely=0.5, anchor="center")
        self.spinner.start()
        for btn in self.script_buttons.values():
            btn.config(state="disabled")

        # Run the selected script in a separate thread.
        threading.Thread(target=self._run_script_thread,
                         args=(script_path, script_name_only, output_images),
                         daemon=True).start()

    def check_required_files(self, script_name):
        """Check if the required JSON files exist for a specific script."""
        # Map scripts to their required JSON files
        required_files_map = {
            "most_liked_users_stories.py": ["story_likes"],
            "most_liked_users_posts.py": ["liked_posts"],
            "top_topics.py": ["recommended_topics"],
            "age_gender_distribution.py": ["audience_insights"],
            "most_liked_users.py": ["liked_posts"],
            "followers_following.py": ["followers_1", "following"]
        }
        
        required_keys = required_files_map.get(script_name, [])
        missing_files = []
        
        for key in required_keys:
            if not self.json_files.get(key):
                missing_files.append(f"{key}.json")
        
        if missing_files:
            self.show_missing_files_error(script_name, missing_files)
            return False
            
        return True
        
    def show_missing_files_error(self, script_name, missing_files):
        """Display an error window showing which required files are missing."""
        error_window = Toplevel(self)
        error_window.title("Missing Required Files")
        error_window.configure(bg=BG_COLOR)
        error_window.geometry("500x250")
        
        # Make the window modal
        error_window.transient(self)
        error_window.grab_set()
        
        # Center the window
        screen_width = error_window.winfo_screenwidth()
        screen_height = error_window.winfo_screenheight()
        x_position = (screen_width - 500) // 2
        y_position = (screen_height - 250) // 2
        error_window.geometry(f"500x250+{x_position}+{y_position}")
        
        # Script name display (remove .py extension for cleaner display)
        script_display = script_name.replace(".py", "").replace("_", " ").title()
        
        # Create message
        message = f"Cannot run {script_display}.\n\nThe following required files were not found in your Instagram archive:\n\n"
        message += "\n".join([f"• {file}" for file in missing_files])
        message += "\n\nPlease select a folder containing these files."
        
        Label(error_window, text=message, font=DEFAULT_FONT, bg=BG_COLOR, 
              justify="left", wraplength=450, pady=20).pack(expand=True)
        
        # Add button to close the window
        Button(error_window, text="OK", font=DEFAULT_FONT,
               command=error_window.destroy, width=10).pack(pady=15)
               
    def _run_script_thread(self, script_path, script_name_only, output_images):
        """Background thread function that runs the selected script and handles its output."""
        try:
            subprocess.run([sys.executable, script_path, self.folder_selected], check=True)
            if script_name_only == "followers_following.py":
                txt_path = os.path.join(self.folder_selected, "OUTPUT_FOLDER", "follow_analysis.txt")
                if not os.path.exists(txt_path):
                    self.show_error("Analysis script ran but no output file was found.")
                else:
                    # Show instructions window for follow analysis
                    self.after(0, self.show_follow_analysis_instructions)
            else:
                output_image_name = output_images.get(script_name_only)
                if output_image_name:
                    output_image_path = os.path.join(self.folder_selected, "OUTPUT_FOLDER", output_image_name)
                    if os.path.exists(output_image_path):
                        self.after(0, lambda: self.display_visualization(output_image_path))
                    else:
                        self.show_warning("Visualization file not found in selected folder.")
        except subprocess.CalledProcessError as e:
            self.show_error(f"Error executing {script_name_only}: {e}")
        finally:
            self.after(0, self._finish_script_run)

    def show_directory_prompt(self):
        """Display a window prompting the user to specify a directory."""
        prompt_window = Toplevel(self)
        prompt_window.title("Select Directory")
        prompt_window.configure(bg=BG_COLOR)
        prompt_window.geometry("450x200")
        
        # Make the window modal
        prompt_window.transient(self)
        prompt_window.grab_set()
        
        # Center the window
        screen_width = prompt_window.winfo_screenwidth()
        screen_height = prompt_window.winfo_screenheight()
        x_position = (screen_width - 450) // 2
        y_position = (screen_height - 200) // 2
        prompt_window.geometry(f"450x200+{x_position}+{y_position}")
        
        # Add message
        message = "Please select an Instagram archive folder before running any analysis."
        Label(prompt_window, text=message, font=DEFAULT_FONT, bg=BG_COLOR, 
              justify="center", wraplength=400, pady=20).pack(expand=True)
        
        # Create button frame
        button_frame = Frame(prompt_window, bg=BG_COLOR)
        button_frame.pack(pady=15)
        
        # Add button to close the window
        Button(button_frame, text="OK", font=DEFAULT_FONT,
               command=prompt_window.destroy, width=10).pack(side="left", padx=10)
        
        # Add button to select folder directly
        def select_and_close():
            prompt_window.destroy()
            self.select_folder()
            
        Button(button_frame, text="Select Folder", font=DEFAULT_FONT,
               command=select_and_close, width=15).pack(side="left", padx=10)
        
        # Wait for the window to be closed
        self.wait_window(prompt_window)

    def show_follow_analysis_instructions(self):
        """Display a window with instructions to open the OUTPUT_FOLDER."""
        instruction_window = Toplevel(self)
        instruction_window.title("Followers/Following Analysis")
        instruction_window.configure(bg=BG_COLOR)
        instruction_window.geometry("500x250")
        
        # Center the window on the screen
        screen_width = instruction_window.winfo_screenwidth()
        screen_height = instruction_window.winfo_screenheight()
        x_position = (screen_width - 500) // 2
        y_position = (screen_height - 250) // 2
        instruction_window.geometry(f"500x250+{x_position}+{y_position}")
        
        # Add instructions
        message = (
            "The Followers/Following Analysis is complete!\n\n"
            "Please open the 'OUTPUT_FOLDER' in your selected archive folder to view the follow_analysis.txt file with your results."
        )
        
        Label(instruction_window, text=message, font=DEFAULT_FONT, bg=BG_COLOR, 
              justify="center", wraplength=450, pady=20).pack(expand=True)
        
        output_path = os.path.join(self.folder_selected, "OUTPUT_FOLDER")
        
        # Create button frame to hold the buttons side by side
        button_frame = Frame(instruction_window, bg=BG_COLOR)
        button_frame.pack(pady=15)
        
        # Add button to close the window
        Button(button_frame, text="OK", font=DEFAULT_FONT,
               command=instruction_window.destroy, width=10).pack(side="left", padx=10)
        
        # Add button to open output folder if available
        if os.path.exists(output_path):
            Button(button_frame, text="Open Folder", font=DEFAULT_FONT,
               command=lambda: os.startfile(output_path), width=10).pack(side="left", padx=10)

    def _finish_script_run(self):
        """Stop spinner animation and re-enable buttons after script execution completes."""
        self.spinner.stop()
        self.spinner.place_forget()
        for btn in self.script_buttons.values():
            btn.config(state="normal")

    def display_visualization(self, image_path):
        """Load and display the visualization image produced by an analysis script."""
        try:
            img = Image.open(image_path)
            img = img.resize((800, 500), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            if self.image_label is not None:
                self.image_label.destroy()
            self.image_label = Label(self.image_frame, image=photo, bg=CARD_BG)
            self.image_label.image = photo  # keep a reference
            self.image_label.place(rely=0.5, relx=0.5, anchor="center")
        except Exception as e:
            self.show_error(f"Could not load visualization: {e}")

    def show_error(self, message):
        """Display an error message to the user."""
        error_window = Toplevel(self)
        error_window.title("Error")
        error_window.configure(bg=BG_COLOR)
        error_window.geometry("450x200")
        
        # Make the window modal
        error_window.transient(self)
        error_window.grab_set()
        
        # Center the window
        screen_width = error_window.winfo_screenwidth()
        screen_height = error_window.winfo_screenheight()
        x_position = (screen_width - 450) // 2
        y_position = (screen_height - 200) // 2
        error_window.geometry(f"450x200+{x_position}+{y_position}")
        
        Label(error_window, text=message, font=DEFAULT_FONT, bg=BG_COLOR, 
              justify="center", wraplength=400, pady=20).pack(expand=True)
        
        Button(error_window, text="OK", font=DEFAULT_FONT,
               command=error_window.destroy, width=10).pack(pady=15)

    def show_warning(self, message):
        """Display a warning message to the user."""
        warning_window = Toplevel(self)
        warning_window.title("Warning")
        warning_window.configure(bg=BG_COLOR)
        warning_window.geometry("450x200")
        
        # Make the window modal
        warning_window.transient(self)
        warning_window.grab_set()
        
        # Center the window
        screen_width = warning_window.winfo_screenwidth()
        screen_height = warning_window.winfo_screenheight()
        x_position = (screen_width - 450) // 2
        y_position = (screen_height - 200) // 2
        warning_window.geometry(f"450x200+{x_position}+{y_position}")
        
        Label(warning_window, text=message, font=DEFAULT_FONT, bg=BG_COLOR, 
              justify="center", wraplength=400, pady=20).pack(expand=True)
        
        Button(warning_window, text="OK", font=DEFAULT_FONT,
               command=warning_window.destroy, width=10).pack(pady=15)