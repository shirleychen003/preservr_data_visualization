"""
Preservr Data Visualizations
Author: Luca Carnegie
Description: This module provides visualization tools for analyzing and displaying
             comment data for the Preservr project. It processes comment datasets
             and generates a word cloud to visualize the most commented media owners by
             the user.
Input: Comment data files stored in the 'data' directory
Output: Visualization files saved to the 'OUTPUT_FOLDER' directory
Date: 2023-11-21
"""

import json
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import sys

def find_file_in_subdirectories(folder_path, filename):
    """
    Recursively search for the specified file in subdirectories.
    """
    for root, dirs, files in os.walk(folder_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

def most_commented_barchart(owner_counts, output_path):
    """
    Create a bar chart showing the number of comments per user.

    Args:
        owner_counts (DataFrame): DataFrame containing media owners and comment counts
        output_path (str): Path to save the visualization
    """
    wordcloud_data = dict(zip(owner_counts["Media Owner"], owner_counts["Comment Count"]))

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcloud_data)

    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("Accounts You Commented On Most")
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()

def load_data(data_path):
    """
    Load the comment data from the JSON file.

    Args:
        data_path (str): Path to the post_comments JSON file

    Returns:
        DataFrame: DataFrame containing media owners and comment counts
    """
    try:
        with open(data_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        media_owners = []
        for comment in data:
            try:
                media_owner = comment["string_map_data"].get("Media Owner", {}).get("value", "Unknown")
                media_owners.append(media_owner)
            except (KeyError, TypeError):
                media_owners.append("Unknown")

        df = pd.DataFrame({"Media Owner": media_owners})
        owner_counts = df["Media Owner"].value_counts().reset_index()
        owner_counts.columns = ["Media Owner", "Comment Count"]
        owner_counts = owner_counts[owner_counts["Media Owner"] != "Unknown"]

        return owner_counts

    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame(columns=["Media Owner", "Comment Count"])

def process_comments(input_folder, output_path=None):
    """
    Process comments data and generate visualization.

    Args:
        input_folder (str): Path to the folder containing the data files
        output_path (str, optional): Path to save the visualization
    """
    if output_path is None:
        output_folder = os.path.join(input_folder, "OUTPUT_FOLDER")
        os.makedirs(output_folder, exist_ok=True)
        output_path = os.path.join(output_folder, "post_comments.png")

    comments_path = find_file_in_subdirectories(input_folder, "post_comments_1.json")

    if comments_path is None:
        print(f"Error: Could not find post_comments_1.json in {input_folder} or its subdirectories")
        return False

    owner_counts = load_data(comments_path)

    if not owner_counts.empty:
        most_commented_barchart(owner_counts, output_path)
        return True
    else:
        return False

def main():
    if len(sys.argv) > 1:
        input_folder = sys.argv[1]
        output_folder = os.path.join(input_folder, "OUTPUT_FOLDER")
        output_path = os.path.join(output_folder, "post_comments.png")

        success = process_comments(input_folder, output_path)
        if success:
            print(f"Visualization created at {output_path}")
        else:
            print("Failed to create visualization")
    else:
        print("Please provide a folder path as a command-line argument")

if __name__ == "__main__":
    main()
