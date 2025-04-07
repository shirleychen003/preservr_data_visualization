import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import sys
from PIL import Image, ImageTk
import os

class InstagramArchiveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualize Your Instagram Archive!")
        self.root.geometry("1000x850")
        self.root.configure(bg="#2e2e2e")

        self.center_window(1000, 850)
        self.folder_selected = None
        self.json_files = {}

        # Create an initial white window to display the image
        self.image_frame = tk.Frame(self.root, width=800, height=500, bg="white")
        self.image_frame.pack(pady=20)
        self.image_label = None

        # Button to select folder
        self.btn_select = tk.Button(self.root, text="Select Folder", command=self.select_folder)
        self.btn_select.pack(pady=20)

        # Label for the selected folder
        self.label = tk.Label(self.root, text="No folder selected", wraplength=350, bg="#2e2e2e", fg="white")
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

            # Check for required JSON files
            file_status = []

            # Look for liked_posts.json
            liked_posts_path = os.path.join(self.folder_selected, "liked_posts.json")
            if os.path.exists(liked_posts_path):
                self.json_files['liked_posts'] = liked_posts_path
                file_status.append("✅ liked_posts.json found")
            else:
                self.json_files['liked_posts'] = None
                file_status.append("❌ liked_posts.json not found")

            # Look for post_comments_1.json
            post_comments_path = os.path.join(self.folder_selected, "post_comments_1.json")
            if os.path.exists(post_comments_path):
                self.json_files['post_comments'] = post_comments_path
                file_status.append("✅ post_comments_1.json found")
            else:
                self.json_files['post_comments'] = None
                file_status.append("❌ post_comments_1.json not found")

            # Look for recommended_topics.json
            recommended_topics_path = os.path.join(self.folder_selected, "recommended_topics.json")
            if os.path.exists(recommended_topics_path):
                self.json_files['recommended_topics'] = recommended_topics_path
                file_status.append("✅ recommended_topics.json found")
            else:
                self.json_files['recommended_topics'] = None
                file_status.append("❌ recommended_topics.json not found")

            # Look for story_likes.json
            story_likes_path = os.path.join(self.folder_selected, "story_likes.json")
            if os.path.exists(story_likes_path):
                self.json_files['story_likes'] = story_likes_path
                file_status.append("✅ story_likes.json found")
            else:
                self.json_files['story_likes'] = None
                file_status.append("❌ story_likes.json not found")

            # Update the label with folder path and file statuses
            status_text = f"Selected Folder: {self.folder_selected}\n" + "\n".join(file_status)
            self.label.config(text=status_text)

    def create_script_buttons(self):
        script_names = {
            "Run Story Likes": "../core/story_likes.py",
            "Run Liked Posts": "../core/liked_posts.py",
            "Run Word Cloud Topics": "../core/top_topics.py",
            "Run Most Commented On Users": "../core/most_commented_on_users.py",
        }

        button_frame = tk.Frame(self.root, bg="#2e2e2e")
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
            "../core/story_likes.py": "../images/story_likes_visualization.png",
            "../core/liked_posts.py": "../images/liked_posts_wordcloud.png",
            "../core/top_topics.py": "../images/top_topics.png",
            "../core/post_comments_1.py": "../images/post_comments.png",
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
            img = img.resize((800, 500), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)

            if self.image_label is not None:
                self.image_label.destroy()

            self.image_label = tk.Label(self.image_frame, image=img, bg="white")
            self.image_label.image = img
            self.image_label.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load visualization: {e}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramArchiveApp(root)
    root.mainloop()
