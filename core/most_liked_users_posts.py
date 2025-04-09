import json
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import sys
import os

titles = []
title_counts = None


def find_file_in_subdirectories(folder_path, filename):
    """
    Recursively search for the specified file in subdirectories.
    """
    for root, dirs, files in os.walk(folder_path):
        if filename in files:
            return os.path.join(root, filename)
    return None


def most_liked_wordcloud(folder_path):
    """
    Create a wordcloud showing the number of likes per title (media owner).
    Saves output image to OUTPUT_FOLDER.
    """
    global title_counts

    # Create a dictionary of titles and their like counts
    wordcloud_data = dict(zip(title_counts["Title"], title_counts["Like Count"]))

    # Generate the wordcloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcloud_data)

    # Plot the wordcloud
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("Accounts You Liked Most")
    plt.tight_layout()

    # Define the output path inside OUTPUT_FOLDER
    output_folder = os.path.join(folder_path, "OUTPUT_FOLDER")
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "liked_posts_wordcloud.png")

    # Save as PNG
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Visualization saved to: {output_path}")
    plt.close()


def load_data(folder_path):
    """
    Load the liked posts data from the JSON file in the specified folder.
    """
    global titles, title_counts

    liked_posts_path = find_file_in_subdirectories(folder_path, "liked_posts.json")

    if liked_posts_path is None:
        print(f"Error: Could not find liked_posts.json in {folder_path} or its subdirectories")
        return

    with open(liked_posts_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    media_titles = []
    for item in data.get("likes_media_likes", []):
        try:
            title = item.get("title", "Unknown")
            if title:
                media_titles.append(title)
        except (KeyError, TypeError):
            continue

    df = pd.DataFrame({"Title": media_titles})
    title_counts = df["Title"].value_counts().reset_index()
    title_counts.columns = ["Title", "Like Count"]
    titles = df

    # Remove unknown entries
    title_counts = title_counts[title_counts["Title"] != "Unknown"]


def main():
    if len(sys.argv) < 2:
        print("Usage: python liked_posts.py <folder_path>")
        sys.exit(1)

    folder = sys.argv[1]
    load_data(folder)
    most_liked_wordcloud(folder)


if __name__ == "__main__":
    main()
