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

            file_status = []
            self.json_files = {
                'liked_posts': None,
                'post_comments': None,
                'recommended_topics': None,
                'story_likes': None,
                'audience_insights': None,
                'followers_1': None,
                'following': None
            }

            # Recursive search for required JSON files
            for root_dir, _, files in os.walk(self.folder_selected):
                for file in files:
                    if file == "liked_posts.json" and self.json_files['liked_posts'] is None:
                        self.json_files['liked_posts'] = os.path.join(root_dir, file)
                        file_status.append("✅ liked_posts.json found")
                    elif file == "post_comments_1.json" and self.json_files['post_comments'] is None:
                        self.json_files['post_comments'] = os.path.join(root_dir, file)
                        file_status.append("✅ post_comments_1.json found")
                    elif file == "recommended_topics.json" and self.json_files['recommended_topics'] is None:
                        self.json_files['recommended_topics'] = os.path.join(root_dir, file)
                        file_status.append("✅ recommended_topics.json found")
                    elif file == "story_likes.json" and self.json_files['story_likes'] is None:
                        self.json_files['story_likes'] = os.path.join(root_dir, file)
                        file_status.append("✅ story_likes.json found")
                    elif file == "audience_insights.json" and self.json_files['audience_insights'] is None:
                        self.json_files['audience_insights'] = os.path.join(root_dir, file)
                        file_status.append("✅ audience_insights.json found")
                    elif file == "followers_1.json" and self.json_files['followers_1'] is None:
                        self.json_files['followers_1'] = os.path.join(root_dir, file)
                        file_status.append("✅ followers_1.json found")
                    elif file == "following.json" and self.json_files['following'] is None:
                        self.json_files['following'] = os.path.join(root_dir, file)
                        file_status.append("✅ following.json found")

            # For any files still not found, add missing status
            if self.json_files['liked_posts'] is None:
                file_status.append("❌ liked_posts.json not found")
            if self.json_files['post_comments'] is None:
                file_status.append("❌ post_comments_1.json not found")
            if self.json_files['recommended_topics'] is None:
                file_status.append("❌ recommended_topics.json not found")
            if self.json_files['story_likes'] is None:
                file_status.append("❌ story_likes.json not found")
            if self.json_files['audience_insights'] is None:
                file_status.append("❌ story_likes.json not found")
            if self.json_files['followers_1'] is None:
                file_status.append("❌ followers_1.json not found")
            if self.json_files['following'] is None:
                file_status.append("❌ following.json not found")

            status_text = f"Selected Folder: {self.folder_selected}\n" + "\n".join(file_status)
            self.label.config(text=status_text)

    def create_script_buttons(self):
        # Get the directory containing the UI script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)

        script_names = {
            "Story Likes": os.path.join(parent_dir, "core", "most_liked_users_stories.py"),
            "Liked Posts": os.path.join(parent_dir, "core", "most_liked_users_posts.py"),
            "Word Cloud Topics": os.path.join(parent_dir, "core", "top_topics.py"),
            "Most Commented On Users": os.path.join(parent_dir, "core", "most_commented_on_users.py"),
            "Age and Gender Distribution": os.path.join(parent_dir, "core", "age_gender_distribution.py"),
            "Followers and Following Analysis": os.path.join(parent_dir, "core", "followers_following.py"),
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

        # Get the directory containing the UI script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)

        # Output visualizations mapping
        output_images = {
            "most_liked_users_stories.py": "story_likes_visualization.png",
            "most_liked_users_posts.py": "liked_posts_wordcloud.png",
            "top_topics.py": "top_topics.png",
            "most_commented_on_users.py": "post_comments.png",
            "age_gender_distribution.py": "age_gender_distribution.png",
        }

        try:
            subprocess.run([sys.executable, script_name, self.folder_selected], check=True)
            script_name_only = os.path.basename(script_name)

            if script_name_only == "followers_following.py":
                # Inform about the text output
                txt_path = os.path.join(self.folder_selected, "follow_analysis.txt")
                if os.path.exists(txt_path):
                    messagebox.showinfo(
                        "Analysis Complete",
                        f"✅ Follower/Following analysis complete!\n\n📄 Output saved to:\n{txt_path}"
                    )
                else:
                    messagebox.showwarning("Warning", "Analysis script ran but no output file was found.")
            else:
                # Handle image display if the script has a visualization output
                output_image_name = output_images.get(script_name_only)
                if output_image_name:
                    output_image_path = os.path.join(self.folder_selected, output_image_name)
                    if os.path.exists(output_image_path):
                        self.display_visualization(output_image_path)
                    else:
                        messagebox.showwarning("Warning", "Visualization file not found in selected folder")

                messagebox.showinfo("Success", f"Executed {script_name_only} successfully!")

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
