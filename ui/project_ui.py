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
        self.root.geometry("1000x0")
        self.root.configure(bg="#2E2E2E")

        self.center_window(1000, 750)
        self.folder_selected = None
        self.json_files = {
            'liked_posts': None,
            'post_comments': None,
            'recommended_topics': None,
            'story_likes': None
        }

        self.btn_select = tk.Button(self.root, text="Select Folder", command=self.select_folder)
        self.btn_select.pack(pady=20)

        # Create an initial white window to display the image
        self.image_frame = tk.Frame(self.root, width=800, height=500, bg="white")
        self.image_frame.pack(pady=20)

        # Label for the selected folder and files
        self.label = tk.Label(self.root, text="No folder selected", wraplength=700, bg="#2E2E2E", fg="white")
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
        # Get the absolute path to the core directory
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "core"))
        
        script_names = {
            "Most Liked Users (Stories)": {
                "script": os.path.join(base_dir, "story_likes.py"),
                "required_file": "story_likes",
                "output_image": "story_likes_visualization.png"
            },
            "Most Commented On Users": {
                "script": os.path.join(base_dir, "most_commented_on_users.py"),
                "required_file": "post_comments",  # Uses post_comments_1.json
                "output_image": "media_owner_wordcloud.png"
            },
            "Most Liked Users (Posts)": {
                "script": os.path.join(base_dir, "liked_posts.py"),
                "required_file": "liked_posts",
                "output_image": "liked_posts_visualization.png"
            },
            "Top Topics": {
                "script": os.path.join(base_dir, "top_topics.py"),
                "required_file": "recommended_topics",
                "output_image": "wordcloud_topics.png"
            },
        }
    
        button_frame = tk.Frame(self.root, bg="#2E2E2E")
        button_frame.pack(pady=10)
    
        for text, info in script_names.items():
            btn = tk.Button(button_frame, text=text, command=lambda info=info: self.run_script(info))
            btn.pack(side=tk.LEFT, padx=5, pady=5)

    def run_script(self, script_info):
        if not self.folder_selected:
            messagebox.showwarning("Warning", "Please select a folder first.")
            return
            
        # Check if the required file is available
        if script_info["required_file"] and not self.json_files[script_info["required_file"]]:
            messagebox.showwarning(
                "Missing File", 
                f"Required file ({script_info['required_file']}.json) was not found in the selected folder."
            )
            return
            
        try:
            # Clear previous visualization
            for widget in self.image_frame.winfo_children():
                widget.destroy()
                
            # Build command with file paths
            cmd = [sys.executable, script_info["script"]]
            
            # Add all available JSON files as arguments
            for file_key, file_path in self.json_files.items():
                if file_path:
                    cmd.extend([f"--{file_key.replace('_', '-')}", file_path])
            
            # Run the script
            subprocess.run(cmd, check=True)
            
            # Display the visualization
            image_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
            self.display_visualization(os.path.join(image_dir, script_info["output_image"]))
            
            messagebox.showinfo("Success", f"Analysis completed successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error executing script: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def display_visualization(self, image_path):
        try:
            img = Image.open(image_path)
            
            # Calculate resize dimensions while maintaining aspect ratio
            img_width, img_height = img.size
            frame_width, frame_height = 800, 400
            
            # Resize while maintaining aspect ratio
            if img_width > frame_width or img_height > frame_height:
                ratio = min(frame_width/img_width, frame_height/img_height)
                new_width = int(img_width * ratio)
                new_height = int(img_height * ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)
            
            img_tk = ImageTk.PhotoImage(img)
            label = tk.Label(self.image_frame, image=img_tk, bg="white")
            label.image = img_tk  # Keep a reference to prevent garbage collection
            label.pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load visualization: {e}")
            label = tk.Label(self.image_frame, text=f"Visualization not found: {os.path.basename(image_path)}", bg="white")
            label.pack(pady=10)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramArchiveApp(root)
    root.mainloop()
