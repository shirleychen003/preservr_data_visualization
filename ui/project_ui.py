import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import sys
from PIL import Image, ImageTk

class InstagramArchiveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualize Your Instagram Archive!")
        self.root.geometry("1000x750")
        self.root.configure(bg="#2E2E2E")

        self.center_window(1000, 750)
        self.folder_selected = None

        self.btn_select = tk.Button(self.root, text="Select Folder", command=self.select_folder)
        self.btn_select.pack(pady=20)

        # Create an initial white window to display the image
        self.image_frame = tk.Frame(self.root, width=800, height=500, bg="white")
        self.image_frame.pack(pady=20)

        # Label for the selected folder
        self.label = tk.Label(self.root, text="No folder selected", wraplength=350, bg="#2E2E2E", fg="white")
        self.label.pack(pady=10)

        # Buttons to run scripts
        self.create_script_buttons()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width - width) // 2
        y_position = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x_position}+{y_position}")

    def select_folder(self):
        self.folder_selected = filedialog.askdirectory()
        if self.folder_selected:
            self.label.config(text=f"Selected Folder: {self.folder_selected}")

    def create_script_buttons(self):
        script_names = {
            "Run Story Likes": "../to_refactor/story_likes_visualizations.py",
            "Run Liked Posts": "../to_refactor/liked_posts.py",
            "Run Word Cloud Topics": "../to_refactor/wordcloud_topics.py",
        }

        button_frame = tk.Frame(self.root, bg="#2E2E2E")
        button_frame.pack(pady=10)

        for text, script in script_names.items():
            btn = tk.Button(button_frame, text=text, command=lambda s=script: self.run_script(s))
            btn.pack(side=tk.LEFT, padx=5, pady=5)

    def run_script(self, script_name):
        if not self.folder_selected:
            messagebox.showwarning("Warning", "Please select a folder first.")
            return

        # Mapping of scripts to their output image
        output_images = {
            "../to_refactor/story_likes_visualizations.py": "../images/story_likes_visualization.png",
            "../to_refactor/liked_posts.py": "../images/liked_posts_wordcloud.png",
            "../to_refactor/wordcloud_topics.py": "../images/wordcloud_topics.png",
        }

        try:
            subprocess.run([sys.executable, script_name, self.folder_selected], check=True)
            messagebox.showinfo("Success", f"Executed {script_name} successfully!")
            self.display_visualization(output_images.get(script_name, ""))
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error executing {script_name}: {e}")

    def display_visualization(self, image_path):
        try:
            img = Image.open(image_path)
            img = img.resize((800, 400), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)

            label = tk.Label(self.image_frame, image=img, bg="white")
            label.image = img
            label.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load visualization: {e}")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramArchiveApp(root)
    root.mainloop()
