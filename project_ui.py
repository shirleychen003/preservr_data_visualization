import tkinter as tk
from tkinter import filedialog

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        label.config(text=f"Selected Folder: {folder_selected}")

# Create main window
root = tk.Tk()
root.title("Visualize Your Instagram Archive!")
root.geometry("1000x750")
root.configure(bg="#2E2E2E")

# Center the window on the screen
root.update_idletasks()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 1000
window_height = 750
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create button to open file dialog
btn_select = tk.Button(root, text="Select Folder", command=select_folder)
btn_select.pack(pady=20)

# Label to display selected folder
label = tk.Label(root, text="No folder selected", wraplength=350)
label.pack(pady=10)

# Run the application
root.mainloop()
