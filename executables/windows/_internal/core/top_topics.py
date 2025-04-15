"""
Preservr Data Visualizations - Top Topics

Author: Luca Carnegie
Description: This module provides visualization tools for analyzing and displaying
             top topics data for the Preservr project. It processes story likes datasets
             and generates a word cloud to visualize which 'Topics' of posts were post interacted 
             with during the archiving period. 
Input: Liked posts data files stored in the 'data' directory
Output: Visualization files saved to the 'OUTPUT_FOLDER' directory
Date: 2025-04-16
"""

import os
import sys
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def find_file_in_subdirectories(folder_path, filename):
    """
    Recursively search for the specified file in subdirectories.
    """
    for root, dirs, files in os.walk(folder_path):
        if filename in files:
            return os.path.join(root, filename)
    return None


def generate_topic_wordcloud(folder_path):
    """
    Generate a word cloud from recommended topics in the given folder.
    Saves the image to an OUTPUT_FOLDER inside folder_path.
    """
    # Search for the recommended_topics.json file in the folder and its subdirectories
    topics_path = find_file_in_subdirectories(folder_path, "recommended_topics.json")

    if topics_path is None:
        print(f"Error: Could not find recommended_topics.json in {folder_path} or its subdirectories")
        return

    # Create OUTPUT_FOLDER
    output_folder = os.path.join(folder_path, "OUTPUT_FOLDER")
    os.makedirs(output_folder, exist_ok=True)

    # Construct the output path inside OUTPUT_FOLDER
    output_path = os.path.join(output_folder, "top_topics.png")

    # Load the JSON file
    with open(topics_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Extract topic names
    topics = [
        item["string_map_data"]["Name"]["value"]
        for item in data.get("topics_your_topics", [])
        if "Name" in item.get("string_map_data", {})
    ]

    if not topics:
        print("No topics found to generate word cloud.")
        return

    # Join topics into a single string for word cloud generation
    text = " ".join(topics)

    # Generate word cloud
    wc = WordCloud(width=800, height=500, background_color="white").generate(text)

    # Print and save the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")

    # Save as PNG
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Visualization saved to: {output_path}")


# Entry point for command-line use
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python recommended_topics.py <folder_path>")
        sys.exit(1)

    folder = sys.argv[1]
    generate_topic_wordcloud(folder)
