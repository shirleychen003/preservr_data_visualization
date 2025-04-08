'''
Preservr Data Visualizations - Liked Posts
Author: Luca Carnegie
Description: This module provides visualization tools for analyzing and displaying
             liked posts data for the Preservr project. It processes liked posts datasets
             and generates a word cloud to visualize the most liked media owners by
             the user.
Input: Liked posts data files stored in the 'data' directory
Output: Visualization files saved to the 'output' directory
Date: 2023-11-21
'''
import json
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import sys
import os

titles = []
title_counts = None

def most_liked_wordcloud():
    """
    Create a wordcloud showing the number of likes per title (media owner).
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

    # Save the figure
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("Accounts You Liked Most")
    plt.tight_layout()

    plt.savefig("../preservr_data_visualization/images/liked_posts_wordcloud.png")
    plt.close()


def load_data(folder_path):
    """
    Load the liked posts data from the JSON file in the specified folder.
    """
    global titles, title_counts

    # Construct the full path to liked_posts.json
    liked_posts_path = os.path.join(folder_path, "liked_posts.json")

    # Load JSON file
    with open(liked_posts_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Extract titles (media owners) from the data
    media_titles = []
    for item in data.get("likes_media_likes", []):
        try:
            title = item.get("title", "Unknown")
            if title:
                media_titles.append(title)
        except (KeyError, TypeError):
            continue

    # Create a DataFrame and count occurrences
    df = pd.DataFrame({"Title": media_titles})
    title_counts = df["Title"].value_counts().reset_index()
    title_counts.columns = ["Title", "Like Count"]
    titles = df

    # Remove unknown entries
    title_counts = title_counts[title_counts["Title"] != "Unknown"]

def main():
    load_data()
    most_liked_wordcloud()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python liked_posts.py <folder_path>")
        sys.exit(1)

    folder = sys.argv[1]
    load_data(folder)