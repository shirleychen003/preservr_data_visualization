"""
Preservr Data Visualizations - Story Likes
Author: Shirley Chen
Description: This module provides visualization tools for analyzing and displaying
             story likes data for the Preservr project. It processes story likes datasets
             and generates a word cloud to visualize which users had interacted most with
             the user's stories.
Input: story_likes.json file stored in the provided folder path.
Output: Visualization saved as story_likes_visualization.png in the same folder.
Date: 2025-03
"""

import os
import sys
import json
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

def generate_story_likes_wordcloud(folder_path):
    """
    Generate a word cloud from story likes in the given folder.
    """
    # Construct file paths
    input_path = os.path.join(folder_path, "story_likes.json")
    output_path = os.path.join(folder_path, "story_likes_visualization.png")

    # Load JSON file
    with open(input_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Extract story likes
    likes = [entry["title"] for entry in data.get("story_activities_story_likes", [])]

    # Count occurrences of each user
    like_counts = Counter(likes)

    if not like_counts:
        print("No likes data found.")
        return

    # Identify top liker
    most_active_liker, max_likes = like_counts.most_common(1)[0]

    # Generate word cloud
    wc = WordCloud(width=800, height=500, background_color="white", colormap="coolwarm")
    wc.generate_from_frequencies(like_counts)

    # Plot and save the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Frequent Story Likers (Top: {most_active_liker} - {max_likes} likes)")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Visualization saved to: {output_path}")

# Entry point for CLI usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python story_likes_visualization.py <folder_path>")
        sys.exit(1)

    folder = sys.argv[1]
    generate_story_likes_wordcloud(folder)
