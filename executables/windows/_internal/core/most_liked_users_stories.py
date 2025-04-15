"""
DEPRECATED: Preservr Data Visualizations - Story Likes

Author: Shirley Chen
Description: This module provides visualization tools for analyzing and displaying
             story likes data for the Preservr project. It processes story likes datasets
             and generates a word cloud to visualize which users had interacted most with
             the user's stories.
Input: Liked posts data files stored in the 'data' directory
Output: Visualization files saved to the 'OUTPUT_FOLDER' directory
Date: 2025-04-16
"""

import os
import sys
import json
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

def find_file_in_subdirectories(folder_path, filename):
    """
    Recursively search for the specified file in subdirectories.
    """
    for root, _, files in os.walk(folder_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

def generate_story_likes_wordcloud(folder_path):
    """
    Generate a word cloud visualization based on story likes data.
    Saves the output image to an OUTPUT_FOLDER inside the provided folder_path.
    """
    input_path = find_file_in_subdirectories(folder_path, "story_likes.json")
    if input_path is None:
        print(f"Error: story_likes.json not found in {folder_path} or its subdirectories")
        return

    # Create or access OUTPUT_FOLDER
    output_folder = os.path.join(folder_path, "OUTPUT_FOLDER")
    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, "story_likes_visualization.png")

    # Load JSON data
    with open(input_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Extract liked story titles
    likes = [entry["title"] for entry in data.get("story_activities_story_likes", [])]

    # Count occurrences of each user/title
    like_counts = Counter(likes)

    if not like_counts:
        print("No story likes data found.")
        return

    # Get most active liker
    most_active_liker, max_likes = like_counts.most_common(1)[0]

    # Generate Word Cloud
    wc = WordCloud(
        width=800,
        height=500,
        background_color="white",
        colormap="coolwarm"
    ).generate_from_frequencies(like_counts)

    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Most Liked Users (Stories)")

    # Save to OUTPUT_FOLDER
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Visualization saved to: {output_path}")

# Entry point for CLI usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python story_likes_visualization.py <folder_path>")
        sys.exit(1)

    folder = sys.argv[1]
    generate_story_likes_wordcloud(folder)
