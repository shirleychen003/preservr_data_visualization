'''
Preservr Data Visualizations
Author: Luca Carnegie
Description: This module provides visualization tools for analyzing and displaying
            comment data for the Preservr project. It processes comment datasets
            and generates visualizations to help understand engagement patterns
            and content characteristics.
Input: Comment data files stored in the 'data' directory
Output: Visualization files saved to the 'output' directory
Date: 2023-11-21
'''

import json
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

owners = []
owner_counts = None

def most_commented_barchart():
    """
    Create a bar chart showing the number of comments per user.
    """
    global owner_counts
    # Create a dictionary of media owners and their comment counts
    wordcloud_data = dict(zip(owner_counts["Media Owner"], owner_counts["Comment Count"]))
    
    # Generate the wordcloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcloud_data)
    
    # Plot the wordcloud
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("Accounts You Commented On Most")
    plt.tight_layout()
    
    plt.show()

"""     # Save the figure
    plt.savefig("output/media_owner_wordcloud.png")
    plt.close()

    print("Wordcloud saved to output/media_owner_wordcloud.png")
"""

def load_data():
    """
    Load the comment data from the JSON file.
    """
    # Load JSON file
    global owners, owner_counts
    with open("data/post_comments_1.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    # Extract media owners from the data
    media_owners = []
    for comment in data:
        try:
            media_owner = comment["string_map_data"].get("Media Owner", {}).get("value", "Unknown")
            media_owners.append(media_owner)
        except (KeyError, TypeError):
            media_owners.append("Unknown")

    # Create a DataFrame and count occurrences
    df = pd.DataFrame({"Media Owner": media_owners})
    owner_counts = df["Media Owner"].value_counts().reset_index()
    owner_counts.columns = ["Media Owner", "Comment Count"]
    owners = df
    owner_counts.columns = ["Media Owner", "Comment Count"]
    owner_counts = owner_counts[owner_counts["Media Owner"] != "Unknown"]
    

def main():
    load_data()
    most_commented_barchart()

main() 




